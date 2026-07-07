<div align="center">

# DeepPaperNote

**把一篇難讀的論文，變成一份真正值得保留的 Obsidian 深度筆記。**

[English](./README.md) | [簡體中文](./README.zh-CN.md)

[![主頁](https://img.shields.io/badge/%E4%B8%BB%E9%A1%B5-online-2563eb)](https://917dhj.github.io/DeepPaperNote/)
[![狀態](https://img.shields.io/badge/status-stable-16a34a)](https://github.com/917Dhj/DeepPaperNote)
[![版本](https://img.shields.io/github/v/release/917Dhj/DeepPaperNote?display_name=tag&color=0f766e)](https://github.com/917Dhj/DeepPaperNote/releases/tag/v2.0.0)
[![許可證](https://img.shields.io/badge/license-MIT-c9a227)](./LICENSE)
[![Agents](https://img.shields.io/badge/agents-Claude%20Code%20%2B%20Codex-7c3aed)](./SKILL.md)
[![輸出](https://img.shields.io/badge/output-Obsidian-16a34a)](./references/obsidian-format.md)
[![圖表](https://img.shields.io/badge/figures-image--first-f59e0b)](./references/figure-placement.md)
[![寫作](https://img.shields.io/badge/writing-model--first-7c3aed)](./references/model-synthesis.md)
[![更新日誌](https://img.shields.io/badge/changelog-latest-0f766e)](./CHANGELOG.md)

</div>

[![DeepPaperNote 主圖](./assets/hero-academic.svg)](https://917dhj.github.io/DeepPaperNote/)

**你是否經常遇到這種情況：準備精讀一篇經典論文時，最累的往往不是看，而是整理成筆記**。真正耗時間的，通常是這些環節：

- 在 PDF、Zotero、網頁和筆記軟體之間來回切換
- 手動整理元資料、摘要、圖表和方法主線
- 明明已經讀懂了一部分，卻還要花很多時間把它寫成結構化筆記
- 最後留下的仍然只是一篇“看起來完整，但以後未必還想回看”的筆記

DeepPaperNote 想解決的，就是這一層重複、機械、但又非常耗時的工作。它會先把整理、結構化、圖表定位和筆記成形這些環節做掉，讓你把精力留給真正的思考。

DeepPaperNote 是一個面向**論文深度閱讀**的技能，同一套核心能力可以執行在 Claude Code 和 Codex 上。它更關注：

- 論文到底在解決什麼問題
- 方法機制是怎麼工作的
- 關鍵公式、實驗結論和圖表資訊是否被保留下來
- 最終能不能沉澱成一份**適合長期積累的 Obsidian 筆記**

> [!tip]
> 如果你已經有自己的 Obsidian / Zotero 工作流，DeepPaperNote 會把最耗時、最容易出錯的取證、整理和成稿環節自動化。

## 🎯 它幫你解決什麼問題？

![DeepPaperNote usage example](./assets/usage-example.png)

| 🎯 你的需求 / 痛點 | ✅ DeepPaperNote 怎麼幫你 |
| --- | --- |
| 想快速讀懂一篇很難啃的複雜論文 | 自動整理方法主線、關鍵結果、圖表上下文和侷限，產生能直接閱讀的深度筆記 |
| 想精讀一篇經典論文，但不想手寫很多機械筆記 | 自動完成元資料整理、結構搭建、圖表佔位和正文筆記產生，專注於真正有價值的理解 |
| 想把論文真正沉澱進 Obsidian | 會結合論文領域自動歸檔到合適的 Obsidian 目錄，再產生論文同名資料夾、Markdown 筆記和 `images/` 目錄 |
| 已經在 Zotero 裡管理文獻，不想重複折騰 | 可優先複用本地論文庫和附件，減少誤匹配，也通常更快 |
| 不想只得到一篇“漂亮摘要” | 更強調機制拆解、關鍵數字、公式、邊界條件和真實侷限 |

## ✨ 它是怎麼做到的？

DeepPaperNote 不是靠“把摘要重新措辭一遍”來顯得更完整，而是靠下面這幾條工作流原則，把筆記品質往上抬：

| 🧭 核心原則 | 📝 具體體現 |
| --- | --- |
| 🤖 模型主導理解 | 真正負責機制拆解、方法主線、關鍵比較和侷限分析的是模型，而不是模板化摘要。 |
| 🗂️ 證據優先 | 先從 PDF、元資料和可選的 Zotero 工作流裡取證，再基於證據寫作。筆記會梳理完整的證據鏈：論文證明了什麼、什麼尚未被證明、哪些實驗最重要、負面或限制性結果在哪裡、結論的邊界在哪裡。 |
| 🧪 技術細節優先 | 對技術論文，會盡量保留關鍵數字、公式、實現邏輯和真實邊界條件，而不是停在高層概括。 |
| 📄 按論文型別自適應寫作 | 不同型別的論文有不同的閱讀策略。方法論文、基準測試論文、資料集論文、綜述論文和實證論文，各自會針對該型別最關鍵的方面做重點處理。 |
| 📊 結果表格更清楚 | 當論文涉及多個模型、資料集、任務、設定或指標時，DeepPaperNote 會把核心比較整理成緊湊的 Markdown 表格，並在表格後解釋這些數字到底說明瞭什麼，方便掃讀和後續複用。 |
| 🖼️ 影像優先插入 | 當圖表候選可用、路徑有效時，直接插入為真實圖片。佔位符只保留給真實問題：候選缺失、視覺缺陷、汙染、截斷或身份不符。 |
| 🔗 原生沉澱到知識庫 | 會先按論文領域歸檔到現有知識庫結構，再為每篇論文產生獨立資料夾、帶 YAML properties 和固定`核心資訊`元資料塊的 Markdown 筆記、穩定的 `images/` 目錄，以及更乾淨的圖表嵌入。 |
| 📚 本地文獻優先 | 如果論文已經在 Zotero 裡，優先複用本地條目和附件，通常更穩，也往往更快。 |

**一句話說：**

> DeepPaperNote 更像一個“論文讀書筆記產生工作流”，而不是“論文摘要總結器”。

## 👀 它更適合誰

<table>
  <tr>
    <td valign="top" width="33%">
      <strong>👓 啃硬核論文、精讀經典論文的人</strong><br><br>
      你讀的不是掃一眼摘要就結束的論文，而是公式多、架構複雜、實驗設計繞、值得反覆回看的論文。你需要的不是一篇“漂亮總結”，而是一份能幫你把方法主線、關鍵結果和圖表結構真正理清楚的筆記。
    </td>
    <td valign="top" width="33%">
      <strong>🗂️ 用 Obsidian 做長期知識沉澱的人</strong><br><br>
      你希望論文筆記不是一次性消費品，而是能長期回看、連結、複用的知識資產。DeepPaperNote 會結合論文領域歸檔到更合適的位置，再產生 Markdown 筆記和 <code>images/</code> 資料夾，讓沉澱這件事更順手。
    </td>
    <td valign="top" width="33%">
      <strong>🤖 不滿足於 AI 摘要總結的人</strong><br><br>
      你不是隻想看一段“看起來很完整”的摘要，而是想知道：這篇論文到底解決了什麼、方法是怎麼工作的、哪些結果最重要、哪裡最容易被誤讀。DeepPaperNote 更接近研究筆記，而不是摘要產生器。
    </td>
  </tr>
</table>

## 🚀 快速上手

### 1) 將 DeepPaperNote 安裝到你的 agent 技能目錄

DeepPaperNote 同時支援 Claude Code 和 Codex。

#### npx Skills（推薦）

大多數情況下，可以直接用 npx 安裝。在終端執行：

```bash
npx skills add 917Dhj/DeepPaperNote
```

此命令會預設安裝到共享的`.agents/skills`目錄，這個目錄中的 skill 可以被 Codex 等大部分 agent 識別並使用。如果你也想在 Claude Code 裡使用，在 **Additional agents** 提示中選擇 Claude Code即可。

你也可以直接指定安裝給某個 agent：

```bash
npx skills add 917Dhj/DeepPaperNote -a codex
npx skills add 917Dhj/DeepPaperNote -a claude-code
```

##### 更新

如果要更新已有的 DeepPaperNote 版本，重新執行 npx 安裝命令即可；它會替換目標 skills 目錄中的現有版本。

#### 手動安裝

如果你更習慣手動安裝，推薦去 [release](https://github.com/917Dhj/DeepPaperNote/releases) 頁面下載最新版本的 zip 包並解壓。

Codex 使用者可以把解壓出來的 `DeepPaperNote` 資料夾放到：

```bash
~/.codex/skills/DeepPaperNote
```

Claude Code 使用者可以把解壓出來的 `DeepPaperNote` 資料夾放到：

```bash
~/.claude/skills/DeepPaperNote
```

也可以直接 `git clone`：

```bash
git clone https://github.com/917Dhj/DeepPaperNote.git ~/.codex/skills/DeepPaperNote
git clone https://github.com/917Dhj/DeepPaperNote.git ~/.claude/skills/DeepPaperNote
```

安裝完成後，重啟你的 agent 讓技能生效。

### 2) 安裝核心 Python 依賴

在正式處理論文前，需要安裝最核心的 Python 依賴：

```bash
python3 -m pip install PyMuPDF
```

為什麼這一步很重要：

- DeepPaperNote 讀取 PDF 主要依賴 `PyMuPDF`
- 如果沒裝 `PyMuPDF`，最核心的 PDF 抽取流程就跑不起來

### 3) 直接開始使用

接下來你只需要把論文丟給 agent 就行，標題、DOI、URL、本地 PDF 都可以，你可以直接給出類似這樣的指令：

- 💬 `給這篇論文產生深度筆記：Attention Is All You Need`
- 💬 `把這篇文章整理成 Obsidian 筆記：https://arxiv.org/abs/1706.03762`
- 💬 `幫我精讀一下這篇 PDF，產生帶圖表的 Markdown`
- 💬 `請用 DeepPaperNote 處理這篇論文：10.48550/arXiv.1706.03762`

預設情況下，DeepPaperNote 會產生**繁體中文、臺灣用語**的筆記。當前寫作規範和格式校驗也主要圍繞這一輸出目標建構；目前繁體中文是唯一能夠發揮 skill 完全能力的筆記語言，如需產生英文版筆記，請期待後續更新。

預設情況下，DeepPaperNote 會自己完成：

- 精準識別論文身份
- 獲取 PDF、元資料和正文證據
- 圖表候選可用時直接插入真實圖片；只有候選缺失、視覺缺陷或寫入失敗等真實問題才保留佔位符
- 產生最終 Markdown 筆記
- 自動寫入 Obsidian；如果沒有配置 Obsidian，則會先詢問你是否有庫路徑，再決定是否降級輸出到當前工作區的輸出目錄

### 4) 首次使用不必追求完整配置

如果你還沒有完整配置 Obsidian / Zotero / OCR，也可以先試跑。

如果你要在本地開發、跑測試或 lint，可以安裝開發依賴：

```bash
python3 -m pip install -e '.[dev]'
```

如果你想先檢查環境，也可以直接對 agent 說：

- 💬 `請幫我檢查這臺機器上的 DeepPaperNote 是否已經準備好`
- 💬 `檢視 deeppapernote 的可用情況`
- 💬 `deeppapernote 有什麼功能`

## 🔧 配置指南（開箱即用，按需進階）

**如果你已經安裝好了 PyMuPDF，那麼你就可以直接開始使用 DeepPaperNote 產生筆記了**。以下介紹的配置都是核心功能的擴充套件，讓你能夠將 DeepPaperNote 產生的筆記真正融入你的科研工作流中。

- 如果你沒有配置 Obsidian，它也能把筆記輸出到當前工作區下的回退輸出目錄，預設是 `DeepPaperNote_output`。
- 但如果你想要更好的長期管理體驗，還是強烈建議配置你的 Obsidian 庫路徑。

### 📍 核心配置：指定你的 Obsidian 庫

```bash
export DEEPPAPERNOTE_OBSIDIAN_VAULT="/你的/Obsidian_Documents/絕對路徑"
```

如果你希望 agent 在之後的新終端會話裡也一直讀到這個預設配置：

- 在 macOS / Linux 上，建議把它寫進 `~/.zshrc` 之類的 shell 配置檔案，然後重新載入 shell 或重啟 agent：

```bash
echo 'export DEEPPAPERNOTE_OBSIDIAN_VAULT="/你的/Obsidian_Documents/絕對路徑"' >> ~/.zshrc
source ~/.zshrc
```

- 在 Windows PowerShell 上，可以把它持久化成使用者環境變數，然後重新開啟終端：

```powershell
setx DEEPPAPERNOTE_OBSIDIAN_VAULT "C:\Users\YourName\Documents\Obsidian_Documents"
```

<details>
<summary><strong>🛠️ 展開檢視更多進階配置（目錄自定義 / Zotero / Semantic Scholar / OCR）</strong></summary>

### 目錄相關配置

如果你希望自定義論文目錄或中間產物目錄，也可以再加：

```bash
export DEEPPAPERNOTE_PAPERS_DIR="Research/Papers"
export DEEPPAPERNOTE_OUTPUT_DIR="tmp/DeepPaperNote"
```

| ⚙️ 變數 | 是否必需 | 📝 作用 |
| --- | --- | --- |
| `DEEPPAPERNOTE_OBSIDIAN_VAULT` | **推薦** | **你的 Obsidian 庫根目錄** |
| `DEEPPAPERNOTE_PAPERS_DIR` | 可選 | Obsidian 庫內論文輸出目錄，預設是 `Research/Papers` |
| `DEEPPAPERNOTE_OUTPUT_DIR` | 可選 | 本地臨時產物目錄，預設是 `tmp/DeepPaperNote` |
| `DEEPPAPERNOTE_WORKSPACE_OUTPUT_DIR` | 可選 | 當沒有配置 Obsidian 庫時，當前工作區下的自動降級輸出目錄，預設是 `DeepPaperNote_output` |

如果你希望 agent 後續一直預設使用這些值：

- 在 macOS / Linux 上，也建議把它們寫進 `~/.zshrc`：

```bash
echo 'export DEEPPAPERNOTE_PAPERS_DIR="Research/Papers"' >> ~/.zshrc
source ~/.zshrc
```

- 在 Windows PowerShell 上，可以把它們持久化成使用者環境變數：

```powershell
setx DEEPPAPERNOTE_PAPERS_DIR "Research/Papers"
```

這些可選路徑配置的實際好處是：

- `DEEPPAPERNOTE_PAPERS_DIR`
  如果你的 Obsidian 庫不是把論文放在 `Research/Papers` 下，或者你已經有自己的目錄約定，這個配置可以讓 DeepPaperNote 直接適配你的現有結構，減少後續手動移動檔案。
- `DEEPPAPERNOTE_OUTPUT_DIR`
  如果你希望中間產物統一落在一個固定位置，方便除錯、清理或做實驗，這個配置會比較有用。

領域路由由 `references/domain_rules.yaml` 中的可編輯分類表控制。DeepPaperNote 會先判斷應用領域，再回退到方法領域；只有標題或摘要能提供相對保守的證據時，才會複用已有的 Obsidian 一級領域目錄。

### 可選：用於本地文獻庫優先工作流的 Zotero

DeepPaperNote 不依賴 Zotero 才能工作。
但如果你本來就用 Zotero 做文獻管理，配置一個你的 agent 真的能用的 Zotero 整合會很值。

它最適合這樣的人：
- 你本來就用 Zotero 做文獻管理
- 你平時主要在 Zotero 裡讀論文、整理附件和元資料

可以這樣理解不同路線：

| 🧩 方案 | 🎯 更適合什麼場景 | 📝 說明 |
| --- | --- | --- |
| [kujenga/zotero-mcp](https://github.com/kujenga/zotero-mcp) | 輕量的只讀訪問 | 更接近一個最小化 Zotero MCP 服務，適合搜尋條目、讀元資料、讀文字，但通常仍需要你自己做一點適配 |
| [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) | 更完整的研究工作流能力 | 功能更豐富，但穩定接進你的 agent 環境時通常也需要額外改造 |

為什麼值得配：

- 本地 Zotero 命中通常是最可靠的論文身份錨點
- 如果論文已經在你的本地 Zotero 庫裡，DeepPaperNote 往往可以直接複用本地條目和附件資訊，不必再重新聯網搜尋和下載，因此產生速度通常也會更快
- agent 可以先查你的本地論文庫，再決定要不要聯網
- 本地附件也更有助於減少標題誤匹配
- 如果你本來就用 Zotero 做論文管理，這會比重新去網上“猜測這篇論文是誰”穩得多
- 對正式發表版、預印本、映象頁面標題相似的場景，Zotero 優先通常會明顯降低誤匹配機率

⚠️需要特別說明的是：

- DeepPaperNote **不強依賴某一個固定的 Zotero 整合倉庫**
- 對 DeepPaperNote 來說，需要的關鍵能力是：讓 agent 能搜尋 Zotero 條目、檢視元資料、最好還能讀取本地 PDF 附件
- 上面提到的兩條路線目前都**不一定是即插即用方案**，如果你想穩定使用，通常還需要自己做一層適配或改造

### 可選：Semantic Scholar API Key

這不是必需項，但如果你有 Semantic Scholar API key，可以設定：

```bash
export DEEPPAPERNOTE_SEMANTIC_SCHOLAR_API_KEY="your_api_key"
```

它的好處主要是：

- 元資料補全通常會更穩一些
- 對一些標題不好匹配的論文，身份解析會更可靠
- 在作者、venue、摘要等資訊回填上，有時會更完整
- 它能給 DeepPaperNote 多一個較強的元資料來源，減少退回到弱匹配的機率

### 可選：OCR 工具

很多現代 PDF 並不需要 OCR。
但如果論文是下面這些情況，OCR 會很有幫助：

- 掃描版 PDF
- 以圖片為主、嵌入文字品質很差的 PDF
- 一些比較老的論文，直接抽文字時內容殘缺

DeepPaperNote 當前的 OCR 使用邏輯是：

- 先用 `PyMuPDF` 做正常的 PDF 文字提取
- 對每一頁統計可搜尋文字的字元數
- 如果某一頁直接抽到的文字太少，就把這頁視為 OCR 回退候選
- 只對這類頁面單獨做 OCR
- OCR 還原出的文字，主要用於補頁級證據和後續圖表/頁面語義匹配的上下文

需要特別說明的是：

- OCR 目前只是 **頁文字兜底方案**
- 它 **不是** 所有 PDF 的主提取路徑
- 它 **不會** 代替模型去理解論文
- 它 **不會** 直接負責“理解圖片內容”

如果沒有 OCR，DeepPaperNote 處理普通數字版 PDF 依然沒問題。面對掃描版或低品質 PDF 時，如果抽取到的證據不足以支撐真正的深度筆記，流程應該要求補充 OCR 或更好的來源，而不是完成一篇低品質輸出。

OCR 需要的依賴如下：

| 🧱 層級 | 📦 依賴 | 📝 作用 |
| --- | --- | --- |
| 系統工具 | `tesseract` | 真正執行 OCR 識別 |
| Python 包 | `pytesseract` | Python 呼叫 `tesseract` 的橋接層 |
| Python 包 | `Pillow` | 開啟頁面渲染後的影像再交給 OCR |

在 macOS 上的安裝方式：

```bash
brew install tesseract
python3 -m pip install --user pytesseract Pillow
```

在 Windows 上，可以用下面這種方式：

```powershell
winget install UB-Mannheim.TesseractOCR
py -m pip install --user pytesseract Pillow
```

如果 `winget` 不可用，也可以手動安裝 `Tesseract OCR`，再執行：

```powershell
py -m pip install --user pytesseract Pillow
```

快速驗證：

```bash
tesseract --version
python3 -c "import pytesseract, PIL; print('python_ok')"
python3 -c "import pytesseract; print(pytesseract.get_tesseract_version())"
```

</details>

## 📝 更新日誌概覽

更完整的版本級更新請見 [CHANGELOG.md](./CHANGELOG.md)。

| 🏷️ 版本 | 🚦 狀態 | ✨ 主要內容 |
| --- | --- | --- |
| v2.0.0 | ✅ 已發布 | 大版本升級：更深的證據優先筆記、原文級 grounding、按論文型別自適應寫作，以及更可靠的圖表處理 |
| v1.1.1 | ✅ 已發布 | Patch 小更新：收緊圖表佔位格式校驗和表格裁圖品質檢查 |
| v1.1.0 | ✅ 已發布 | 圖表提取品質升級：新增基於圖注的整頁區域裁剪、視覺品質門禁，並保持影像候選佔位優先 |
| v1.0.1 | ✅ 已發布 | 一個 patch 版本：補充 Obsidian 原生 frontmatter 格式支援，修復 lint 相容性問題，並清理 README 中未使用的資源圖片 |
| v1.0.0 | ✅ 已發布 | 第一個穩定版：採用純 skill 結構，支援 Claude Code、Codex、Cursor、Copilot、Gemini CLI 以及其他相容 Agent Skills 的環境 |
| v0.3.1-alpha | ✅ 已發布 | 預設 Obsidian 論文根目錄改為 `Research/Papers`，執行時路徑解析和寫入行為也同步對齊到這個新位置 |
| v0.3.0-alpha | ✅ 已發布 | 一次較大的品質升級：新增固定創新點章節、顯式機制流程、更強的整條 workflow 約束、最終可讀性品質檢查、公式語法檢查，以及新的 `原文摘要翻譯` 前置區塊 |
| v0.2.0-alpha | ✅ 已發布 | 重現級技術筆記寫作升級：顯式 `note_plan`、公式感知輸出、更強的最終自檢、摘要中英雙寫，以及更嚴格的格式校驗 |
| v0.1.0-alpha | ✅ 已發布 | 第一個公開 alpha 版：綜合證據包流程、Zotero 優先輔助能力、佔位優先圖表處理、工作區回退輸出、OCR 回退、測試與 CI |
| 未發布 | 🕒 暫無新的 release 級變化 | 當前還沒有下一版 release 的公開更新內容，最新版本為 v2.0.0 |

## ⚙️ 工作流

預設流程是：

1. 解析論文身份
2. 收集元資料
3. 獲取最佳可用 PDF
4. 抽取完整原文與 source manifest
5. 抽取結構化索引和 PDF 影像資產
6. 規劃圖表位置
7. 建構全量圖表決策表
8. 建構 manifest synthesis bundle
9. 讓模型讀取 raw sections 並規劃筆記
10. 對 note_plan 執行 grounding lint
11. 讓模型寫筆記
12. 校驗最終筆記
13. 做最終內容品質複核
14. 做最終可讀性複核
15. 寫入 Obsidian

核心原則：

- 指令碼負責原文、元資料、資產和品質訊號
- 模型負責寫作
- 格式校驗、最終內容品質複核和最終可讀性複核在寫入前兜底

相關文件：

- [工作流](./references/workflow.md)
- [架構](./references/architecture.md)
- [模型綜合寫作](./references/model-synthesis.md)

## 🖼️ 圖表策略

DeepPaperNote 把”圖片是否插入”和”是否保留佔位”當作兩個獨立問題來處理。

當圖表候選可用時——裁圖視覺品質合格、能確認是目標圖表、圖片路徑有效——直接插入為真實圖片嵌入。

佔位符只保留給真實問題：

- 沒有可用的圖表候選
- 裁圖有視覺缺陷、截斷或汙染
- 無法確認圖片與目標圖表匹配
- 檔案複製或寫入失敗

當確實需要佔位時，DeepPaperNote 會保留語義位置、說明和上下文，讓筆記結構不斷掉，也讓你知道這個位置原本對應什麼圖：

```md
> [!figure] Fig. 3 資料分佈與品質評估
> 建議位置：資料與任務定義
> 放置原因：這張圖同時展示樣本構成、對話長度統計和專家品質檢查結果，是理解 `PsyInterview` 資料邊界最重要的圖之一。
> 當前狀態：保留佔位；當前提取結果只拿到區域性子圖，無法穩定還原成可獨立解釋的完整原圖。
```

詳見 [圖表放置規則](./references/figure-placement.md)。

## ✅ 品質標準

DeepPaperNote 對“什麼算一篇合格筆記”有明確門檻。

最終筆記應該：

- 區分研究問題和任務定義
- 講清楚真正的方法或分析流程
- 抓住真正重要的關鍵數字
- 覆蓋關鍵的實驗設定和條件
- 區分證據實際證明了什麼和尚未證明什麼
- 指出哪些地方最容易被誤讀
- 至少寫出一個真實侷限，並給出邊界約束
- 至少包含一個可複用的研究或工程 takeaway
- 使用真實標題層級：`#`、`##`、`###`
- 避免正文出現半中半英的句子

如果證據品質不夠，就應該降級或直接失敗，而不是假裝完成了深度精讀。

相關文件：

- [證據優先](./references/evidence-first.md)
- [深度分析](./references/deep-analysis.md)
- [最終寫作](./references/final-writing.md)
- [筆記品質標準](./references/note-quality.md)

## 🗂️ 倉庫結構

```text
DeepPaperNote/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── agents/
│   └── openai.yaml
├── assets/
│   ├── hero-academic.svg
│   ├── usage-example.png
│   └── note_template.md
├── references/
│   ├── architecture.md
│   ├── deep-analysis.md
│   ├── domain_rules.yaml
│   ├── evidence-first.md
│   ├── figure-placement.md
│   ├── final-writing.md
│   ├── metadata-sources.md
│   ├── model-synthesis.md
│   ├── note-quality.md
│   ├── obsidian-format.md
│   ├── paper-types.md
│   └── workflow.md
└── scripts/
    ├── build_synthesis_bundle.py
    ├── check_environment.py
    ├── citation_links.py
    ├── collect_metadata.py
    ├── common.py
    ├── contracts.py
    ├── create_input_record.py
    ├── extract_evidence.py
    ├── extract_pdf_assets.py
    ├── extract_source_text.py
    ├── fetch_pdf.py
    ├── lint_grounding.py
    ├── lint_note.py
    ├── locate_zotero_attachment.py
    ├── materialize_figure_asset.py
    ├── plan_figure_table_decisions.py
    ├── plan_figures.py
    ├── resolve_paper.py
    ├── run_pipeline.py
    └── write_obsidian_note.py
```

## 🧰 推薦環境

| 🧰 元件 | 🚦 狀態 | 📝 說明 |
| --- | --- | --- |
| Claude Code / Codex | 推薦 | 支援的 agent 環境 |
| Python 3.10+ | 必需 | 執行輔助指令碼 |
| PyMuPDF | 必需 | 核心 PDF 依賴，可用 `python3 -m pip install PyMuPDF` 安裝 |
| 本地 Obsidian 庫 | 推薦 | 配好後可直接寫入長期筆記體系；未配置時使用當前工作區下的回退輸出目錄 |
| Zotero 整合 | 可選 | 對本地論文庫工作流很有幫助 |
| OCR 工具 | 可選 | 對掃描版 PDF 更友好 |

## 🧭 設計原則

DeepPaperNote 背後的基本判斷很簡單：

1. **好的論文筆記，不等於段落式摘要**

真正有價值的筆記，應該幫助你理解：

- 方法怎麼工作
- 證據在哪裡
- 實驗說明瞭什麼
- 有哪些邊界與侷限

2. **論文的閱讀目標，是沉澱的可複用資產**

不是當下“懂了一點”，而是未來還能回看、能引用、能接著研究。

3. **筆記產生應該服務真實研究工作流**

所以它更貼近：

- Obsidian
- Zotero
- 本地論文管理
- 長期知識庫建構和管理

## 🧭 致謝與靈感

DeepPaperNote 在工作流設計上受到了這些論文閱讀 / 筆記產生專案的啟發：

- [heleninsights-dot/phd-deepread-workflow](https://github.com/heleninsights-dot/phd-deepread-workflow)
- [juliye2025/evil-read-arxiv](https://github.com/juliye2025/evil-read-arxiv)

## 🤝 貢獻說明

DeepPaperNote 的開發分支是 `develop`。請把 PR 提交到 `develop` 分支，而不是 `main`。

如果改動可能影響最終筆記品質，請按照 `evals/` 中定義的評估流程和品質標準驗證：

- [`evals/regression-workflow-zh.md`](./evals/regression-workflow-zh.md)
- [`evals/note-quality-rubric.md`](./evals/note-quality-rubric.md)

對於和筆記品質相關的 PR，我只會接受在評估流程下能證明最終筆記品質有實際提升的改動。單純的格式更整潔、內部抽象更多，或者程式碼結構調整，本身不算筆記品質提升，除非它們最終確實改善了產生出來的筆記。

## Star History

<a href="https://www.star-history.com/?repos=917Dhj%2FDeepPaperNote&type=date&legend=top-left">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://api.star-history.com/image?repos=917Dhj/DeepPaperNote&type=date&theme=dark&legend=top-left"
    />
    <source
      media="(prefers-color-scheme: light)"
      srcset="https://api.star-history.com/image?repos=917Dhj/DeepPaperNote&type=date&legend=top-left"
    />
    <img
      alt="Star History Chart"
      src="https://api.star-history.com/image?repos=917Dhj/DeepPaperNote&type=date&legend=top-left"
    />
  </picture>
</a>

<p align="center">
  <em>感謝你閱讀、使用和支援 DeepPaperNote。願你的每一次論文精讀，都更清晰、更從容，也更有收穫。</em>
</p>

<p align="center">
  <a href="./LICENSE">MIT License</a> &copy; <a href="https://github.com/917Dhj">917Dhj</a>
</p>
