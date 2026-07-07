# Paper Types

Every note keeps the same 12 top-level sections from `NOTE_REQUIRED_SECTIONS`.
Paper type only changes the typed semantics of shared sections and the recommended `###` subsections used in `note_plan.section_plan`.

Use `contracts_by_paper_type[note_plan.paper_type]` as the canonical structured source:
- `section_semantics`: how each fixed top-level section should be interpreted for this paper type.
- `recommended_subsections`: paper-type-specific `###` candidates for technical or analytical sections.
- `boundary_questions`: paper-type-specific questions that should shape `central_claims`, `claim_boundaries`, `negative_or_limiting_results`, `mechanism_result_map`, `comparative_positioning`, and `followup_questions`.

## `AI_method`

section_semantics:
- 研究問題: 方法要解決的具體技術問題和現有方法短板。
- 資料與任務定義: 資料集、輸入輸出、評測任務和實驗設定。
- 方法主線: 模型、演算法、訓練或推理機制。
- 關鍵結果: 主結果、強基線、消融和關鍵數字。
- 深度分析: 方法為什麼有效、何處脆弱、重現和擴充套件代價。

recommended_subsections:
- 方法主線: `機制流程`, `模型結構`, `訓練目標`, `推理與取樣鏈路`, `關鍵實現細節`
- 關鍵結果: `主結果與強基線`, `消融到底說明瞭什麼`, `失敗或不穩定設定`
- 深度分析: `為什麼有效`, `複雜度與擴充套件性`, `重現注意點`

boundary_questions:
- 核心機制的收益由哪個實驗或消融支撐，而不是隻由主結果暗示？
- 哪些比較只能證明在當前資料、基線、算力或協議下有效，不能外推到通用場景？
- 論文是否給出失敗、退化、不穩定或成本上升的證據；如果沒有，結論邊界是什麼？

## `benchmark_or_dataset`

section_semantics:
- 研究問題: 這個 benchmark/dataset 想補足的評測或資料缺口。
- 資料與任務定義: 資料來源、任務拆分、標籤/題目定義、樣本範圍。
- 方法主線: 資料建構、篩選、標註和評測協議，不寫成模型 pipeline。
- 關鍵結果: 基線表現、難度分佈、覆蓋範圍和偏差。
- 深度分析: 它真正測到了什麼，以及不能代表什麼。

recommended_subsections:
- 資料與任務定義: `資料來源`, `任務拆分`, `標註/篩選協議`
- 方法主線: `建構流程`, `評測協議`, `Baseline 設定`
- 關鍵結果: `基線表現`, `難度分佈`, `覆蓋與偏差`
- 深度分析: `benchmark 真正測到了什麼`, `適用邊界`

boundary_questions:
- 這個 benchmark/dataset 實際測量的構念是什麼，哪些能力只是間接近似？
- 任務、標籤、取樣、過濾或評測協議會引入哪些覆蓋缺口或偏差？
- 基線結果證明了評測集有區分度，還是隻證明某類模型適應該協議？
- 樣本時長、語料長度、人口統計、類別分佈、資料可訪問性或隱私限制如何影響重現和外推？

## `clinical_or_psychology_empirical`

section_semantics:
- 研究問題: 臨床、心理學或行為科學中的研究問題、假設或變數關係。
- 資料與任務定義: 樣本來源、納排標準、變數/量表、測量方式。
- 方法主線: 研究設計、分組、測量流程和統計分析路徑。
- 關鍵結果: 主要效應、相關性、組間差異、不確定性或顯著性。
- 深度分析: 結果解釋、因果邊界、臨床/心理學意義和外推限制。

recommended_subsections:
- 資料與任務定義: `樣本與納排標準`, `變數與量表`, `測量流程`
- 方法主線: `研究設計`, `分析模型`, `主要比較`
- 關鍵結果: `主要效應`, `不確定性與顯著性`, `臨床或心理學解釋`
- 深度分析: `因果解釋邊界`, `外推限制`

boundary_questions:
- 樣本來源、納排標準、測量工具和標註流程如何限制外推？
- 結果支援相關、預測、組間差異還是因果解釋；不要越過論文設計能證明的範圍。
- 臨床或心理學意義是否依賴未觀測混雜、量表閾值、文字/語音缺失或場景約束？
- 樣本構成、資料缺失、隱私限制或材料不可公開會怎樣限制重現與再分析？

## `humanities_or_social_science`

section_semantics:
- 研究問題: 作者要解釋的社會、文化、歷史、制度或理論問題。
- 資料與任務定義: 材料、案例、文字、訪談、檔案或語料範圍，不寫成 ML task。
- 方法主線: 理論框架、概念區分和論證路徑。
- 關鍵結果: 核心解釋性發現、概念貢獻或對既有觀點的修正。
- 深度分析: 論證強度、材料邊界、解釋替代性和可遷移性。

recommended_subsections:
- 資料與任務定義: `材料範圍`, `選擇標準`, `案例或語料邊界`
- 方法主線: `理論框架`, `概念區分`, `論證路徑`
- 關鍵結果: `核心解釋性發現`, `概念貢獻`
- 深度分析: `論證強度`, `替代解釋`, `材料邊界`

boundary_questions:
- 作者的解釋依賴哪些材料、案例或理論前提？
- 是否存在同樣能解釋材料的替代解釋，論文如何排除或沒有排除？
- 哪些結論是概念貢獻或規範性判斷，而不是可直接當作經驗事實？

## `survey_or_review`

section_semantics:
- 研究問題: 綜述試圖整理的領域問題、爭議或知識缺口。
- 資料與任務定義: 納入文獻範圍、檢索/篩選標準和綜述物件。
- 方法主線: 分類體系、綜述組織方式和證據綜合邏輯，不寫成單篇方法架構。
- 關鍵結果: 領域共識、分歧、趨勢、代表性方向和開放問題。
- 深度分析: 綜述覆蓋的盲區、分類體系的解釋力和未來研究機會。

recommended_subsections:
- 資料與任務定義: `綜述範圍`, `納入/排除標準`, `文獻覆蓋`
- 方法主線: `分類體系`, `方法譜系`, `證據組織方式`
- 關鍵結果: `代表性方向`, `共識與分歧`, `開放問題`
- 深度分析: `分類體系的侷限`, `未覆蓋區域`, `後續研究機會`

boundary_questions:
- 檢索範圍、納入排除標準或分類軸會遺漏哪些研究路線？
- 綜述給出的是領域共識、作者分類，還是尚未解決的分歧？
- 哪些趨勢結論來自覆蓋範圍內的文獻分佈，不能直接當作技術成熟度判斷？

## Selection Rule

Choose one primary `note_plan.paper_type` from the synthesis bundle's allowed values first.
Then keep the fixed top-level sections and use that paper type's `section_semantics` plus `recommended_subsections` to write `note_plan.section_plan`.
