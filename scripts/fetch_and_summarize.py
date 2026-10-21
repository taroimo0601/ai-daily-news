import argparse
import base64
from datetime import datetime, timedelta, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
from typing import Literal
import feedparser
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
import requests

JST = timezone(timedelta(hours=9))
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "docs" / "data"

RSS_SOURCES = [
    # 海外の公式発表・大手テックメディア
    {
        "name": "OpenAI News",
        "url": "https://openai.com/news/rss.xml",
        "category": "global",
        "max_items": 6,
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/",
        "category": "global",
        "max_items": 6,
    },
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "category": "global",
        "max_items": 8,
    },
    {
        "name": "The Verge AI",
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "category": "global",
        "max_items": 6,
    },
    # 国内の主要AIニュース・トレンド
    {
        "name": "ITmedia AI+",
        "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
        "category": "domestic",
        "max_items": 8,
    },
    {
        "name": "はてなブックマーク (AI)",
        "url": "https://b.hatena.ne.jp/q/AI?mode=rss&sort=recent&users=15",
        "category": "domestic",
        "max_items": 8,
    },
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AIDailyNewsBot/1.0; +https://github.com)"
}


class SelectedNewsItem(BaseModel):
    candidate_id: int = Field(description="候補記事リストの candidate_id（整数）")
    title_ja: str = Field(description="スマホで一目で内容がわかる自然な日本語タイトル（45文字以内）")
    rating: int = Field(
        description="おすすめ度（1〜5の5段階評価の整数。5が特に必見の最重要ニュース、3〜4が注目ニュース）",
        ge=1,
        le=5,
    )
    points: list[str] = Field(
        description="記事の要点を3行（3項目）で簡潔にまとめた箇条書きリスト。各項目は50〜70文字程度。"
    )
    insight: str = Field(
        description="一言解説：なぜこのニュースが重要か、または実務や日常にどう影響するか（60〜90文字程度）"
    )


class DailyDigest(BaseModel):
    headline: str = Field(description="今日のAI界隈のトレンドを一言で表すキャッチコピー（35文字以内）")
    overview: str = Field(description="今日の全体トレンドの30秒サマリー（120〜180文字程度）")
    items: list[SelectedNewsItem] = Field(description="その日のおすすめ重要ニュース（必ず10件）")


def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw_html)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:400]


def fetch_rss_articles() -> list[dict]:
    articles = []
    for src in RSS_SOURCES:
        try:
            resp = requests.get(src["url"], headers=HEADERS, timeout=15)
            resp.raise_for_status()
            feed = feedparser.parse(resp.content)
            for entry in feed.entries[: src["max_items"]]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                summary = clean_html(
                    entry.get("summary", "") or entry.get("description", "")
                )
                if title and link:
                    articles.append(
                        {
                            "category": src["category"],
                            "source": src["name"],
                            "title": title,
                            "url": link,
                            "summary": summary,
                        }
                    )
        except Exception as e:
            print(f"[WARN] Failed to fetch {src['name']}: {e}")
    return articles


def fetch_hf_daily_papers(max_items: int = 8) -> list[dict]:
    papers = []
    try:
        resp = requests.get(
            "https://huggingface.co/api/daily_papers", headers=HEADERS, timeout=15
        )
        resp.raise_for_status()
        data = resp.json()
        # Sort by upvotes descending if available
        data.sort(key=lambda x: x.get("paper", {}).get("upvotes", 0), reverse=True)
        for item in data[:max_items]:
            paper = item.get("paper", {})
            paper_id = paper.get("id", "")
            title = item.get("title") or paper.get("title", "")
            summary = clean_html(item.get("summary") or paper.get("summary", ""))
            if paper_id and title:
                papers.append(
                    {
                        "category": "paper",
                        "source": "Hugging Face Papers",
                        "title": title,
                        "url": f"https://huggingface.co/papers/{paper_id}",
                        "summary": summary,
                    }
                )
    except Exception as e:
        print(f"[WARN] Failed to fetch Hugging Face Daily Papers: {e}")
    return papers


def decrypt_digest_if_needed(content: dict, password: str) -> dict:
    if not content.get("encrypted"):
        return content
    if not password:
        return {}
    try:
        salt = base64.b64decode(content["salt"])
        cipher_bytes = base64.b64decode(content["ciphertext"])
        pwd_bytes = password.encode("utf-8")
        key = hashlib.sha256(salt + pwd_bytes).digest()
        plain_bytes = bytearray(len(cipher_bytes))
        for blk in range((len(cipher_bytes) + 31) // 32):
            ks = hashlib.sha256(key + blk.to_bytes(4, "big")).digest()
            s = blk * 32
            e = min(s + 32, len(cipher_bytes))
            for i in range(s, e):
                plain_bytes[i] = cipher_bytes[i] ^ ks[i - s]
        tag = hashlib.sha256(b"VERIFY:" + key + bytes(plain_bytes)).hexdigest()[:32]
        if tag != content.get("tag"):
            return {}
        return json.loads(bytes(plain_bytes).decode("utf-8"))
    except Exception:
        return {}


def load_recent_urls(days: int = 3) -> set[str]:
    """過去に配信した記事URLの重複を防ぐために直近数日分のURLを取得する"""
    seen_urls = set()
    if not DATA_DIR.exists():
        return seen_urls
    site_password = os.environ.get("SITE_PASSWORD", "").strip() or "0000"
    json_files = sorted(DATA_DIR.glob("20*.json"), reverse=True)[:days]
    for path in json_files:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            content = decrypt_digest_if_needed(raw, site_password)
            for item in content.get("items", []):
                if "url" in item:
                    seen_urls.add(item["url"])
        except Exception:
            pass
    return seen_urls


def summarize_with_gemini(candidates: list[dict], date_str: str) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "環境変数 GEMINI_API_KEY が設定されていません。Google AI Studioで発行したキーを設定してください。"
        )

    client = genai.Client(api_key=api_key)

    indexed_candidates = [
        {"candidate_id": idx, **item} for idx, item in enumerate(candidates)
    ]
    candidates_text = json.dumps(indexed_candidates, ensure_ascii=False, indent=2)
    prompt = f"""あなたは優秀なAI専門ニュースキュレーターです。
本日（{date_str}）収集された以下のAI関連ニュースおよび最新論文の候補リストから、通勤中やスキマ時間にスマホでサクッと読める「今日のおすすめAIニュース厳選10件」を作成してください。

選定・要約のルール:
1. 必ず合計10件を選定し、複数のサイト（情報源）から偏りなくバランスよく選んでください:
   - 海外の公式発表・大手メディア (category: "global" / OpenAI News, Google AI Blog, TechCrunch AI, The Verge AI): 4件
   - 国内の主要AIニュース・トレンド (category: "domestic" / ITmedia AI+, はてなブックマーク (AI)): 4件
   - 最新の注目AI論文 (category: "paper" / Hugging Face Papers): 2件
2. 専門用語が多すぎる場合や英語の記事・論文は、非専門家でも直感的に理解できる自然な日本語に噛み砕いて翻訳・要約してください。
3. 各ニュースの points は必ず3項目（3行）の箇条書きにし、スマホ画面でパッと読める簡潔な文（各50〜70文字程度）にしてください。
4. rating には、業界へのインパクトや実用性の高さに応じた「おすすめ度」を1〜5の5段階（整数）で評価してください（5: 最重要・必見、4: 非常に有益、3: 押さえておきたい、等）。
5. insight には「なぜこのニュースが重要か」「私たちの仕事や開発にどう関わるか」の一言解説を入れてください。
6. candidate_id には、元になった候補記事の candidate_id（整数）を正確に指定してください。

候補記事リスト:
{candidates_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=DailyDigest,
            temperature=0.3,
        ),
    )

    digest_data = json.loads(response.text)
    candidate_map = {item["candidate_id"]: item for item in indexed_candidates}

    resolved_items = []
    for selected in digest_data["items"]:
        cid = selected["candidate_id"]
        orig = candidate_map.get(cid)
        if not orig:
            continue
        resolved_items.append(
            {
                "title_ja": selected["title_ja"],
                "category": orig["category"],
                "source": orig["source"],
                "url": orig["url"],
                "rating": selected["rating"],
                "points": selected["points"],
                "insight": selected["insight"],
            }
        )

    return {
        "date": date_str,
        "generated_at": datetime.now(JST).strftime("%Y-%m-%d %H:%M JST"),
        "headline": digest_data["headline"],
        "overview": digest_data["overview"],
        "items": resolved_items,
    }


def encrypt_digest(digest: dict, password: str) -> dict:
    """パスワードを用いてニュースJSONデータをSHA-256ストリーム暗号化する"""
    plaintext = json.dumps(digest, ensure_ascii=False).encode("utf-8")
    salt = os.urandom(16)
    pwd_bytes = password.encode("utf-8")
    key = hashlib.sha256(salt + pwd_bytes).digest()

    tag = hashlib.sha256(b"VERIFY:" + key + plaintext).hexdigest()[:32]

    cipher_bytes = bytearray(len(plaintext))
    block_count = (len(plaintext) + 31) // 32
    for blk in range(block_count):
        keystream = hashlib.sha256(key + blk.to_bytes(4, "big")).digest()
        start = blk * 32
        end = min(start + 32, len(plaintext))
        for i in range(start, end):
            cipher_bytes[i] = plaintext[i] ^ keystream[i - start]

    return {
        "date": digest["date"],
        "generated_at": digest["generated_at"],
        "encrypted": True,
        "salt": base64.b64encode(salt).decode("ascii"),
        "tag": tag,
        "ciphertext": base64.b64encode(bytes(cipher_bytes)).decode("ascii"),
    }


def save_digest(digest: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    date_str = digest["date"]
    target_file = DATA_DIR / f"{date_str}.json"

    site_password = os.environ.get("SITE_PASSWORD", "").strip() or "0000"
    payload = encrypt_digest(digest, site_password)

    target_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Update index.json with available dates (newest first, up to 30 days)
    dates = sorted(
        [p.stem for p in DATA_DIR.glob("20*.json")],
        reverse=True,
    )[:30]

    index_payload = {
        "latest_date": dates[0] if dates else date_str,
        "available_dates": dates,
        "updated_at": digest["generated_at"],
    }
    index_file = DATA_DIR / "index.json"
    index_file.write_text(
        json.dumps(index_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"[INFO] Saved {target_file} (encrypted={bool(site_password)}) and updated {index_file}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch and summarize daily AI news")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch feeds and print candidate count without calling Gemini API",
    )
    args = parser.parse_args()

    now_jst = datetime.now(JST)
    date_str = now_jst.strftime("%Y-%m-%d")

    print(f"[INFO] Fetching AI news candidates for {date_str}...")
    seen_urls = load_recent_urls(days=3)

    rss_items = fetch_rss_articles()
    paper_items = fetch_hf_daily_papers()
    all_candidates = [
        item for item in (rss_items + paper_items) if item["url"] not in seen_urls
    ]

    # Fallback if all were filtered out
    if len(all_candidates) < 10:
        all_candidates = rss_items + paper_items

    print(
        f"[INFO] Collected {len(all_candidates)} candidate items (RSS: {len(rss_items)}, Papers: {len(paper_items)})"
    )

    if args.dry_run:
        for idx, item in enumerate(all_candidates[:10], 1):
            print(f"  {idx}. [{item['category']}] {item['source']}: {item['title']}")
        return

    digest = summarize_with_gemini(all_candidates, date_str)
    save_digest(digest)


if __name__ == "__main__":
    main()
