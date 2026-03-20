# Output Slide Spec · 16:9 Slide PDF

> 本文件定義「Slide PDF」輸出模式的完整設計規格。
> 當 Phase 1 Intake 確認輸出形式為「PDF（slide 比例）」「簡報」「deck」「16:9」時，Phase 7 必須依本文件執行，不得使用 output-print.md 的印刷邏輯。

---

## 1. 頁面規格

```css
@page {
  size: 338mm 190mm;   /* 16:9，等比於 1920×1080 */
  margin: 0;           /* 零 page margin，內距全部在 .slide div 內控制 */
}
```

每個投影片單元：

```css
.slide {
  width: 338mm;
  height: 190mm;
  position: relative;
  overflow: hidden;          /* 硬規則：內容絕對不能溢出 */
  page-break-after: always;
}
```

**overflow: hidden 是不可妥協的硬規則。** 如果內容塞不進去，解法是拆成兩頁，不是縮字或移除 overflow: hidden。

---

## 2. 字體規格

印刷版與 Slide 的字體層級完全不同。Slide 的讀者距離螢幕或投影畫面較遠，且閱讀時間極短。

| 層級 | 用途 | 字體大小 | 字重 | 備註 |
|------|------|---------|------|------|
| Display | 封面主標題、Section Divider 主標 | 26–34px | 800 | 可跨行，最多 3 行 |
| Title | 每頁標題（slide-header） | 16–20px | 800 | 單行為佳，最多 2 行 |
| Subtitle | 副標題、insight box 文字 | 10–12px | 700 | 核心主張句，最多 3 行 |
| Body | card / steal card 內文 | 8.5–9.5px | 400–500 | **最小可用字體** |
| Label | eyebrow、tag、小標籤 | 7–8px | 600–700 | 全大寫 + letter-spacing |
| Source | 來源標注、初步判讀標注 | 6.5–7px | 400 | italic，色彩減淡 |
| Metric | 關鍵數字 | 18–26px | 800 | 與 label 搭配形成視覺錨點 |

**禁止使用低於 6.5px 的字體。** 低於此閾值在投影時完全不可讀。

**Body 文字每個 card 或 block 內不超過 6 行。** 超過 6 行代表這個 card 的資訊量應該拆成兩個 card 或兩頁。

---

## 3. 版面設計語言

### 3.1 印刷版 vs. Slide 的根本差異

| 維度 | 印刷報告（A4） | Slide（16:9） |
|------|--------------|--------------|
| 閱讀方式 | 線性、逐段讀 | 掃視、主張先行 |
| 每頁資訊量 | 高密度 | 單一核心主張 |
| 段落文字 | 允許 5–8 行連續段落 | **禁止**，改用 card / bullet / metric |
| 色塊比例 | 點綴性 | 結構性，整頁背景色是常態 |
| 留白 | 功能性（呼吸感） | 設計語言的一部分（不填滿是對的） |
| 視覺錨點 | 選配 | **必須**：大數字、粗標題、色條、色塊 |
| 頁面高度 | 257mm（A4 扣邊距） | 190mm，零 margin |

### 3.2 每頁資訊密度原則

每頁只允許 **一個核心主張**，配 2–4 個支撐元素。

支撐元素種類：
- Metric（大數字 + 短說明）
- Card（有標題的資訊方塊，內文 ≤ 6 行）
- Steal card（方法卡，有標題 + 說明 + 條件）
- Flow（流程圖）
- Quote box（核心主張句，深色背景）
- Reframe pair（舊說法 vs. 新說法並排）

**每頁禁止出現的格式：**
- 連續段落文字（超過 3 行未換 card）
- 多層級巢狀 bullet point
- 超過 5 個 card 在同一頁
- 表格超過 6 列（表格頁例外）

### 3.3 版型庫（必須使用其中一種）

**Cover**：左右雙欄，左側主標題區，右側案例/摘要區。背景深色（主色）。

**Section Divider**：全版深色背景，大型數字（低透明度）作底，品牌名稱 + 分析視角標籤。用於每個案例的起始頁。

**Content（標準內容頁）**：頂部 4px 色條（案例識別色）+ slide-header + 主體內容區（flex 佈局）。背景白色。

**Dark Full**：全版深色背景，用於 Cross-Case Recap、結論頁的核心主張。讓讀者在視覺上感受到「轉折」。

**Appendix**：淺灰背景（#F4F7FB），雙欄文字佈局，字體較小但仍需 ≥ 7.5px。

---

## 4. 色彩使用規則

色彩系統在 Phase 6.5 由 AI 依案例調性決定。本規格定義使用規則，不限定特定色票。

**色條（slide 頂部 4px bar）**：每個案例固定一種識別色，全程一致。讓讀者看到色條就知道在看哪個案例。

**深色背景頁（Cover / Section Divider / Dark Full）**：主色（深色）佔 100% 背景。內文用白色或高亮度色。重點文字用 Accent 色（通常是暖色）。

**白色背景頁（Content / Appendix）**：內文用近黑色（#1a1a1a 或 #374151）。Card 背景用極淺色（#F4F7FB 或 #EBF4FF）。色彩點綴在 card 左邊框、badge、tag。

**禁止在白色背景頁使用低對比文字。** 文字顏色與背景的對比比率必須 ≥ 4.5:1。

---

## 5. Slide 頁數規劃

16:9 Slide 的資訊密度低於 A4 報告，因此相同內容需要更多頁。

**每案分析的 Slide 頁數：**

| 分析頁面 | A4 報告 | Slide（16:9） | 說明 |
|---------|--------|--------------|------|
| Case in one line | 1 頁 | 1 頁 | metrics 同頁 |
| Real problem | 1 頁 | 1 頁 | 三個結構性力量 + 時間點 |
| Tension | 1 頁 | 1 頁 | 可與 reframe 合頁 |
| Strategic reframe | 1 頁 | 可與 tension 合頁 | 視內容量決定 |
| System | 1 頁 | 1 頁 | flow + 說明 |
| Why it lands | 1 頁 | 1 頁 | metrics + 已驗證事實 + 判讀 |
| What to steal | 1 頁 | 1 頁 | 3 個 steal card |

**非案例頁的 Slide 頁數：**
- 封面：1 頁
- 框架說明：1 頁
- 案例總覽：1 頁
- Section Divider（每案）：1 頁 × 案例數
- Cross-Case Recap：1 頁（表格）
- 結論 Phase 框架：1 頁
- Core Insight：1 頁（Dark Full）
- 來源附錄：1–2 頁

**3 案報告預估總頁數：26–30 頁。**

---

## 6. 寫作規則（Slide 專用）

**標題必須是主張句，不是名詞句。**

| 錯誤（名詞句） | 正確（主張句） |
|--------------|--------------|
| 真實問題 | 選項愈多，旅客愈不買 |
| 核心矛盾 | 資訊透明化的終點是 AI 替你決定，不是你自己決定 |
| 策略重框 | 從資訊平台到決策平台，必須選一個 |

**例外**：slide-header 的 `sh-title`（頁面功能標籤）允許名詞句，因為它是導覽用的，不是主張。真正的主張放在 `q-box`（insight box）的 `q-text` 內。

**Quote box 的文字必須是一個完整主張，不是摘要。**
- 錯誤：「Trip.com 導入了 AI Trip Planner，讓旅客可以用三個問題完成行程規劃。」（這是描述）
- 正確：「三個問題取代三百個篩選器——Trip.com 押注的是，旅遊平台的護城河不在庫存量，而在把旅客意圖轉化為行動的速度。」（這是主張）

**Steal card 的第一行必須包含動詞，說明「做什麼」。**
- 錯誤：「意圖捕捉前台入口」
- 正確：「把「意圖捕捉」做成前台入口，取代搜尋框」

---

## 7. WeasyPrint 轉換規格

```python
from weasyprint import HTML, CSS

css = CSS(string='''
@page {
  size: 338mm 190mm;
  margin: 0;
}
''')

HTML(filename='/home/claude/report_slides.html').write_pdf(
    '/mnt/user-data/outputs/report_slides.pdf',
    stylesheets=[css]
)
```

轉換完成後呼叫 `present_files(['/mnt/user-data/outputs/report_slides.pdf'])`

**轉換前檢查清單：**
- [ ] 所有顏色使用硬編碼 hex，無 CSS variable
- [ ] 所有字體使用 system font stack，無 Google Fonts 或外部字體
- [ ] 每個 `.slide` 有 `overflow: hidden`
- [ ] 無 `position: fixed` 元素
- [ ] 無 `min-height: 100vh`
- [ ] 無 CSS animation 或 transition（WeasyPrint 不支援）
- [ ] 每個 `.slide` 有 `page-break-after: always`

---

## 8. 常見錯誤與修正

**錯誤 1｜把 A4 的字體大小直接套用到 Slide**
A4 的 body 文字 8–10px 在印刷品上可讀，但在 Slide 上太小。Slide 的 body 最小 8.5px，重要內文應在 9.5–10.5px。

**錯誤 2｜連續段落文字**
一個 card 裡放了 8 行連續文字，讀者看不完。解法：拆成兩個 card，或把次要資訊移到 source note（6.5px）。

**錯誤 3｜每頁塞太多 card**
5 個 card + 1 個 metric strip + 1 個 flow，全部在同一頁。結果每個 card 只有 2–3 行，什麼都說不清楚。解法：減少到 3 個 card，每個說清楚一件事。

**錯誤 4｜Section Divider 頁面用白色背景**
Section Divider 的功能是「視覺轉折 + 案例預告」，必須用深色背景才能讓讀者感受到節奏切換。白色背景的 Section Divider 不存在。

**錯誤 5｜忘記頂部色條**
色條是案例識別的視覺系統。每個案例分析頁的頂部必須有 4px 色條，顏色與該案例的識別色一致。沒有色條讀者無法快速判斷自己在看哪個案例。
