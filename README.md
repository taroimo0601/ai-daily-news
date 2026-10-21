# Morning AI Digest（毎朝3分で読めるAIニュース）

完全無料（GitHub Actions + Gemini API 無料枠 + GitHub Pages）で毎朝自動更新される、スマホ特化の自分専用AIニュースサイトです。

## 特徴
- 3ジャンルをバランスよく自動収集
  - 海外公式・大手メディア: OpenAI News, Google AI Blog, TechCrunch AI, The Verge AI
  - 国内トレンド: ITmedia AI+, はてなブックマーク（AI注目記事）
  - 最新注目論文: Hugging Face Daily Papers（上位論文をわかりやすく日本語解説）
- 通勤中・スキマ時間向けの3分構成
  - 全体の30秒トレンドサマリー
  - 重要ニュース8〜10件を厳選し、それぞれ「3行の要点」＋「一言解説（なぜ重要か）」に要約
- スマホで快適に使える機能
  - カテゴリ絞り込みタブ（すべて / 海外 / 国内 / 論文）
  - 記事ごとの「読了チェック」機能（スマホ内に自動保存）
  - ダークモード / ライトモード切り替え
  - 過去の日付のアーカイブ切り替え
  - ホーム画面に追加（PWA対応）でアプリ感覚で起動可能

---

## 完全無料で運用開始する手順（所要時間：約5分）

### ステップ1: Gemini APIキー（無料）の取得
1. Google AI Studio ( https://aistudio.google.com/app/apikey ) にアクセスします。
2. 「Create API key」をクリックし、無料のAPIキーを発行してコピーします。

### ステップ2: GitHubリポジトリの作成とプッシュ
このフォルダ（`ai-daily-news`）をGitHubの新しいリポジトリ（Public推奨：GitHub ActionsとGitHub Pagesが完全無料になります）にプッシュします。

```bash
cd /Users/mizunotarou/Desktop/agy/ai-daily-news
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<あなたのGitHubユーザー名>/ai-daily-news.git
git push -u origin main
```

### ステップ3: GitHubにAPIキーと閲覧パスワードを登録
1. GitHubのリポジトリ画面で `Settings` > 左メニューの `Secrets and variables` > `Actions` を開きます。
2. `New repository secret` ボタンをクリックし、以下の2つを登録します。
   - 1つ目（必須）:
     - Name: `GEMINI_API_KEY`
     - Secret: ステップ1でコピーしたGemini APIキー
   - 2つ目（自分専用の閲覧パスワード）:
     - Name: `SITE_PASSWORD`
     - Secret: あなたが決めた任意のパスワード（未設定の場合は初期値 `0000` になります）

### ステップ4: GitHub Pagesの有効化
1. リポジトリの `Settings` > 左メニューの `Pages` を開きます。
2. Build and deployment の Source で `Deploy from a branch` を選択します。
3. Branch で `main`、フォルダで `/docs` を選択して `Save` を押します。
4. 1〜2分ほど待つと、`https://<あなたのGitHubユーザー名>.github.io/ai-daily-news/` でサイトが公開されます。

### ステップ5: 初回テスト実行とスマホ登録
1. リポジトリ上部の `Actions` タブを開きます。
2. 左側の `Generate Morning AI Digest` をクリックし、右側の `Run workflow` ボタンを押すと、今すぐ最新ニュースの収集と要約が実行されます。
3. スマホのブラウザ（Safari / Chrome）で公開されたURLを開き、「ホーム画面に追加」をしておくと、毎朝ワンタップで読めるようになります。
