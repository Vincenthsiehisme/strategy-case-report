# Report Data Schema

> **讀取時機**：Phase 7 路徑 B（HTML artifact）執行前，由 `references/phases-4-7.md` 引用。  
> **用途**：定義 `report_data.json` 的完整資料結構。Claude 在 Phase 6.5 完成視覺系統決策後，依此結構填入分析內容，交由 `scripts/build_report.py` 組裝 HTML deck。  
> **字體說明**：`visual.fonts` 在 PDF 路徑使用 system font（Georgia、Arial、Palatino 等），不使用 Google Fonts；HTML artifact 路徑（路徑 B）可使用 Google Fonts。

---

## 頂層結構

```
report_data.json
├── meta          報告基本資訊
├── visual        視覺系統（色彩 + 字體）
├── cases[]       案例陣列（1–5 案）
└── conclusion    跨案結論（選填）
```

---

## `meta`

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `title` | string | ✅ | 報告標題，例：「品牌案例觀察月報｜2025 Q2」 |
| `subtitle` | string | — | 一句話說明本期聚焦的策略問題 |
| `date` | string | ✅ | 格式 `YYYY-MM-DD` |
| `mode` | string | ✅ | `"full"` 或 `"sprint"` |

---

## `visual`

### `visual.colors`

| 欄位 | 說明 |
|------|------|
| `bg_primary` | 主背景色，覆蓋 60–70% 視覺面積 |
| `bg_secondary` | 次要背景，用於區塊分隔或卡片底色 |
| `text_primary` | 主文字色 |
| `text_secondary` | 次要文字色，用於說明文字、標注 |
| `accent` | 強調色，用於關鍵判斷句、圖表亮點、頁碼 |

所有顏色填硬編碼 hex（如 `"#1a1a1a"`），不使用 CSS variable。

### `visual.fonts`

| 欄位 | 說明 |
|------|------|
| `display` | Display 層級字體，用於頁面大標題、Statement page 大字 |
| `body` | Body 層級字體，用於內文、說明、標注 |

PDF 路徑填 system font（Georgia、Arial、Palatino 等）。HTML 路徑可填 Google Fonts 名稱。

### `visual.mood`

情緒基調標籤，從以下四選一：`銳利張力` / `沉穩優雅` / `專業精準` / `高冷奢華`

---

## `cases[]`

每個 case 物件包含以下欄位：

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `id` | number | ✅ | 案例序號，從 1 起算 |
| `brand` | string | ✅ | 品牌名稱 |
| `industry` | string | ✅ | 產業類別 |
| `year` | string | ✅ | 執行年份，例：`"2024"` 或 `"2023–24"` |
| `case_in_one_line` | string | ✅ | 格式：「[品牌] 面對 [真實問題]，選擇 [策略動作]，而不是 [原本的做法]。」 |
| `pages` | object | ✅ | 各分析頁內容，見下方 |
| `model_configs` | array | — | 使用的分析模型配置，見下方 |
| `sources` | array | ✅ | 來源列表，見下方 |

### `cases[].pages`

Full Mode 必填：`real_problem` / `tension` / `strategic_reframe` / `system` / `why_it_lands` / `what_to_steal`  
Sprint Mode 必填：`real_problem` / `tension` / `strategic_reframe` / `what_to_steal`

所有頁面物件共用 `pending_verification` 欄位：`false` = 內容已驗證；`true` = 有 ⚠️ 內容，build_report.py 會自動加上「初步判讀，待驗證」標注。

**`real_problem`**

| 欄位 | 說明 |
|------|------|
| `headline` | 頁面標題，10–20 字 |
| `body` | 核心問題定義，說明為何品牌不能照舊做，2–3 句 |
| `footer` | 頁尾收束句，比標題再往前推半步的判斷 |
| `pending_verification` | boolean |

**`tension`**

| 欄位 | 說明 |
|------|------|
| `headline` | 頁面標題 |
| `insight` | Insight 句，消費者 / 市場的核心矛盾判斷 |
| `body` | 矛盾來源說明 |
| `footer` | 頁尾收束句 |
| `pending_verification` | boolean |

**`strategic_reframe`**

| 欄位 | 說明 |
|------|------|
| `headline` | 頁面標題 |
| `old_frame` | 品牌原本的說法 |
| `new_frame` | 品牌選擇的新說法 |
| `rationale` | 換框依據，一句話 |
| `footer` | 頁尾收束句 |
| `pending_verification` | boolean |

**`system`**

| 欄位 | 說明 |
|------|------|
| `headline` | 頁面標題 |
| `touchpoints` | 接觸點陣列，見下方 |
| `image_brief` | 若有接觸點圖片待補，填入配圖需求描述；否則填 `null` |
| `footer` | 頁尾收束句 |
| `pending_verification` | boolean |

`touchpoints` 每項：

| 欄位 | 說明 |
|------|------|
| `name` | 接觸點名稱 |
| `role` | 這個點在消費者路徑中的角色 |
| `image_status` | `"found"` 已找到配圖 / `"needed"` 需補圖 |

**`why_it_lands`**

| 欄位 | 說明 |
|------|------|
| `headline` | 頁面標題 |
| `verified_facts` | string[]，已有公開數據佐證的事實，每條附來源標注 |
| `preliminary_reads` | string[]，初步判讀（缺乏公開數據支持），可為空陣列 |
| `footer` | 頁尾收束句 |
| `pending_verification` | boolean |

**`what_to_steal`**

| 欄位 | 說明 |
|------|------|
| `headline` | 頁面標題 |
| `methods` | 可借用方法陣列，見下方 |
| `footer` | 頁尾收束句 |
| `pending_verification` | boolean |

`methods` 每項：

| 欄位 | 說明 |
|------|------|
| `method` | 具體方法描述，動詞開頭 |
| `condition` | 適用條件：什麼類型的品牌、什麼情境下可借用 |

### `cases[].model_configs`

選填。每項記錄本案使用的分析模型：

| 欄位 | 說明 |
|------|------|
| `model` | 模型名稱，參照 `references/model-library.md` |
| `page` | 放在哪一頁，例：`"system"` / `"tension"` |
| `purpose` | 這個模型在此頁解決什麼分析問題（非模型名稱，是本案應用結論） |

### `cases[].sources`

每項：

| 欄位 | 說明 |
|------|------|
| `label` | 資訊標注，說明這筆來源用於哪個判斷 |
| `source` | 來源名稱或完整 URL |
| `type` | `"official"` / `"major_media"` / `"secondary_media"` |

---

## `conclusion`

選填。Sprint Mode 可設為 `null`。

| 欄位 | 說明 |
|------|------|
| `cross_case_insight` | 從多案提煉出的跨案洞察，不是摘要，是更高一層的判斷 |
| `action_prompt` | 對讀者的行動建議或思考提問 |

---

## 最小合法範例（Full Mode，單案）

```json
{
  "meta": {
    "title": "品牌案例觀察月報｜2025 Q2",
    "subtitle": "本期聚焦：旅遊品牌如何在 OTA 夾殺下重建直客關係",
    "date": "2026-03-21",
    "mode": "full"
  },
  "visual": {
    "colors": {
      "bg_primary": "#1a1a1a",
      "bg_secondary": "#2a2a2a",
      "text_primary": "#f0f0f0",
      "text_secondary": "#999999",
      "accent": "#e8c547"
    },
    "fonts": {
      "display": "Georgia",
      "body": "Arial"
    },
    "mood": "沉穩優雅"
  },
  "cases": [
    {
      "id": 1,
      "brand": "品牌名稱",
      "industry": "旅遊",
      "year": "2024",
      "case_in_one_line": "[品牌] 面對 [真實問題]，選擇 [策略動作]，而不是 [原本的做法]。",
      "pages": {
        "real_problem": {
          "headline": "頁面標題",
          "body": "說明為何品牌不能照舊做。",
          "footer": "頁尾收束句。",
          "pending_verification": false
        },
        "tension": {
          "headline": "頁面標題",
          "insight": "Insight 句。",
          "body": "矛盾來源說明。",
          "footer": "頁尾收束句。",
          "pending_verification": false
        },
        "strategic_reframe": {
          "headline": "頁面標題",
          "old_frame": "舊說法。",
          "new_frame": "新說法。",
          "rationale": "換框依據。",
          "footer": "頁尾收束句。",
          "pending_verification": false
        },
        "system": {
          "headline": "頁面標題",
          "touchpoints": [
            { "name": "接觸點 A", "role": "角色說明", "image_status": "found" },
            { "name": "接觸點 B", "role": "角色說明", "image_status": "needed" },
            { "name": "接觸點 C", "role": "角色說明", "image_status": "found" }
          ],
          "image_brief": "接觸點 B 需補圖：品牌官網活動頁截圖",
          "footer": "頁尾收束句。",
          "pending_verification": false
        },
        "why_it_lands": {
          "headline": "頁面標題",
          "verified_facts": ["事實 1（來源：品牌新聞稿）", "事實 2（來源：經濟日報）"],
          "preliminary_reads": ["初步判讀 1（缺乏公開數據支持）"],
          "footer": "頁尾收束句。",
          "pending_verification": true
        },
        "what_to_steal": {
          "headline": "頁面標題",
          "methods": [
            {
              "method": "動詞開頭的方法描述",
              "condition": "適用於具備 X 條件的品牌，在 Y 情境下使用"
            }
          ],
          "footer": "頁尾收束句。",
          "pending_verification": false
        }
      },
      "model_configs": [
        {
          "model": "Consumer Journey",
          "page": "system",
          "purpose": "說明接觸點在消費者路徑中的邏輯關係"
        }
      ],
      "sources": [
        { "label": "品牌背景資料", "source": "https://example.com/press", "type": "official" },
        { "label": "市場數據", "source": "經濟日報 2024-08-15", "type": "major_media" }
      ]
    }
  ],
  "conclusion": {
    "cross_case_insight": "跨案洞察句。",
    "action_prompt": "對讀者的行動建議。"
  }
}
```
