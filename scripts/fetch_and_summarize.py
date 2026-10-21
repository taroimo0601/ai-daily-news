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


def is_mostly_english(text: str) -> bool:
    if not text:
        return False
    # ひらがな・カタカナが含まれていれば日本語と判定
    if re.search(r"[\u3040-\u30ff]", text):
        return False
    ascii_letters = sum(1 for c in text if ("a" <= c.lower() <= "z"))
    return ascii_letters > 5


def translate_en_to_ja(text: str) -> str:
    """APIキー不要の無料翻訳API（MyMemory）で英語テキストを自然な日本語に翻訳する"""
    cleaned = text.strip()
    if not cleaned or not is_mostly_english(cleaned):
        return cleaned
    try:
        resp = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": cleaned[:480], "langpair": "en|ja"},
            headers=HEADERS,
            timeout=12,
        )
        resp.raise_for_status()
        translated = (
            resp.json().get("responseData", {}).get("translatedText", "").strip()
        )
        if translated and "MYMEMORY WARNING" not in translated:
            return html.unescape(translated)
    except Exception as e:
        print(f"[WARN] Translation fallback error: {e}")
    return cleaned


def call_github_models_fallback(candidates: list[dict], date_str: str, github_token: str) -> dict:
    """GitHub Actions内蔵のGITHUB_TOKEN（無料枠）を使って日本語要約を生成する"""
    url = "https://models.github.ai/inference/chat/completions"
    # トークン上限を超えないよう各サイトからバランスよく最大14件に絞って渡す
    by_source: dict[str, list[dict]] = {}
    for c in candidates:
        by_source.setdefault(c["source"], []).append(c)
    compact_list = []
    for round_idx in range(3):
        for src, items in by_source.items():
            if round_idx < len(items) and len(compact_list) < 14:
                it = items[round_idx]
                compact_list.append({
                    "candidate_id": it["candidate_id"],
                    "source": it["source"],
                    "category": it["category"],
                    "title": it["title"][:120],
                    "summary": it.get("summary", "")[:220],
                })

    prompt = f"""本日（{date_str}）のAIニュース候補リストから、スマホで読める「今日のおすすめAIニュース10件」を厳選し、英語の記事・論文もすべて自然な日本語に翻訳・要約してJSONで出力してください。
- 必ず合計10件選び、各ニュースの title_ja（日本語タイトル）、points（日本語3行の要点リスト）、insight（日本語の一言解説）、rating（1〜5の整数）、candidate_id（元の整数ID）を含めてください。
- 英語のまま残さず、必ずすべて日本語で記述してください。

候補リスト:
{json.dumps(compact_list, ensure_ascii=False)}

出力形式（純粋なJSONのみ）:
{{
  "headline": "キャッチコピー（35文字以内・日本語）",
  "overview": "今日の全体トレンドの30秒サマリー（120〜180文字程度・日本語）",
  "items": [
    {{
      "candidate_id": 0,
      "title_ja": "日本語タイトル（45文字以内）",
      "rating": 5,
      "points": ["日本語の要点1", "日本語の要点2", "日本語の要点3"],
      "insight": "日本語の一言解説（60〜90文字程度）"
    }}
  ]
}}"""

    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {github_token}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "あなたは優秀な日本のAIニュース編集者です。すべてのタイトルと要約を自然な日本語に翻訳してJSON形式で出力します。"},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.3,
        },
        timeout=60,
    )
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def build_rss_fallback_digest(indexed_candidates: list[dict], date_str: str) -> dict:
    """APIクレジット不足時でも無料翻訳を使ってサイト別10件を日本語で生成するフォールバック"""
    by_source: dict[str, list[dict]] = {}
    for c in indexed_candidates:
        by_source.setdefault(c["source"], []).append(c)

    selected = []
    # 各サイトから最大2件ずつバランスよく最大10件選ぶ
    for round_idx in range(2):
        for src, items in by_source.items():
            if round_idx < len(items) and len(selected) < 10:
                selected.append(items[round_idx])

    resolved_items = []
    for idx, orig in enumerate(selected):
        title_ja = translate_en_to_ja(orig["title"])[:65]
        raw_summary = orig.get("summary", "") or orig["title"]
        summary_ja = translate_en_to_ja(raw_summary)

        sentences = [
            s.strip()
            for s in re.split(r"[。.!?！？\n]+", summary_ja)
            if len(s.strip()) > 6
        ]
        points = [s + ("。" if not s.endswith("。") else "") for s in sentences[:3]]
        if not points:
            points.append(f"{title_ja} に関する最新発表です。")
        if len(points) == 1:
            points.append(f"{orig['source']} で公開された注目のAI動向・活用事例です。")
        if len(points) == 2:
            points.append("詳しい検証データや背景については「元記事を開く」から確認できます。")

        if orig["category"] == "paper":
            insight = "Hugging Faceで注目されている最新AI研究論文。手法や実験結果の詳細は元論文ページで確認できます。"
        elif orig["category"] == "global":
            insight = f"{orig['source']} による海外の最新AIトレンド・公式発表。今後のツール活用や開発動向の参考になります。"
        else:
            insight = f"{orig['source']} で話題の国内AIニュース。実務への応用や業界動向の把握に役立ちます。"

        resolved_items.append(
            {
                "title_ja": title_ja,
                "category": orig["category"],
                "source": orig["source"],
                "url": orig["url"],
                "rating": 5 if idx < 3 else 4,
                "points": [p[:90] for p in points[:3]],
                "insight": insight,
            }
        )

    return {
        "date": date_str,
        "generated_at": datetime.now(JST).strftime("%Y-%m-%d %H:%M JST"),
        "headline": f"{date_str} の注目AIニュース・論文ピックアップ10選",
        "overview": "海外公式ブログ・大手テックメディア・国内AIメディア・Hugging Face注目論文から最新の10件を厳選し、日本語に翻訳・要約しました。",
        "items": resolved_items,
    }


def summarize_with_gemini(candidates: list[dict], date_str: str) -> dict:
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

    digest_data = None
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if api_key:
        client = genai.Client(api_key=api_key)
        for model_name in ["gemini-3.8-flash", "gemini-3.8-flash-lite", "gemini-2.0-flash"]:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=DailyDigest,
                        temperature=0.3,
                    ),
                )
                digest_data = json.loads(response.text)
                print(f"[INFO] Summarized successfully with Gemini ({model_name})")
                break
            except Exception as e:
                print(f"[WARN] Gemini ({model_name}) failed: {e}")

    if digest_data is None:
        github_token = os.environ.get("GITHUB_TOKEN", "").strip()
        if github_token:
            try:
                print("[INFO] Trying free GitHub Models fallback...")
                digest_data = call_github_models_fallback(
                    indexed_candidates, date_str, github_token
                )
                print("[INFO] Summarized successfully with GitHub Models (gpt-4o-mini)")
            except Exception as e:
                print(f"[WARN] GitHub Models fallback failed: {e}")

    if digest_data is None:
        print("[WARN] Using built-in RSS fallback summarizer...")
        return build_rss_fallback_digest(indexed_candidates, date_str)

    candidate_map = {item["candidate_id"]: item for item in indexed_candidates}

    resolved_items = []
    for selected in digest_data.get("items", []):
        cid = selected.get("candidate_id")
        orig = candidate_map.get(cid)
        if not orig:
            continue
        title_ja = translate_en_to_ja(selected.get("title_ja", orig["title"]))
        points_ja = [translate_en_to_ja(pt) for pt in selected.get("points", [])[:3]]
        insight_ja = translate_en_to_ja(selected.get("insight", ""))
        resolved_items.append(
            {
                "title_ja": title_ja,
                "category": orig["category"],
                "source": orig["source"],
                "url": orig["url"],
                "rating": selected.get("rating", 4),
                "points": points_ja,
                "insight": insight_ja,
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
