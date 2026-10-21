const CATEGORY_LABELS = {
  global: "海外公式・大手",
  domestic: "国内トレンド",
  paper: "最新注目論文",
};

const FALLBACK_DIGEST = {
  date: "2026-10-21",
  generated_at: "2026-10-21 06:00 JST",
  headline: "Gemini 4 Argon公開とOpenAI常時稼働エージェント「Dots」の日本急拡大",
  overview:
    "海外ではGoogleの最新フロンティアモデル「Gemini 4 Argon」の発表や車載Android AutoへのAI統合、OpenAIの企業向け導入事例が注目を集めています。国内ではOpenAIの常時稼働エージェント「Dots」の日本ユーザー数が世界2位に達したことが大きな話題となっています。",
  items: [
    {
      title_ja: "ChatGPT Workの活用でフランチャイズ店舗の現金照合時間を94%削減",
      category: "global",
      source: "OpenAI News",
      url: "https://openai.com/index/ted-taylor-restaurant",
      rating: 4,
      points: [
        "米国の飲食店フランチャイズオーナーがChatGPT Workでバックオフィス業務を自動化",
        "メニュー価格の再設定にかかる時間を95%削減し、現金照合の作業時間も94%短縮",
        "業務フローの改善により年間約10万ドルのキャッシュフロー改善効果を見込む"
      ],
      insight: "非IT企業や店舗経営でも、日常の経理・価格改定業務にAIを組み込むだけで大きな投資対効果が出ています。"
    },
    {
      title_ja: "投資評価AI「Terminal X」がGPT-6.1活用でベテラン投資家の判断と88.6%一致",
      category: "global",
      source: "OpenAI News",
      url: "https://openai.com/index/terminal-x",
      rating: 5,
      points: [
        "54項目の評価ルーブリックに基づき、投資案件の出力を自動採点する評価エージェントを構築",
        "ファンドの投資方針からの逸脱を従来比で25%多く検出することに成功",
        "シニア投資家の判断との一致率が88.6%に達し、デューデリジェンスを大幅に高速化"
      ],
      insight: "明確な評価基準（ルーブリック）を定義すれば、高度な専門判断の一次スクリーニングもAIで高精度に代替可能です。"
    },
    {
      title_ja: "Google、最新フロンティアモデル「Gemini 4 Argon」を公開",
      category: "global",
      source: "Google AI Blog",
      url: "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/",
      rating: 5,
      points: [
        "複雑な推論・コーディング・科学計算などの難問解決に特化した最新モデル「Gemini 4 Argon」を発表",
        "開発者、エンタープライズ企業、研究者、一般ユーザー向けに提供を開始",
        "長文脈の理解力とマルチステップのエージェント実行能力が大幅に強化"
      ],
      insight: "複雑なシステム設計や高度なデータ分析タスクにおいて、最優先で試すべき最新フラッグシップモデルです。"
    },
    {
      title_ja: "Anthropic、大規模被害リスクがあるAIモデルを差し止め可能なAI安全法案を提唱",
      category: "global",
      source: "TechCrunch AI",
      url: "https://techcrunch.com/2026/10/20/anthropic-pitches-ai-safety-bill-that-may-block-a-model-if-50-people-could-be-killed/",
      rating: 4,
      points: [
        "重大な人的被害が生じる恐れがある場合にモデルの公開を制限する新たな安全フレームワークを提案",
        "一方で連邦機関が裁判所の許可なしにモデル公開を一方的に差し止めることは禁じる条項も含む",
        "AIの安全性確保と過剰規制の防止をどう両立するかを巡り米国内で議論が活発化"
      ],
      insight: "今後の米国AI規制の方向性を左右する動きであり、フロンティアモデル提供各社のガバナンス基準に影響します。"
    },
    {
      title_ja: "Google、車載システム「Android Auto」にパーソナライズ化されたGemini AIを統合",
      category: "global",
      source: "The Verge AI",
      url: "https://www.theverge.com/tech/1014999/google-gemini-ai-cars-android-auto",
      rating: 4,
      points: [
        "Android AutoおよびGoogle搭載車両で、Gmail・カレンダー・マップ・YouTube等と連携するGeminiが利用可能に",
        "運転中に音声だけで予定の確認やメール内容に基づく目的地設定がスムーズに行える",
        "パーソナルインテリジェンス機能により個人の予定や文脈に合わせた自然な対話を実現"
      ],
      insight: "スマホ画面を見られない移動中・運転中こそ、パーソナルデータと連携した音声AIエージェントの価値が最も発揮されます。"
    },
    {
      title_ja: "OpenAIの常時稼働エージェント「Dots」、日本のユーザー数が世界2位に",
      category: "domestic",
      source: "ITmedia AI+",
      url: "https://www.itmedia.co.jp/aiplus/article/2610/21/2000002457/",
      rating: 5,
      points: [
        "OpenAI Japanの長崎忠雄社長が、新AIエージェント機能「Dots」の日本ユーザー数が世界2位と発表",
        "人間が都度指示しなくてもバックグラウンドで常時稼働し業務を遂行するスタイルが国内で急速に浸透",
        "「日本の働き方や仕事の在り方を大きく変える可能性がある」と企業導入の加速に言及"
      ],
      insight: "国内でも単発のチャット利用から「常時稼働型エージェント」へのシフトが一気に進んでいます。"
    },
    {
      title_ja: "予算やツールを入れてもDX・セキュリティ移行が止まる「組織摩擦」の正体",
      category: "domestic",
      source: "ITmedia AI+",
      url: "https://mag.executive.itmedia.co.jp/executive/article/2610/21/2000002352/",
      rating: 3,
      points: [
        "最新ツールや予算を確保しても社内導入が進まない原因を「組織の摩擦」という視点から分析",
        "250社以上の実装支援から見えた、部署間の壁や既存業務フローへの固執を数値化する手法を紹介",
        "AIやセキュリティ製品の導入成功には技術選定以上に組織設計と合意形成が不可欠と指摘"
      ],
      insight: "社内へAIツールを導入する際、技術検証だけでなく現場の運用負荷や組織摩擦をどう下げるかの参考になります。"
    },
    {
      title_ja: "AIに200万円渡してネットショップを1年運営させる実験、資産14倍の例も",
      category: "domestic",
      source: "はてなブックマーク (AI)",
      url: "https://www.itmedia.co.jp/news/article/2610/21/2000002421/",
      rating: 5,
      points: [
        "Alibabaの研究者らがAIエージェントに初期資金を与えてEC店舗を1年間自律運営させるシミュレーションを実施",
        "商品選定・価格設定・在庫管理・広告運用までをAIが判断し、資産を14倍に増やしたモデルも登場",
        "長期的な経営判断におけるLLMエージェントの強みと失敗パターンを詳細に検証"
      ],
      insight: "EC運営やマーケティングの意思決定ループをAIエージェントに委ねる自律型コマースの可能性を示す注目研究です。"
    },
    {
      title_ja: "米国人の「恐怖の対象」調査、AIによる政治介入や世論操作が上位に",
      category: "domestic",
      source: "はてなブックマーク (AI)",
      url: "https://japan.cnet.com/article/35253804/",
      rating: 3,
      points: [
        "米国の最新世論調査で、AIを用いた政治介入やフェイク情報が国民の強い懸念事項として3位に浮上",
        "ディープフェイクや自動ボットによる世論誘導への警戒感が急速に高まっていることが判明",
        "AIコンテンツの来歴証明（ウォーターマーク等）やプラットフォーム側の透明性確保が急務に"
      ],
      insight: "生成AIの出力物を公開・発信する企業にとっても、情報の真正性担保やファクトチェック体制がより重要になっています。"
    },
    {
      title_ja: "Specter: 量子化と投機的オフロードを組み合わせたMoEモデルの高速推論手法",
      category: "paper",
      source: "Hugging Face Papers",
      url: "https://huggingface.co/papers/2511.14102",
      rating: 4,
      points: [
        "単一GPUのメモリに収まらない大規模MoEモデルを高速に推論するための新システム「Specter」を提案",
        "PCIe通信のボトルネックを解消するため、量子化とマルチステップの投機的オフロードを統合",
        "限られたGPUリソース環境でも大規模MoEモデルの実用的なスループットを実現"
      ],
      insight: "ローカル環境や低コストGPUサーバーで大規模なMoE（Mixture-of-Experts）モデルを動かす際の重要技術です。"
    }
  ]
};

let currentDigest = null;
let activeSite = "all";
let unreadOnly = false;

const STORAGE_PREFIX = "manual_read_v2_";

function clearLegacyAutoReadStorage() {
  try {
    const keysToRemove = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k && k.startsWith("read_items_")) {
        keysToRemove.push(k);
      }
    }
    keysToRemove.forEach((k) => localStorage.removeItem(k));
  } catch {
    // ignore storage errors
  }
}

function getReadSet(dateStr) {
  try {
    const raw = localStorage.getItem(`${STORAGE_PREFIX}${dateStr}`);
    return new Set(raw ? JSON.parse(raw) : []);
  } catch {
    return new Set();
  }
}

function saveReadSet(dateStr, setObj) {
  try {
    localStorage.setItem(`${STORAGE_PREFIX}${dateStr}`, JSON.stringify([...setObj]));
  } catch {
    // ignore storage errors
  }
}

function formatStars(rating) {
  const score = Math.max(1, Math.min(5, Number(rating) || 4));
  return "★".repeat(score) + "☆".repeat(5 - score);
}

function initTheme() {
  const saved = localStorage.getItem("theme_mode") || "dark";
  document.documentElement.setAttribute("data-theme", saved);
  const btn = document.getElementById("theme-toggle");
  btn.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme_mode", next);
  });
}

function getOrderedSites(items) {
  const seen = new Set();
  const sites = [];
  for (const item of items) {
    const src = item.source || "その他";
    if (!seen.has(src)) {
      seen.add(src);
      sites.push(src);
    }
  }
  return sites;
}

function updateSummaryCounts(digest, scrollActiveIntoView = false) {
  const readSet = getReadSet(digest.date);
  const total = digest.items.length;
  const count = digest.items.filter((item) => readSet.has(item.url)).length;
  document.getElementById("read-progress").textContent = `既読 ${count} / ${total}`;

  // Update each site header count in DOM
  document.querySelectorAll(".site-section").forEach((sec) => {
    const siteName = sec.dataset.site;
    const siteItems = digest.items.filter((i) => i.source === siteName);
    const siteRead = siteItems.filter((i) => readSet.has(i.url)).length;
    const countEl = sec.querySelector(".site-count");
    if (countEl) {
      countEl.textContent = `既読 ${siteRead}/${siteItems.length}件`;
    }
  });

  // Update site tab counts
  renderSiteTabs(digest, scrollActiveIntoView);
}

function renderSiteTabs(digest, scrollActiveIntoView = false) {
  const tabsEl = document.getElementById("site-tabs");
  const prevScrollLeft = tabsEl.scrollLeft;
  const readSet = getReadSet(digest.date);
  const sites = getOrderedSites(digest.items);

  const totalUnread = digest.items.filter((i) => !readSet.has(i.url)).length;
  let html = `
    <button class="tab-btn ${activeSite === "all" ? "active" : ""}" data-site="all" type="button">
      <span>すべて（サイト別）</span>
      <span class="tab-count">未読${totalUnread}/${digest.items.length}</span>
    </button>
  `;

  for (const site of sites) {
    const siteItems = digest.items.filter((i) => i.source === site);
    const siteUnread = siteItems.filter((i) => !readSet.has(i.url)).length;
    const isActive = activeSite === site ? "active" : "";
    html += `
      <button class="tab-btn ${isActive}" data-site="${escapeHtml(site)}" type="button">
        <span>${escapeHtml(site)}</span>
        <span class="tab-count">${siteUnread > 0 ? `未読${siteUnread}` : "✓"}</span>
      </button>
    `;
  }

  tabsEl.style.scrollBehavior = "auto";
  tabsEl.innerHTML = html;
  tabsEl.scrollLeft = prevScrollLeft;
  tabsEl.style.scrollBehavior = "";

  if (scrollActiveIntoView) {
    const activeBtn = tabsEl.querySelector(".tab-btn.active");
    if (activeBtn) {
      activeBtn.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
    }
  }

  tabsEl.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (tabsEl.dataset.dragging === "true") return;
      activeSite = btn.dataset.site;
      renderDigest(currentDigest, true);
    });
  });
}

function markCardAsRead(digest, item, cardEl) {
  const latestSet = getReadSet(digest.date);
  if (latestSet.has(item.url)) return;

  latestSet.add(item.url);
  saveReadSet(digest.date, latestSet);

  cardEl.classList.add("is-read");
  const statusBadge = cardEl.querySelector(".status-badge");
  if (statusBadge) statusBadge.textContent = "✓ 既読";
  const readBtn = cardEl.querySelector(".read-btn");
  if (readBtn) readBtn.textContent = "未読に戻す";

  updateSummaryCounts(digest);
  if (unreadOnly) {
    renderDigest(digest);
  }
}

function toggleCardReadManual(digest, item, cardEl) {
  const latestSet = getReadSet(digest.date);
  const statusBadge = cardEl.querySelector(".status-badge");
  const readBtn = cardEl.querySelector(".read-btn");

  if (latestSet.has(item.url)) {
    latestSet.delete(item.url);
    cardEl.classList.remove("is-read");
    if (statusBadge) statusBadge.textContent = "● 未読";
    if (readBtn) readBtn.textContent = "既読にする";
  } else {
    latestSet.add(item.url);
    cardEl.classList.add("is-read");
    if (statusBadge) statusBadge.textContent = "✓ 既読";
    if (readBtn) readBtn.textContent = "未読に戻す";
  }

  saveReadSet(digest.date, latestSet);
  updateSummaryCounts(digest);
  if (unreadOnly) {
    renderDigest(digest);
  }
}

function setupTabsScrollControls() {
  const tabsEl = document.getElementById("site-tabs");
  const leftBtn = document.getElementById("tabs-scroll-left");
  const rightBtn = document.getElementById("tabs-scroll-right");

  if (leftBtn) {
    leftBtn.addEventListener("click", () => {
      tabsEl.scrollBy({ left: -200, behavior: "smooth" });
    });
  }
  if (rightBtn) {
    rightBtn.addEventListener("click", () => {
      tabsEl.scrollBy({ left: 200, behavior: "smooth" });
    });
  }

  // マウスホイールでの横スクロール対応
  tabsEl.addEventListener(
    "wheel",
    (e) => {
      if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
        e.preventDefault();
        tabsEl.scrollLeft += e.deltaY;
      }
    },
    { passive: false }
  );

  // マウスドラッグでの横スクロール対応
  let isDown = false;
  let startX = 0;
  let scrollStart = 0;

  tabsEl.addEventListener("mousedown", (e) => {
    isDown = true;
    tabsEl.dataset.dragging = "false";
    startX = e.pageX - tabsEl.offsetLeft;
    scrollStart = tabsEl.scrollLeft;
  });

  window.addEventListener("mouseup", () => {
    isDown = false;
    setTimeout(() => {
      tabsEl.dataset.dragging = "false";
    }, 50);
  });

  tabsEl.addEventListener("mousemove", (e) => {
    if (!isDown) return;
    const x = e.pageX - tabsEl.offsetLeft;
    const walk = x - startX;
    if (Math.abs(walk) > 6) {
      tabsEl.dataset.dragging = "true";
      e.preventDefault();
      tabsEl.scrollLeft = scrollStart - walk;
    }
  });
}

function renderDigest(digest, scrollActiveIntoView = false) {
  currentDigest = digest;
  document.getElementById("digest-date").textContent = `${digest.date}（おすすめ10選）`;
  document.getElementById("digest-headline").textContent = digest.headline;
  document.getElementById("digest-overview").textContent = digest.overview;

  const listEl = document.getElementById("news-list");
  listEl.innerHTML = "";

  const readSet = getReadSet(digest.date);
  const sites = getOrderedSites(digest.items).filter(
    (site) => activeSite === "all" || site === activeSite
  );

  let renderedCount = 0;

  sites.forEach((siteName) => {
    const allSiteItems = digest.items.filter((item) => item.source === siteName);
    const visibleItems = allSiteItems.filter(
      (item) => !unreadOnly || !readSet.has(item.url)
    );

    if (visibleItems.length === 0) return;

    const sectionEl = document.createElement("section");
    sectionEl.className = "site-section";
    sectionEl.dataset.site = siteName;

    const firstCategory = allSiteItems[0]?.category || "global";
    const categoryLabel = CATEGORY_LABELS[firstCategory] || firstCategory;
    const siteReadCount = allSiteItems.filter((i) => readSet.has(i.url)).length;

    sectionEl.innerHTML = `
      <div class="site-header">
        <div class="site-title-group">
          <span class="category-badge ${escapeHtml(firstCategory)}">${escapeHtml(categoryLabel)}</span>
          <h3 class="site-title">${escapeHtml(siteName)}</h3>
        </div>
        <span class="site-count">既読 ${siteReadCount}/${allSiteItems.length}件</span>
      </div>
    `;

    visibleItems.forEach((item) => {
      renderedCount += 1;
      const isRead = readSet.has(item.url);
      const card = document.createElement("article");
      card.className = `news-card${isRead ? " is-read" : ""}`;
      card.dataset.url = item.url;

      const globalIndex = digest.items.indexOf(item) + 1;
      const starsText = formatStars(item.rating);
      const pointsHtml = (item.points || [])
        .map((pt) => `<li>${escapeHtml(pt)}</li>`)
        .join("");

      card.innerHTML = `
        <div class="card-header">
          <div class="badge-group">
            <span class="source-name">#${globalIndex}</span>
            <span class="rating-badge" aria-label="おすすめ度 ${escapeHtml(item.rating || 4)} / 5">
              <span class="rating-label">おすすめ度</span>
              <span class="rating-stars">${starsText}</span>
            </span>
          </div>
          <span class="status-badge">${isRead ? "✓ 既読" : "● 未読"}</span>
        </div>
        <h4 class="card-title">
          <a class="title-link" href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">
            ${escapeHtml(item.title_ja)}
          </a>
        </h4>
        <ul class="points-list">${pointsHtml}</ul>
        <div class="insight-box">
          <span class="insight-label">💡 ポイント:</span>
          <span>${escapeHtml(item.insight)}</span>
        </div>
        <div class="card-footer">
          <button class="read-btn" type="button">
            ${isRead ? "未読に戻す" : "既読にする"}
          </button>
          <a class="source-link" href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">
            元記事を開く →
          </a>
        </div>
      `;

      // 記事タイトルをタップ（クリック）して読んだときに既読にする
      const titleLink = card.querySelector(".title-link");
      titleLink.addEventListener("click", () => {
        markCardAsRead(digest, item, card);
      });

      // 手動の既読・未読切り替えボタン
      const readBtn = card.querySelector(".read-btn");
      readBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        toggleCardReadManual(digest, item, card);
      });

      // 元記事リンクをタップした際にも既読にする
      const sourceLink = card.querySelector(".source-link");
      sourceLink.addEventListener("click", () => {
        markCardAsRead(digest, item, card);
      });

      sectionEl.appendChild(card);
    });

    listEl.appendChild(sectionEl);
  });

  if (renderedCount === 0) {
    listEl.innerHTML = `
      <div class="empty-state">
        表示できる未読記事はありません。すべて既読です！
      </div>
    `;
  }

  updateSummaryCounts(digest, scrollActiveIntoView);
  autoTranslateDigestItems(digest);
}

function isMostlyEnglishText(str) {
  if (!str) return false;
  if (/[\u3040-\u30ff]/.test(str)) return false;
  const asciiCount = (str.match(/[a-zA-Z]/g) || []).length;
  return asciiCount > 5;
}

async function translateTextEnToJa(text) {
  const cleaned = String(text || "").trim();
  if (!cleaned || !isMostlyEnglishText(cleaned)) return cleaned;

  const cacheKey = `tr_ja_${cleaned.slice(0, 120)}`;
  try {
    const cached = localStorage.getItem(cacheKey);
    if (cached) return cached;
  } catch {
    // ignore
  }

  try {
    const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(
      cleaned.slice(0, 450)
    )}&langpair=en|ja`;
    const res = await fetch(url);
    if (!res.ok) return cleaned;
    const data = await res.json();
    const translated = (data?.responseData?.translatedText || "").trim();
    if (translated && !translated.includes("MYMEMORY WARNING")) {
      try {
        localStorage.setItem(cacheKey, translated);
      } catch {
        // ignore
      }
      return translated;
    }
  } catch {
    // ignore network errors
  }
  return cleaned;
}

async function autoTranslateDigestItems(digest) {
  if (!digest || !Array.isArray(digest.items)) return;
  let updated = false;

  for (const item of digest.items) {
    if (item._translatedAttempted) continue;
    item._translatedAttempted = true;

    if (isMostlyEnglishText(item.title_ja)) {
      const jaTitle = await translateTextEnToJa(item.title_ja);
      if (jaTitle !== item.title_ja) {
        item.title_ja = jaTitle;
        updated = true;
      }
    }
    if (Array.isArray(item.points)) {
      for (let i = 0; i < item.points.length; i++) {
        if (isMostlyEnglishText(item.points[i])) {
          const jaPt = await translateTextEnToJa(item.points[i]);
          if (jaPt !== item.points[i]) {
            item.points[i] = jaPt;
            updated = true;
          }
        }
      }
    }
  }

  if (updated && currentDigest === digest) {
    renderDigest(digest, false);
  }
}

const PASSWORD_STORAGE_KEY = "morning_ai_site_password";
const DEFAULT_SAMPLE_PASSWORD = "0000";
let pendingRawPayload = null;

// Pure-JS SHA-256 implementation (works on both https:// and local file://)
const SHA256_K = new Uint32Array([
  0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
  0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
  0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
  0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]);

function rotr(n, x) {
  return (x >>> n) | (x << (32 - n));
}

function sha256Bytes(msgBytes) {
  const len = msgBytes.length;
  const bitLenHi = Math.floor((len * 8) / 0x100000000);
  const bitLenLo = (len * 8) >>> 0;
  const padLen = ((len + 9 + 63) & ~63);
  const padded = new Uint8Array(padLen);
  padded.set(msgBytes);
  padded[len] = 0x80;
  const view = new DataView(padded.buffer);
  view.setUint32(padLen - 8, bitLenHi, false);
  view.setUint32(padLen - 4, bitLenLo, false);

  let h0 = 0x6a09e667, h1 = 0xbb67ae85, h2 = 0x3c6ef372, h3 = 0xa54ff53a;
  let h4 = 0x510e527f, h5 = 0x9b05688c, h6 = 0x1f83d9ab, h7 = 0x5be0cd19;
  const w = new Uint32Array(64);

  for (let offset = 0; offset < padLen; offset += 64) {
    for (let i = 0; i < 16; i++) {
      w[i] = view.getUint32(offset + i * 4, false);
    }
    for (let i = 16; i < 64; i++) {
      const s0 = rotr(7, w[i - 15]) ^ rotr(18, w[i - 15]) ^ (w[i - 15] >>> 3);
      const s1 = rotr(17, w[i - 2]) ^ rotr(19, w[i - 2]) ^ (w[i - 2] >>> 10);
      w[i] = (w[i - 16] + s0 + w[i - 7] + s1) >>> 0;
    }
    let a = h0, b = h1, c = h2, d = h3, e = h4, f = h5, g = h6, h = h7;
    for (let i = 0; i < 64; i++) {
      const S1 = rotr(6, e) ^ rotr(11, e) ^ rotr(25, e);
      const ch = (e & f) ^ (~e & g);
      const temp1 = (h + S1 + ch + SHA256_K[i] + w[i]) >>> 0;
      const S0 = rotr(2, a) ^ rotr(13, a) ^ rotr(22, a);
      const maj = (a & b) ^ (a & c) ^ (b & c);
      const temp2 = (S0 + maj) >>> 0;
      h = g; g = f; f = e; e = (d + temp1) >>> 0;
      d = c; c = b; b = a; a = (temp1 + temp2) >>> 0;
    }
    h0 = (h0 + a) >>> 0; h1 = (h1 + b) >>> 0; h2 = (h2 + c) >>> 0; h3 = (h3 + d) >>> 0;
    h4 = (h4 + e) >>> 0; h5 = (h5 + f) >>> 0; h6 = (h6 + g) >>> 0; h7 = (h7 + h) >>> 0;
  }

  const out = new Uint8Array(32);
  const outView = new DataView(out.buffer);
  [h0, h1, h2, h3, h4, h5, h6, h7].forEach((val, idx) => {
    outView.setUint32(idx * 4, val, false);
  });
  return out;
}

function bytesToHex(bytes) {
  return Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

function base64ToBytes(b64) {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) {
    out[i] = bin.charCodeAt(i);
  }
  return out;
}

function concatBytes(...arrays) {
  const total = arrays.reduce((acc, arr) => acc + arr.length, 0);
  const res = new Uint8Array(total);
  let offset = 0;
  for (const arr of arrays) {
    res.set(arr, offset);
    offset += arr.length;
  }
  return res;
}

function tryDecryptOrVerify(rawPayload, password) {
  if (!password) return null;
  if (!rawPayload.encrypted) {
    // 非暗号化の初期サンプルデータは設定パスワード（初期値 0000）で照合
    return password === DEFAULT_SAMPLE_PASSWORD ? rawPayload : null;
  }

  try {
    const salt = base64ToBytes(rawPayload.salt);
    const cipherBytes = base64ToBytes(rawPayload.ciphertext);
    const pwdBytes = new TextEncoder().encode(password);
    const key = sha256Bytes(concatBytes(salt, pwdBytes));

    const plainBytes = new Uint8Array(cipherBytes.length);
    const blockCount = Math.ceil(cipherBytes.length / 32);
    const blkBuf = new Uint8Array(4);
    const blkView = new DataView(blkBuf.buffer);

    for (let blk = 0; blk < blockCount; blk++) {
      blkView.setUint32(0, blk, false);
      const keystream = sha256Bytes(concatBytes(key, blkBuf));
      const start = blk * 32;
      const end = Math.min(start + 32, cipherBytes.length);
      for (let i = start; i < end; i++) {
        plainBytes[i] = cipherBytes[i] ^ keystream[i - start];
      }
    }

    const verifyPrefix = new TextEncoder().encode("VERIFY:");
    const computedTag = bytesToHex(
      sha256Bytes(concatBytes(verifyPrefix, key, plainBytes))
    ).slice(0, 32);

    if (computedTag !== rawPayload.tag) {
      return null;
    }

    const jsonStr = new TextDecoder().decode(plainBytes);
    return JSON.parse(jsonStr);
  } catch {
    return null;
  }
}

function showLockOverlay(showError = false) {
  const overlay = document.getElementById("auth-overlay");
  const mainEl = document.getElementById("app-main");
  const errEl = document.getElementById("auth-error");
  const inputEl = document.getElementById("auth-password-input");

  mainEl.hidden = true;
  overlay.hidden = false;
  errEl.hidden = !showError;
  setTimeout(() => inputEl.focus(), 50);
}

function hideLockOverlay() {
  document.getElementById("auth-overlay").hidden = true;
  document.getElementById("app-main").hidden = false;
  document.getElementById("auth-error").hidden = true;
}

function handlePayloadWithAuth(rawPayload) {
  pendingRawPayload = rawPayload;
  const savedPwd = localStorage.getItem(PASSWORD_STORAGE_KEY) || "";
  const unlocked = tryDecryptOrVerify(rawPayload, savedPwd);
  if (unlocked) {
    hideLockOverlay();
    renderDigest(unlocked);
  } else {
    showLockOverlay(false);
  }
}

function escapeHtml(str) {
  return String(str || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

async function loadDigestByDate(dateStr) {
  try {
    const res = await fetch(`./data/${dateStr}.json`, { cache: "no-cache" });
    if (!res.ok) throw new Error("Failed to fetch digest");
    const data = await res.json();
    handlePayloadWithAuth(data);
  } catch {
    handlePayloadWithAuth(FALLBACK_DIGEST);
  }
}

async function initApp() {
  clearLegacyAutoReadStorage();
  initTheme();
  setupTabsScrollControls();

  // パスワードロック解除フォーム
  const authForm = document.getElementById("auth-form");
  const pwdInput = document.getElementById("auth-password-input");
  authForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const pwd = pwdInput.value.trim();
    if (!pendingRawPayload) return;
    const unlocked = tryDecryptOrVerify(pendingRawPayload, pwd);
    if (unlocked) {
      localStorage.setItem(PASSWORD_STORAGE_KEY, pwd);
      pwdInput.value = "";
      hideLockOverlay();
      renderDigest(unlocked);
    } else {
      showLockOverlay(true);
    }
  });

  // 手動ロックボタン
  const lockBtn = document.getElementById("lock-btn");
  if (lockBtn) {
    lockBtn.addEventListener("click", () => {
      localStorage.removeItem(PASSWORD_STORAGE_KEY);
      showLockOverlay(false);
    });
  }

  // Unread-only filter button
  const unreadBtn = document.getElementById("unread-filter-btn");
  unreadBtn.addEventListener("click", () => {
    unreadOnly = !unreadOnly;
    unreadBtn.classList.toggle("active", unreadOnly);
    unreadBtn.textContent = unreadOnly ? "すべて表示" : "未読のみ";
    if (currentDigest) renderDigest(currentDigest);
  });

  // Reset read status button
  const resetBtn = document.getElementById("reset-read-btn");
  resetBtn.addEventListener("click", () => {
    if (!currentDigest) return;
    saveReadSet(currentDigest.date, new Set());
    renderDigest(currentDigest);
  });

  const selectEl = document.getElementById("date-select");
  try {
    const res = await fetch("./data/index.json", { cache: "no-cache" });
    if (!res.ok) throw new Error("No index.json");
    const indexData = await res.json();
    const dates = indexData.available_dates || [];
    selectEl.innerHTML = dates
      .map((d) => `<option value="${escapeHtml(d)}">${escapeHtml(d)}</option>`)
      .join("");

    selectEl.addEventListener("change", (e) => {
      activeSite = "all";
      loadDigestByDate(e.target.value);
    });

    if (dates.length > 0) {
      await loadDigestByDate(dates[0]);
      return;
    }
  } catch {
    // Fallback for local file:// preview
    selectEl.innerHTML = `<option value="${FALLBACK_DIGEST.date}">${FALLBACK_DIGEST.date}</option>`;
    handlePayloadWithAuth(FALLBACK_DIGEST);
  }
}

document.addEventListener("DOMContentLoaded", initApp);
