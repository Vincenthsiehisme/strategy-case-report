# Visual Reference 系統

> 此文件由 SKILL.md Phase 6.5（Visual Brief）引用。  
> 輸出形式：HTML artifact 可視化 deck。  
> 目標：在 Phase 7 開始製作頁面前，鎖定整份報告的視覺系統，確保每頁風格一致、有主張、不飄移。  
> **本文件只處理視覺 ref（設計錨點用）。論證型配圖執行規則見 `references/writing-rules.md`。**

## 目錄
1. [執行時機](#執行時機)
2. [Phase 6.5 執行流程](#phase-65-visual-brief-執行流程)
   - Step 1：案例特性萃取
   - Step 2：視覺系統決策（色彩 / 字體 / 版型 / 動態）
   - Step 3：Visual Brief 輸出格式
3. [視覺 Ref 搜圖規則](#視覺-ref-搜圖規則)
4. [視覺 Ref 與論證型配圖的分工邊界](#視覺-ref-與論證型配圖的分工邊界)

---

## 執行時機

**Phase 6 批判確認完成後、Phase 7 開始前，插入 Phase 6.5：Visual Brief。**

這不是可選步驟。視覺系統必須在內容進入 HTML 製作前鎖定。  
Visual Brief 輸出後，等使用者確認或微調，確認後才能進 Phase 7。

**精簡版 Visual Brief 的觸發條件：Sprint Mode。**  
Sprint Mode 只需完成色彩系統與字體配對兩個維度，版型節奏和動態節奏在製作時即時決定。  
即使使用者說「直接開始做」，仍須先確認色彩與字體，才能保證視覺一致性。

---

## Phase 6.5｜Visual Brief 執行流程

### Step 1｜案例特性萃取（決策輸入）

從已完成的分析內容中，萃取以下四個維度的方向輸入。  
這些不是憑空選擇，而是從案例本身的特性推導出來的：

| 維度 | 要問的問題 | 輸出 |
|------|----------|------|
| 產業調性 | 這個案例的品牌屬於哪個象限？（奢華 / 大眾 / 專業 / 親民） | 一個形容詞 |
| 情緒基調 | 這份報告讀完應該讓人感覺到什麼？（銳利 / 沉穩 / 張力 / 優雅） | 一個形容詞 |
| 讀者身份 | 這份報告的主要讀者是誰？（策略長 / 客戶高層 / 內部團隊） | 一個身份標籤 |
| 報告主張 | 這份報告整體想說的核心判斷是什麼？ | 一句話 |

這四個維度的組合，決定後續所有視覺選擇的方向。

**從四個維度合成視覺主張句（用於 Visual Brief 的「情緒基調」欄）：**
格式：「這是一份給 [讀者身份] 看的報告，視覺語言要傳遞 [情緒基調形容詞] 的感受，對應 [產業調性形容詞] 的品牌調性，核心主張是 [報告主張]。」

例如：「這是一份給策略長看的報告，視覺語言要傳遞銳利的感受，對應專業的品牌調性，核心主張是品牌在做的事比它說的話更值得被看見。」

這句話是後續色彩、字體、版型決策的統一錨點，每次做視覺決策時都對照這句話。

---

### Step 2｜視覺系統決策（四個維度）

#### 維度 A｜色彩系統

**決策邏輯：**

先確定主色調的「溫度」與「重量」：
- 案例品牌屬奢華 / 專業類 → 偏深色背景（深炭 / 深藍 / 深綠），亮色文字
- 案例品牌屬大眾 / 親民類 → 偏淺色背景，有重量感的深色文字
- 報告情緒偏銳利張力 → 高對比配色，accent 色要刺眼
- 報告情緒偏沉穩優雅 → 低對比主色，accent 色克制但精準

**色彩結構（每份報告必須定義以下五個）：**

```css
:root {
  --bg-primary: #______;      /* 主背景色，覆蓋 60-70% 視覺面積 */
  --bg-secondary: #______;    /* 次要背景，用於區塊分隔或卡片底色 */
  --text-primary: #______;    /* 主文字色 */
  --text-secondary: #______;  /* 次要文字色，用於說明文字、標注 */
  --accent: #______;          /* 強調色，用於關鍵判斷句、圖表亮點、頁碼 */
}
```

**禁止：**
- 不用紫色漸層配白底（過度使用的 AI 美學）
- 不用 5 個以上的顏色
- accent 色不能超過總視覺面積的 10%
- 不在同一份報告裡混用暖色調和冷色調主色

**搜圖方向（用於確認色彩方向感）：**
搜尋 `editorial magazine color palette [產業形容詞]` 或 `strategy deck dark minimal [情緒形容詞]`，找 2–3 張視覺參考確認色彩方向，搜到後通過證據檢查（見下方），才作為參考錨點。

---

#### 維度 B｜字體系統

**決策邏輯：**

HTML artifact 使用 Google Fonts CDN，字體選擇遵循以下原則：

- **Display 字體**（用於頁面大標題、statement page）：選有個性的襯線體或幾何無襯線體，避免 Inter、Roboto、Arial
- **Body 字體**（用於內文、說明、標注）：選可讀性強的無襯線體，與 Display 字體形成對比

**推薦字體配對（依情緒基調）：**

| 情緒基調 | HTML Display | HTML Body | 特質 |
|---------|------------|---------|------|
| 銳利張力 | Bebas Neue / Barlow Condensed | DM Sans | 壓縮感、力道強 |
| 沉穩優雅 | Playfair Display / Cormorant | Lato | 古典感、有重量 |
| 專業精準 | Syne / Epilogue | Source Sans 3 | 現代感、乾淨 |
| 高冷奢華 | Bodoni Moda / Libre Baskerville | Raleway | 時尚感、留白多 |

**PPTX 字體對照表（HTML Google Fonts 無法在 PPTX 使用，改用以下系統字體）：**

| 情緒基調 | PPTX Header 字體 | PPTX Body 字體 | 說明 |
|---------|----------------|--------------|------|
| 銳利張力 | Impact | Calibri | 壓縮感保留，力道最強 |
| 沉穩優雅 | Georgia | Calibri Light | 最接近 Playfair 的古典感 |
| 專業精準 | Trebuchet MS | Calibri | 現代感、乾淨 |
| 高冷奢華 | Palatino Linotype | Calibri | 最接近 Bodoni 的優雅感 |

**HTML 字體層級結構：**

```css
/* Display — 頁面主標題，statement page 大字 */
font-family: '[Display字體]', serif;
font-size: clamp(2.5rem, 6vw, 5rem);
font-weight: 700;
letter-spacing: -0.02em;

/* Heading — 分析頁小標、模型標題 */
font-family: '[Body字體]', sans-serif;
font-size: clamp(1rem, 2vw, 1.4rem);
font-weight: 600;
letter-spacing: 0.08em;
text-transform: uppercase;

/* Body — 內文段落 */
font-family: '[Body字體]', sans-serif;
font-size: clamp(0.85rem, 1.5vw, 1rem);
line-height: 1.7;

/* Caption — 來源標注、圖說、頁碼 */
font-family: '[Body字體]', sans-serif;
font-size: 0.7rem;
letter-spacing: 0.12em;
opacity: 0.5;
```

**PPTX 字體大小規範（pptxGenJS 使用 pt 單位）：**

| 層級 | 用途 | 大小 | 樣式 |
|------|------|------|------|
| Display | 投影片主標題、statement slide 大字 | 40pt | bold |
| Heading | 分析頁小標、模型標題 | 20pt | bold、uppercase、charSpacing: 4 |
| Body | 內文段落 | 14pt | regular、lineSpacingMultiple: 1.4 |
| Caption | 來源標注、頁碼、eyebrow | 10pt | regular、charSpacing: 6 |
| Insight | Tension 頁的 insight 句 | 22pt | bold italic |
| Footer | 頁尾收束句 | 11pt | italic、accent 色 |

**PPTX 版型尺寸規範：**
- 投影片尺寸：`LAYOUT_WIDE`（13.3" × 7.5"），比 16:9 更寬，適合策略報告
- 邊距：左右 0.6"，上下 0.5"，導航列高度 0.4"
- 內容區域：從 y=0.9" 開始（導航列下方）

---

#### 維度 C｜版型節奏

**決策邏輯：**

整份 deck 至少要有三種版型節奏，不能所有頁面長得一樣。

**五種標準版型（每份報告選定每種版型的具體呈現方式）：**

| 版型類型 | 適用頁面 | 核心視覺邏輯 | HTML 佈局方向 |
|---------|---------|------------|--------------|
| Statement page | Case in one line、封面、章節分頁 | 大字佔滿版面，留白為主，圖片為背景層 | `min-height: 100vh; display: flex; align-items: center` + 背景圖層 |
| Analysis page | Real problem、Tension、Reframe | 左側文字 + 右側模型圖表，或上下分區 | CSS Grid `grid-template-columns: 1fr 1fr` |
| System page | The system | 水平流程圖，接觸點圖片嵌入節點 | Flex row + 接觸點卡片陣列 |
| Proof page | Why it lands | 數據大字突出，佐證文字為輔 | 數字用 Display 字體放大，說明文字縮小對比 |
| Takeaway page | What to steal | 條列清晰，每條方法有獨立視覺區塊 | 卡片式佈局，每張卡片有 accent 色邊框或色塊 |

**排版禁止事項：**
- 不用置中對齊做主要版型（過於對稱，缺乏張力）
- 不讓所有頁面都是「左文右圖」的同一模式
- Statement page 的文字不能超過版面的 60%，留白是設計的一部分

---

#### 維度 D｜動態節奏

HTML artifact 支援 CSS 動畫。這份報告的動畫邏輯如下：

**原則：一個頁面只有一個入場動畫邏輯，不堆疊多種效果。**

```css
/* 標準入場動畫（適用大多數頁面）*/
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* 使用方式：staggered reveal，標題先進，內文後進 */
.slide-title    { animation: fadeUp 0.6s ease both; }
.slide-body     { animation: fadeUp 0.6s 0.15s ease both; }
.slide-caption  { animation: fadeUp 0.6s 0.3s ease both; }
```

**Statement page 例外：**  
可以用更戲劇性的入場，例如文字從左側滑入（`translateX(-40px)`），或 opacity 淡入搭配 scale（`scale(0.96) → scale(1)`）。

**不要用的動畫：**
- bounce、wobble、rotate 等非線性動畫
- 每個元素都有不同動畫方向（視覺噪音）
- 動畫時間超過 0.8s（讓人等）

---

### Step 3｜Visual Brief 輸出格式

完成四個維度決策後，輸出以下格式給使用者確認：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VISUAL BRIEF｜[報告名稱]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【情緒基調】[一句話描述這份報告的視覺主張]

【色彩系統】
  主背景：#______ （[顏色名稱]，[視覺感受]）
  次背景：#______
  主文字：#______
  次文字：#______
  強調色：#______ （用於[具體用途]）

【字體配對｜HTML artifact】
  Display：[Google Fonts 字體名稱]（用於[具體用途]）
  Body：[Google Fonts 字體名稱]（用於[具體用途]）

【字體配對｜PPTX】
  Header：[系統字體名稱]（對應 HTML Display 的最近替代）
  Body：[系統字體名稱]（對應 HTML Body 的最近替代）

【版型節奏】
  Statement page → [具體描述]
  Analysis page → [具體描述]
  System page → [具體描述]
  Proof page → [具體描述]
  Takeaway page → [具體描述]

【動態節奏】
  標準入場：fadeUp，staggered 0.15s
  特例頁面：[如有特殊動畫設計，說明在哪一頁用]

【視覺禁止事項（本報告特定）】
  - [依案例特性列出 2–3 條這份報告不能做的設計選擇]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
確認後進入 Phase 7 製作。
```

---

## 視覺 Ref 搜圖規則

視覺 ref 的搜圖邏輯與論證型配圖完全不同。

**目的：** 找到 2–3 張圖作為色彩方向與版型語言的視覺錨點，不是用來嵌入報告頁面。

**搜尋關鍵字模式：**
- 色彩方向：`editorial magazine layout [情緒形容詞]`、`brand strategy deck minimal dark`
- 字體靈感：`typography poster [Display字體名稱]`
- 版型靈感：`annual report design [產業形容詞]`、`strategy presentation layout`

**證據檢查（視覺 ref 版）：**
搜到的圖必須能回答以下問題，才作為參考錨點：

1. 這張圖的色彩組合，和這份報告的情緒基調吻合嗎？
2. 這張圖的版型邏輯，有沒有可以轉化進 HTML 的設計元素？
3. 這張圖不會讓整份報告看起來像在模仿某個特定品牌？

通過三個問題才作為參考。不通過則繼續搜，最多搜 3 輪。3 輪後仍無合適參考，直接進入文字描述決策，不強迫配視覺 ref。

**視覺 ref 圖片的用途限制：**
- 只作為設計決策的參考錨點
- 不嵌入報告頁面
- 不作為論證配圖使用
- 不出現在 Image Source Appendix（因為不進入最終輸出）

---

## 視覺 Ref 與論證型配圖的分工邊界

| 類型 | 目的 | 是否進入最終頁面 | 來源記錄 |
|------|------|----------------|---------|
| 視覺 ref | 確立設計語言，供 AI 製作時參考 | 否 | 不記錄 |
| 論證型配圖 | 佐證分析論點，讓讀者更相信某個判斷 | 是 | 必須記錄於 Image Source Appendix |

兩種圖的搜圖在不同步驟執行：
- 視覺 ref → Phase 6.5，在內容確認後、HTML 製作前
- 論證型配圖 → Phase 7，在頁面製作過程中逐頁處理

不能把視覺 ref 的圖直接拿來當論證配圖用。如果視覺 ref 搜到的圖恰好也能作為論證使用，必須重新走論證配圖的證據檢查流程，確認後才能嵌入。
