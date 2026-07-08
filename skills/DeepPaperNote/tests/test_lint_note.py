from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from lint_note import (
    core_info_structure_issues,
    figure_structure_issues,
    figure_structure_passes,
    find_missing_sections,
    front_matter_order_warnings,
    has_figure_marker,
    inspect_note_plan,
    inspect_figure_callouts,
    inspect_substantive_content,
    math_render_issues,
    mechanical_translation_artifact_issues,
    mixed_language_issues,
    strip_frontmatter,
    suspicious_code_formatted_math,
    suspicious_mid_sentence_linebreaks,
)


def _valid_note_text() -> str:
    return """# Paper

## 核心資訊

- 標題: Paper
- 發表時間: 2024
- DOI: 10.1234/example

## 原文摘要翻譯

論文圍繞長鏈路推理中的錯誤傳播問題，提出一種把檢索證據、工具呼叫狀態和最終答案聯合建模的框架，並報告了主要實驗結論。

## 創新點

- 論文把檢索證據選擇和工具呼叫規劃放在同一個狀態轉移過程裡建模，使錯誤證據不會在後續步驟中被預設當成可靠輸入。
- 論文設計了失敗呼叫回溯機制，顯式記錄每一步工具返回的置信度和異常型別，從而讓最終答案能區分證據不足和模型推理錯誤。

## 一句話總結

這篇論文用可稽核的工具呼叫狀態機降低長鏈路問答中的錯誤累積。

## 研究問題

論文關注多步問答系統在檢索證據不完整、工具呼叫失敗和中間狀態被誤用時，如何保持最終答案的可追溯性與可靠性。

## 資料與任務定義

任務輸入包括使用者問題、候選檢索證據和可呼叫工具列表；輸出包括最終答案、每一步工具呼叫記錄以及失敗原因標註。

## 方法主線

### 機制流程

輸入問題先進入證據篩選模組，隨後工具規劃器選擇下一步呼叫，最後由答案產生器結合狀態日誌輸出可追溯結論。

> [!figure] 圖一 方法概覽
> 建議位置：方法主線
> 放置原因：幫助理解整體過程。
> 當前狀態：保留佔位；未找到高置信度整圖。

## 關鍵結果

在三個多步問答資料集上，方法把答案準確率從 71.2% 提升到 78.5%，並將不可追溯錯誤比例從 18% 降到 9%。

## 深度分析

這項工作的關鍵價值不只是提升最終分數，而是把失敗工具呼叫從隱藏中間狀態變成可檢查證據，因此適合需要稽核鏈路的知識密集型問答。

## 侷限

論文主要在英文問答資料上驗證，工具集合也集中在檢索和計算兩類，尚未證明該狀態機能穩定覆蓋多模態工具或高延遲外部服務。

## 我的筆記

我會重點關注它的失敗回溯機制是否能遷移到論文精讀流程，因為 DeepPaperNote 同樣需要區分證據缺失和模型總結不足。

## 引用

- Smith et al. 2024. Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example
"""


def test_figure_callout_requires_status_line() -> None:
    note = """# Title

## 核心資訊

> [!figure] Fig. 1 方法圖
> 建議位置：方法主線
> 放置原因：幫助理解整體流程。
"""
    warnings = inspect_figure_callouts(note)
    assert "figure_callout_missing_status" in warnings


def test_legacy_placeholder_block_is_flagged() -> None:
    note = """# Title

[FIGURE_PLACEHOLDER]
id: Fig.1
[/FIGURE_PLACEHOLDER]
"""
    warnings = inspect_figure_callouts(note)
    assert "legacy_figure_placeholder_block_used" in warnings


def test_figure_bucket_heading_is_figure_structure_issue() -> None:
    note = """# Title

## 深度分析

### 剩餘圖表佔位

> [!figure] Fig. 6 補充圖
> 建議位置：深度分析
> 放置原因：幫助理解補充材料。
> 當前狀態：保留佔位；未找到高置信度整圖。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "figure_placeholder_bucket_heading" for issue in issues)
    assert figure_structure_passes(note) is False


def test_figure_callout_target_section_mismatch_is_flagged() -> None:
    note = """# Title

## 深度分析

> [!figure] Fig. 1 問題邊界圖
> 建議位置：研究問題
> 放置原因：幫助定義問題邊界。
> 當前狀態：保留佔位；未找到高置信度整圖。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "figure_callout_placement_mismatch" for issue in issues)


def test_figure_callout_inside_declared_section_passes() -> None:
    note = """# Title

## 方法主線

### 機制流程

> [!figure] Fig. 2 總體流程
> 建議位置：方法主線
> 放置原因：幫助理解執行鏈。
> 當前狀態：保留佔位；未找到高置信度整圖。

> [!figure] Fig. 3 機制細節
> 建議位置：機制流程
> 放置原因：幫助理解執行鏈細節。
> 當前狀態：保留佔位；未找到高置信度整圖。
"""
    assert figure_structure_issues(note) == []
    assert figure_structure_passes(note) is True


def test_figure_callout_with_inserted_image_status_fails_figure_structure_gate() -> None:
    note = """# Title

## 方法主線

> [!figure] Fig. 2 總體流程
> 建議位置：方法主線
> 放置原因：幫助理解執行鏈。
> 當前狀態：已替換為真實圖片；當前插入的是論文原圖的區域性面板。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "inserted_figure_redundant_callout" for issue in issues)
    assert figure_structure_passes(note) is False


def test_dqn_style_callout_plus_embed_fails_figure_structure_gate() -> None:
    note = """# Title

## 方法主線

> [!figure] Fig. 1 Agent-environment loop
> 建議位置：方法主線
> 放置原因：幫助理解強化學習互動閉環。
> 當前狀態：已複製到 images/figure_1.png，並插入為真實圖片。
![Figure 1](../img/DQN/figure_1.png)
*論文原圖編號：Fig. 1。Agent-environment loop。*
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "inserted_figure_redundant_callout" for issue in issues)
    assert figure_structure_passes(note) is False


def test_non_figure_remaining_heading_is_not_flagged() -> None:
    note = """# Title

## 深度分析

### 剩餘問題

這裡討論論文還沒有回答的問題。
"""
    assert figure_structure_issues(note) == []


def test_figure_callout_missing_location_fails_figure_structure_gate() -> None:
    note = """# Title

## 方法主線

> [!figure] Fig. 1 方法圖
> 放置原因：幫助理解整體流程。
> 當前狀態：保留佔位；未找到高置信度整圖。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "figure_callout_missing_location" for issue in issues)
    assert figure_structure_passes(note) is False


def test_figure_callout_missing_title_fails_figure_structure_gate() -> None:
    note = """# Title

## 方法主線

> [!figure]
> 建議位置：方法主線
> 放置原因：幫助理解整體流程。
> 當前狀態：保留佔位；未找到高置信度整圖。
"""
    warnings = inspect_figure_callouts(note)
    issues = figure_structure_issues(note)
    assert "figure_callout_missing_title" in warnings
    assert any(issue["reason"] == "figure_callout_missing_title" for issue in issues)
    assert figure_structure_passes(note) is False


def test_nonstandard_bracket_figure_placeholder_fails_figure_structure_gate() -> None:
    note = """# Title

## 研究問題

[圖表佔位 | Fig. 1] 論文給出的整體任務示意圖。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "nonstandard_figure_placeholder_format" for issue in issues)
    assert figure_structure_passes(note) is False


def test_nonstandard_colon_and_english_figure_placeholders_fail_gate() -> None:
    note = """# Title

## 關鍵結果

圖表佔位：Table 2 跨資料集結果。

Figure Placeholder | Fig. 3 reasoning example.
"""
    issues = figure_structure_issues(note)
    assert len([issue for issue in issues if issue["reason"] == "nonstandard_figure_placeholder_format"]) == 2
    assert figure_structure_passes(note) is False


def test_image_embed_without_italic_caption_fails_figure_structure_gate() -> None:
    note = """# Title

## 方法主線

![Fig. 2 Architecture](images/page_005_fig_figure_2.png)
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "inserted_figure_missing_caption" for issue in issues)
    assert figure_structure_passes(note) is False


def test_flashattention_style_embed_with_italic_caption_passes() -> None:
    note = """# Title

## 方法主線

![Fig. 2 Architecture](../img/FlashAttention/page_005_fig_figure_2.png)
*論文原圖編號：Fig. 2。FlashAttention 的分塊計算流程圖。這裡插入是因為它最能幫助理解方法主線。*
"""
    assert figure_structure_issues(note) == []
    assert figure_structure_passes(note) is True
    assert has_figure_marker(note) is True


def test_usable_candidate_soft_placeholder_reasons_fail_figure_structure_gate() -> None:
    statuses = [
        "影像裁剪可讀，但最終筆記採用佔位以保持輕量。",
        "影像匹配度高，但最終筆記不插入真實圖片。",
        "表格裁剪清晰，但正文已摘錄核心數值。",
        "雖然有可用候選圖，但表格內容在正文中更適合直接轉寫關鍵數值。",
        "已人工檢視，裁剪清晰且圖號匹配；但 Fig. 1 已承擔主流程說明，因此作為低優先順序補充圖保留佔位。",
        "已人工檢視，影像清晰且圖號匹配；由於它服務於輔助集說明，而非主結論，因此作為低優先順序補充圖保留佔位。",
    ]
    for status in statuses:
        note = f"""# Title

## 方法主線

> [!figure] Fig. 2 候選圖
> 建議位置：方法主線
> 放置原因：幫助理解執行鏈。
> 當前狀態：{status}
"""
        issues = figure_structure_issues(note)
        assert any(issue["reason"] == "usable_candidate_unresolved_decision" for issue in issues)
        assert figure_structure_passes(note) is False


def test_usable_candidate_visual_defect_placeholder_reason_passes() -> None:
    note = """# Title

## 方法主線

> [!figure] Table 5 評測表
> 建議位置：方法主線
> 放置原因：幫助理解評測協議。
> 當前狀態：候選裁剪可用，但混入相鄰 Table 6。
"""
    assert figure_structure_issues(note) == []
    assert figure_structure_passes(note) is True


def test_usable_candidate_lower_priority_placeholder_reason_fails() -> None:
    note = """# Title

## 方法主線

> [!figure] Fig. 3 補充機制圖
> 建議位置：方法主線
> 放置原因：幫助理解補充機制。
> 當前狀態：候選裁剪可用；已插入 Figure 2 作為同一機制更核心圖，因此本圖低優先順序。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "usable_candidate_unresolved_decision" for issue in issues)
    assert figure_structure_passes(note) is False


def test_usable_candidate_materialization_blocked_reason_passes() -> None:
    note = """# Title

## 方法主線

> [!figure] Fig. 4 工具鏈圖
> 建議位置：方法主線
> 放置原因：幫助理解工具鏈。
> 當前狀態：候選可用但 materialize_note_figure.py 複製失敗/許可權不足。
"""
    assert figure_structure_issues(note) == []
    assert figure_structure_passes(note) is True


def test_missing_asset_must_not_be_reported_as_materialization_blocked() -> None:
    note = """# Title

## 方法主線

> [!figure] Fig. 4 系統圖
> 建議位置：方法主線
> 放置原因：幫助理解整體執行鏈。
> 當前狀態：保留佔位：對應影像資產缺失導致 materialize_note_figure.py 複製 blocked；保留結構佔位用於回查原圖。
"""
    issues = figure_structure_issues(note)
    assert any(
        issue["reason"] == "missing_asset_misreported_as_materialization_blocked"
        for issue in issues
    )
    assert figure_structure_passes(note) is False


def test_chinese_placeholder_policy_prose_is_not_flagged_as_nonstandard_placeholder() -> None:
    note = """# Title

## 深度分析

這裡討論圖表佔位策略為什麼不能替代正文分析。
"""
    assert figure_structure_issues(note) == []


def test_mechanical_translation_detector_flags_figure_title_artifacts() -> None:
    note = "> [!figure] Figure 7 Storing the KV快取 of two requests at the same time in vLLM"

    issues = mechanical_translation_artifact_issues(note)

    assert len(issues) == 1
    assert issues[0]["artifact"]


def test_mechanical_translation_detector_flags_metadata_artifacts() -> None:
    note = "- 機構: UC Berkeley, Stanford University, In相關 Researcher, UC San Diego"

    issues = mechanical_translation_artifact_issues(note)

    assert len(issues) == 1
    assert issues[0]["line_number"] == 1


def test_mechanical_translation_detector_accepts_stable_proper_nouns() -> None:
    note = "> [!figure] Fig. 2 Overview of the training pipeline，訓練流程概覽。"

    assert mechanical_translation_artifact_issues(note) == []


def test_mixed_language_detector_flags_prose_line() -> None:
    note = "這篇論文 uses a model and the result is better than baseline in several settings."
    issues = mixed_language_issues(note)
    assert len(issues) == 1


def test_mixed_language_detector_exempts_figure_status_lines() -> None:
    note = "> 當前狀態：保留佔位；當前提取結果只拿到 partial crop，無法穩定還原。"
    issues = mixed_language_issues(note)
    assert issues == []


def test_mixed_language_detector_exempts_figure_callout_title_only() -> None:
    note = "> [!figure] Fig. 2 Overview of the training pipeline，訓練流程概覽。"
    issues = mixed_language_issues(note)
    assert issues == []


def test_mixed_language_detector_flags_ordinary_blockquote_prose() -> None:
    note = "> 這段解釋 uses a model and the result is better than baseline in experiments."
    issues = mixed_language_issues(note)
    assert len(issues) == 1


def test_mixed_language_detector_exempts_core_info_section() -> None:
    note = """## 核心資訊

- 標題：
`AffectGPT: A New Dataset, Model, and Benchmark for Emotion Understanding with Multimodal Large Language Models`
- 作者：
Zheng Lian, Haoyu Chen, Lan Chen
- 機構：
Institute of Automation, Chinese Academy of Sciences
"""
    issues = mixed_language_issues(note)
    assert issues == []


def test_mixed_language_detector_exempts_core_info_wrapped_value_lines() -> None:
    note = """## 核心資訊

- 作者：
Zheng Lian, Haoyu Chen, Lan Chen, Haiyang Sun
and additional collaborators from multiple institutions
"""
    issues = mixed_language_issues(note)
    assert issues == []


def test_mixed_language_detector_flags_summary_section_when_mixed() -> None:
    note = """## 原文摘要翻譯

這篇論文 uses a multimodal framework and achieves strong performance.
"""
    issues = mixed_language_issues(note)
    assert len(issues) == 1


def test_mid_sentence_linebreak_detector_flags_pdf_style_wrapping() -> None:
    note = "這篇論文最重要的貢獻在於，\n它重新定義了視覺自迴歸的預測順序。"
    issues = suspicious_mid_sentence_linebreaks(note)
    assert len(issues) == 1


def test_mid_sentence_linebreak_detector_ignores_real_paragraph_breaks() -> None:
    note = "這篇論文最重要的貢獻在於重新定義了視覺自迴歸的預測順序。\n\n## 方法主線"
    issues = suspicious_mid_sentence_linebreaks(note)
    assert issues == []


def test_code_formatted_math_detector_flags_inline_code_formula() -> None:
    note = "核心分解可以寫成 `p(r_1, r_2)=\\prod_k p(r_k | r_{<k})`。"
    issues = suspicious_code_formatted_math(note)
    assert len(issues) == 1


def test_code_formatted_math_detector_flags_fenced_formula_block() -> None:
    note = """```
L = x + y
```"""
    issues = suspicious_code_formatted_math(note)
    assert len(issues) == 1


def test_math_render_detector_flags_double_escaped_tex_command() -> None:
    note = """## 方法主線

$$
\\\\tau = \\\\exp(x)
$$
"""
    issues = math_render_issues(note)
    assert any(issue["reason"] == "double_escaped_tex_command" for issue in issues)


def test_math_render_detector_flags_invalid_frac_arguments() -> None:
    note = r"""$$
\mathrm{Precision} =
\frac{a}
\left|b\right|}
$$
"""
    issues = math_render_issues(note)
    assert any(issue["reason"] == "invalid_frac_arguments" for issue in issues)


def test_math_render_detector_flags_environment_mismatch() -> None:
    note = r"""$$
\begin{cases}
a
$$
"""
    issues = math_render_issues(note)
    assert any(issue["reason"] == "environment_mismatch" for issue in issues)


def test_math_render_detector_flags_left_right_mismatch() -> None:
    note = r"""$$
\left| x + y
$$
"""
    issues = math_render_issues(note)
    assert any(issue["reason"] == "left_right_mismatch" for issue in issues)


def test_math_render_detector_flags_unbalanced_braces() -> None:
    note = r"""$$
\bar{R_t
$$
"""
    issues = math_render_issues(note)
    assert any(issue["reason"] == "unbalanced_braces" for issue in issues)


def test_math_render_detector_accepts_valid_cases_formula() -> None:
    note = r"""$$
\tau =
\begin{cases}
1, & \bar R_t^{(c)} \ge \bar R_t^{(w)} \\
\exp(\bar R_t^{(c)} - \bar R_t^{(w)}), & \bar R_t^{(c)} < \bar R_t^{(w)}
\end{cases}
$$
"""
    issues = math_render_issues(note)
    assert issues == []


def test_find_missing_sections_requires_innovation_section() -> None:
    note = """# Title

## 核心資訊

## 原文摘要翻譯

## 一句話總結

## 研究問題

## 資料與任務定義

## 方法主線

## 關鍵結果

## 深度分析

## 侷限

## 我的筆記

## 引用
"""
    missing = find_missing_sections(note)
    assert "創新點" in missing


def test_substantive_gate_passes_specific_note() -> None:
    issues = inspect_substantive_content(_valid_note_text())

    assert issues == []


def test_substantive_gate_rejects_empty_shell_innovation() -> None:
    note = _valid_note_text().replace(
        "- 論文把檢索證據選擇和工具呼叫規劃放在同一個狀態轉移過程裡建模，使錯誤證據不會在後續步驟中被預設當成可靠輸入。\n"
        "- 論文設計了失敗呼叫回溯機制，顯式記錄每一步工具返回的置信度和異常型別，從而讓最終答案能區分證據不足和模型推理錯誤。",
        "本文提出一種新方法，具有創新性。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "innovation_empty_shell" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_substantive_gate_warns_single_specific_innovation() -> None:
    note = _valid_note_text().replace(
        "- 論文把檢索證據選擇和工具呼叫規劃放在同一個狀態轉移過程裡建模，使錯誤證據不會在後續步驟中被預設當成可靠輸入。\n"
        "- 論文設計了失敗呼叫回溯機制，顯式記錄每一步工具返回的置信度和異常型別，從而讓最終答案能區分證據不足和模型推理錯誤。",
        "- 論文把檢索證據選擇和工具呼叫規劃放在同一個狀態轉移過程裡建模，使錯誤證據不會在後續步驟中被預設當成可靠輸入。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "innovation_too_few_specific_points" for issue in issues)
    assert all(issue["severity"] != "error" for issue in issues)


def test_substantive_gate_rejects_generic_key_results() -> None:
    note = _valid_note_text().replace(
        "在三個多步問答資料集上，方法把答案準確率從 71.2% 提升到 78.5%，並將不可追溯錯誤比例從 18% 降到 9%。",
        "實驗結果表明方法有效。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "key_results_empty_shell" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_substantive_gate_rejects_honest_missing_in_key_results() -> None:
    note = _valid_note_text().replace(
        "在三個多步問答資料集上，方法把答案準確率從 71.2% 提升到 78.5%，並將不可追溯錯誤比例從 18% 降到 9%。",
        "本文未給出可重現的定量 benchmark；依據是正文和附錄都只報告案例分析，沒有指標表或 baseline 對比，因此這裡不能偽造數值結論，只能說明結論強度受限。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "key_results_honest_missing_not_allowed" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_substantive_gate_rejects_honest_missing_outside_references() -> None:
    note = _valid_note_text().replace(
        "輸入問題先進入證據篩選模組，隨後工具規劃器選擇下一步呼叫，最後由答案產生器結合狀態日誌輸出可追溯結論。",
        "本文未給出可重現的方法流程；依據是正文和附錄都沒有展開模組輸入輸出，因此這裡不能補寫機制細節，只能說明方法理解受限。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "section_honest_missing_not_allowed" for issue in issues)
    assert any(issue["section"] == "方法主線" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_substantive_gate_rejects_placeholder_references() -> None:
    note = _valid_note_text().replace(
        "- Smith et al. 2024. Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example",
        "待補充。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "references_placeholder" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_substantive_gate_accepts_real_reference_entry() -> None:
    note = _valid_note_text().replace(
        "- Smith et al. 2024. Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example",
        "- [[Auditable Tool Use|Smith et al. 2024]] 提供了工具呼叫稽核的直接參考。",
    )

    issues = inspect_substantive_content(note)

    assert not any(issue["section"] == "引用" for issue in issues)


def test_substantive_gate_allows_honest_missing_in_references() -> None:
    note = _valid_note_text().replace(
        "- Smith et al. 2024. Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example",
        "本文未給出可解析的參考文獻條目；依據是正文和附錄未提供 DOI、arXiv 或編號引用，因此引用完整性受限。",
    )

    issues = inspect_substantive_content(note)

    assert not any(issue["severity"] == "error" for issue in issues)
    assert any(issue["reason"] == "references_unavailable_declared" for issue in issues)


def test_substantive_gate_rejects_generic_limitation() -> None:
    note = _valid_note_text().replace(
        "論文主要在英文問答資料上驗證，工具集合也集中在檢索和計算兩類，尚未證明該狀態機能穩定覆蓋多模態工具或高延遲外部服務。",
        "未來工作需要更多資料。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "limitations_empty_shell" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_strip_frontmatter_removes_yaml_block() -> None:
    text = "---\ntags:\n  - papers/NLP\ndate: 2024-01-01\n---\n\n# Title\n\n## 核心資訊\n"
    assert strip_frontmatter(text).lstrip().startswith("# Title")


def test_strip_frontmatter_is_noop_without_frontmatter() -> None:
    text = "# Title\n\n## 核心資訊\n"
    assert strip_frontmatter(text) == text


def test_title_heading_not_flagged_when_frontmatter_present() -> None:
    # A note that starts with YAML frontmatter should NOT trigger title_heading_missing.
    # We test via strip_frontmatter directly since main() does I/O.
    text = "---\ntags:\n  - papers/NLP\naliases:\n  - MyPaper\ndate: 2024-01-01\ndoi: 10.1234/test\n---\n\n# My Paper Title\n"
    assert strip_frontmatter(text).lstrip().startswith("# ")


def test_mid_sentence_linebreaks_not_triggered_by_frontmatter() -> None:
    # Frontmatter lines like "date: 2024-01-01\ndoi: 10.xxx" must not be treated as
    # mid-sentence prose linebreaks.
    frontmatter_only = "---\ntags:\n  - papers/NLP\naliases:\n  - MyPaper\ndate: 2024-01-01\ndoi: 10.1234/test\n---\n"
    issues = suspicious_mid_sentence_linebreaks(strip_frontmatter(frontmatter_only))
    assert issues == []


def test_front_matter_order_requires_innovation_after_abstract() -> None:
    note = """# Title

## 核心資訊

## 原文摘要翻譯

## 一句話總結

## 創新點
"""
    warnings = front_matter_order_warnings(note)
    assert "front_matter_order_invalid" in warnings


def test_core_info_accepts_fixed_metadata_schema() -> None:
    note = """# Title

## 核心資訊

- 標題: Example Paper
- 標題翻譯: 示例論文
- 作者: Ada Lovelace; Alan Turing
- 機構: Example Lab
- 發表時間: 2024
- 發表管道: arXiv
- DOI: 10.1234/example
- arXiv: 2401.00001
- 論文連結: https://arxiv.org/abs/2401.00001
- 程式碼 / 專案: https://github.com/example/project
- 資料 / 資源: https://example.org/data
- 論文型別: AI_method

## 原文摘要翻譯
"""

    assert core_info_structure_issues(note) == []


def test_core_info_rejects_prose_and_ad_hoc_fields() -> None:
    note = """# Title

## 核心資訊

- 標題: Example Paper
- 作者: Ada Lovelace
- 我的評價: 很重要

這篇論文的核心不是提出新模型，而是建立一個評測場。

## 原文摘要翻譯
"""

    issues = core_info_structure_issues(note)

    assert any(issue["reason"] == "core_info_unknown_field" for issue in issues)
    assert any(issue["reason"] == "core_info_non_metadata_line" for issue in issues)


def test_core_info_rejects_out_of_order_fields() -> None:
    note = """# Title

## 核心資訊

- 作者: Ada Lovelace
- 標題: Example Paper

## 原文摘要翻譯
"""

    issues = core_info_structure_issues(note)

    assert any(issue["reason"] == "core_info_field_order_invalid" for issue in issues)


def test_core_info_issues_fail_basic_structure_gate(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    plan_path = tmp_path / "Paper.plan.json"
    note_path.write_text(
        _valid_note_text().replace(
            "- DOI: 10.1234/example",
            "- DOI: 10.1234/example\n\n這篇論文在元資料塊裡追加了一句導讀。",
        ),
        encoding="utf-8",
    )
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "method paper",
                "dominant_domain": "NLP",
                "must_cover": ["problem", "method"],
                "key_numbers": ["78.5"],
                "real_comparisons": ["baseline"],
                "central_claims": [
                    {
                        "claim": "The method improves traceability.",
                        "supporting_evidence": [{"section_id": "sec:method"}],
                        "what_it_actually_proves": "The described mechanism records tool states.",
                        "what_it_does_not_prove": "It does not prove production robustness.",
                    }
                ],
                "claim_boundaries": ["The evidence is limited to the reported workflow."],
                "negative_or_limiting_results": ["The paper does not report multi-service failures."],
                "mechanism_result_map": ["The failure-state mechanism explains lower unrecoverable errors."],
                "comparative_positioning": ["The method is compared against answer-only baselines."],
                "reuse_takeaways": ["Track failure state explicitly."],
                "followup_questions": ["Check whether the mechanism survives missing tool outputs."],
                "section_plan": [{"section": "方法主線", "evidence_sources": [{"section_id": "sec:method"}]}],
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "scripts" / "lint_note.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--input",
            str(note_path),
            "--plan-file",
            str(plan_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["passes_basic_structure"] is False
    assert "core_info_non_metadata_line" in payload["warnings"]


def test_note_plan_missing_fails_plan_gate(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    note_path.write_text(_valid_note_text(), encoding="utf-8")

    script_path = Path(__file__).resolve().parents[1] / "scripts" / "lint_note.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--input", str(note_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["planning_artifact_found"] is False
    assert payload["planning_artifact_issues"] == ["planning_artifact_missing"]
    assert "planning_artifact_missing" in payload["warnings"]
    assert payload["passes_basic_structure"] is True
    assert payload["passes_style_gate"] is True
    assert payload["passes_math_gate"] is True
    assert payload["passes_figure_gate"] is True
    assert payload["passes_plan_gate"] is False


def test_mechanical_translation_artifacts_fail_style_gate(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    plan_path = tmp_path / "Paper.plan.json"
    note_path.write_text(
        _valid_note_text().replace(
            "放置原因：幫助理解整體過程。",
            "放置原因：Figure 7 Storing the KV快取 of two requests.",
        ),
        encoding="utf-8",
    )
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "The paper proposes a model mechanism and evaluates it experimentally.",
                "dominant_domain": "reasoning",
                "must_cover": ["方法主線"],
                "key_numbers": ["78.5"],
                "real_comparisons": ["baseline"],
                "central_claims": [
                    {
                        "claim": "The method improves traceability.",
                        "supporting_evidence": [{"section_id": "sec:method"}],
                        "what_it_actually_proves": "The described mechanism records tool states.",
                        "what_it_does_not_prove": "It does not prove production robustness.",
                    }
                ],
                "claim_boundaries": ["The evidence is limited to the reported workflow."],
                "negative_or_limiting_results": ["The paper does not report multi-service failures."],
                "mechanism_result_map": ["The failure-state mechanism explains lower unrecoverable errors."],
                "comparative_positioning": ["The method is compared against answer-only baselines."],
                "reuse_takeaways": ["Track failure state explicitly."],
                "followup_questions": ["Check whether the mechanism survives missing tool outputs."],
                "section_plan": [{"section": "方法主線", "evidence_sources": [{"section_id": "sec:method"}]}],
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "scripts" / "lint_note.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--input",
            str(note_path),
            "--plan-file",
            str(plan_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["passes_style_gate"] is False
    assert "mechanical_translation_artifacts_present" in payload["warnings"]
    assert payload["mechanical_translation_artifact_issues"]


def test_note_plan_empty_required_values_fail_plan_gate(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    plan_path = tmp_path / "Paper.plan.json"
    note_path.write_text(_valid_note_text(), encoding="utf-8")
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "",
                "paper_type_rationale": "",
                "dominant_domain": "   ",
                "must_cover": [],
                "key_numbers": [],
                "real_comparisons": [],
                "central_claims": [],
                "claim_boundaries": [],
                "negative_or_limiting_results": [],
                "mechanism_result_map": [],
                "comparative_positioning": [],
                "reuse_takeaways": [],
                "followup_questions": [],
                "section_plan": [],
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "scripts" / "lint_note.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--input", str(note_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["planning_artifact_found"] is True
    assert payload["passes_plan_gate"] is False
    assert payload["planning_artifact_issues"] == [
        "planning_paper_type_empty",
        "planning_paper_type_rationale_empty",
        "planning_dominant_domain_empty",
        "planning_must_cover_empty",
        "planning_key_numbers_empty",
        "planning_real_comparisons_empty",
        "planning_central_claims_empty",
        "planning_claim_boundaries_empty",
        "planning_negative_or_limiting_results_empty",
        "planning_mechanism_result_map_empty",
        "planning_comparative_positioning_empty",
        "planning_reuse_takeaways_empty",
        "planning_followup_questions_empty",
        "planning_section_plan_empty",
    ]


def test_note_plan_explicit_not_reported_entries_pass_plan_gate(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    plan_path = tmp_path / "Paper.plan.json"
    note_path.write_text(_valid_note_text(), encoding="utf-8")
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "The paper proposes a model mechanism and evaluates it experimentally.",
                "dominant_domain": "reasoning",
                "must_cover": ["方法主線"],
                "key_numbers": ["論文未報告明確核心數字"],
                "real_comparisons": ["論文未提供直接對比"],
                "central_claims": [
                    {
                        "claim": "The paper offers a method mechanism.",
                        "supporting_evidence": [{"section_id": "sec:method"}],
                        "what_it_actually_proves": "The mechanism is described in source sections.",
                        "what_it_does_not_prove": "It does not prove all deployment cases.",
                    }
                ],
                "claim_boundaries": ["The comparison evidence is limited."],
                "negative_or_limiting_results": ["論文未清楚報告負向消融。"],
                "mechanism_result_map": ["The state log explains why errors can be recovered."],
                "comparative_positioning": ["The method is positioned against answer-only tool use."],
                "reuse_takeaways": ["Use explicit state logs when evaluating tool chains."],
                "followup_questions": ["Test the state log with slower external tools."],
                "section_plan": [{"section": "方法主線"}],
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "scripts" / "lint_note.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--input", str(note_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["planning_artifact_issues"] == []
    assert payload["passes_plan_gate"] is True


def test_write_note_output_refuses_failed_plan_gate(tmp_path) -> None:
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(
        json.dumps(
            {
                "passes_basic_structure": True,
                "passes_style_gate": True,
                "passes_math_gate": True,
                "passes_figure_gate": True,
                "passes_plan_gate": False,
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "scripts" / "write_note_output.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Plan Gate Paper",
            "--content",
            "# Plan Gate Paper",
            "--lint-json",
            str(lint_path),
            "--vault",
            str(tmp_path / "vault"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "plan gate failed" in result.stderr


def test_real_image_embed_counts_as_figure_marker_in_full_lint(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    note_path.write_text(
        """# Paper

## 核心資訊

這是一條完整元資訊佔位。

## 原文摘要翻譯

這是一段中文摘要翻譯。

## 創新點

這裡記錄論文的具體創新。

## 一句話總結

這篇論文解決一個清晰問題。

## 研究問題

問題邊界描述清楚。

## 資料與任務定義

任務輸入和輸出定義清楚。

## 方法主線

### 執行流程

這裡說明方法過程。

![Fig. 1](../img/Paper/page_001_fig_figure_1.png)
*論文原圖編號：Fig. 1。方法流程圖。*

## 關鍵結果

結果部分記錄關鍵發現。

## 深度分析

分析部分說明為什麼成立。

## 侷限

這裡記錄限制。

## 我的筆記

這裡記錄個人理解。

## 引用

這裡記錄引用資訊。
""",
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "scripts" / "lint_note.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--input", str(note_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert "no_figure_markers" not in payload["warnings"]
    assert payload["passes_figure_gate"] is True
    assert payload["passes_substantive_content"] is False
    assert any(
        issue["reason"] == "innovation_empty_shell"
        for issue in payload["substantive_content_issues"]
    )


def test_write_note_output_refuses_failed_substantive_gate(tmp_path) -> None:
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(
        json.dumps(
            {
                "passes_basic_structure": True,
                "passes_style_gate": True,
                "passes_math_gate": True,
                "passes_figure_gate": True,
                "passes_plan_gate": True,
                "passes_substantive_content": False,
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "scripts" / "write_note_output.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Substantive Gate Paper",
            "--content",
            "# Substantive Gate Paper",
            "--lint-json",
            str(lint_path),
            "--vault",
            str(tmp_path / "vault"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "substantive content gate failed" in result.stderr


def passing_lint_payload() -> dict:
    return {
        "passes_basic_structure": True,
        "passes_style_gate": True,
        "passes_math_gate": True,
        "passes_figure_gate": True,
        "passes_plan_gate": True,
        "passes_substantive_content": True,
    }


def test_write_note_output_materializes_insert_decision(tmp_path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    source_image = tmp_path / "page_001_fig_figure_1.png"
    source_image.write_bytes(b"fake-png")
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(json.dumps(passing_lint_payload()), encoding="utf-8")
    decisions_path = tmp_path / "figure_decisions.json"
    decisions_path.write_text(
        json.dumps(
            {
                "decisions": [
                    {
                        "source_id": "Figure 1",
                        "decision": "insert",
                        "source_image_path": str(source_image),
                        "source_image_filename": source_image.name,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    output_path = tmp_path / "write.json"
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "write_note_output.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Figure Insert Paper",
            "--filename",
            "Figure Insert Paper.md",
            "--subdir",
            "Research/Papers/Figure Insert Paper",
            "--content",
            "# Figure Insert Paper\n\n![Figure 1](images/page_001_fig_figure_1.png)\n*Fig. 1 caption.*\n",
            "--lint-json",
            str(lint_path),
            "--figure-decisions",
            str(decisions_path),
            "--vault",
            str(vault),
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))

    materialized = payload["materialized_figures"][0]
    assert materialized["relative_markdown_path"] == "images/page_001_fig_figure_1.png"
    assert Path(materialized["dest_image_path"]).read_bytes() == b"fake-png"


def test_write_note_output_rejects_unreferenced_insert_decision(tmp_path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    source_image = tmp_path / "page_001_fig_figure_1.png"
    source_image.write_bytes(b"fake-png")
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(json.dumps(passing_lint_payload()), encoding="utf-8")
    decisions_path = tmp_path / "figure_decisions.json"
    decisions_path.write_text(
        json.dumps(
            {
                "decisions": [
                    {
                        "source_id": "Figure 1",
                        "decision": "insert",
                        "source_image_path": str(source_image),
                        "source_image_filename": source_image.name,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "write_note_output.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Figure Insert Paper",
            "--content",
            "# Figure Insert Paper\n\n正文沒有引用圖片。\n",
            "--lint-json",
            str(lint_path),
            "--figure-decisions",
            str(decisions_path),
            "--vault",
            str(vault),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "is not referenced as an image embed" in result.stderr


def test_write_note_output_rejects_plain_path_for_insert_decision(tmp_path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    source_image = tmp_path / "page_001_fig_figure_1.png"
    source_image.write_bytes(b"fake-png")
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(json.dumps(passing_lint_payload()), encoding="utf-8")
    decisions_path = tmp_path / "figure_decisions.json"
    decisions_path.write_text(
        json.dumps(
            {
                "decisions": [
                    {
                        "source_id": "Figure 1",
                        "decision": "insert",
                        "source_image_path": str(source_image),
                        "source_image_filename": source_image.name,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "write_note_output.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Figure Insert Paper",
            "--content",
            "# Figure Insert Paper\n\n正文只提到 images/page_001_fig_figure_1.png 這個路徑。\n",
            "--lint-json",
            str(lint_path),
            "--figure-decisions",
            str(decisions_path),
            "--vault",
            str(vault),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "is not referenced as an image embed" in result.stderr


def test_write_note_output_rejects_unsafe_insert_filename(tmp_path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    source_image = tmp_path / "page_001_fig_figure_1.png"
    source_image.write_bytes(b"fake-png")
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(json.dumps(passing_lint_payload()), encoding="utf-8")
    decisions_path = tmp_path / "figure_decisions.json"
    decisions_path.write_text(
        json.dumps(
            {
                "decisions": [
                    {
                        "source_id": "Figure 1",
                        "decision": "insert",
                        "source_image_path": str(source_image),
                        "source_image_filename": "../escaped.png",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "write_note_output.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Figure Insert Paper",
            "--content",
            "# Figure Insert Paper\n\n![Figure 1](images/../escaped.png)\n*Fig. 1 caption.*\n",
            "--lint-json",
            str(lint_path),
            "--figure-decisions",
            str(decisions_path),
            "--vault",
            str(vault),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Unsafe figure image filename" in result.stderr


def test_inspect_note_plan_reports_missing_file(tmp_path) -> None:
    found, issues = inspect_note_plan(tmp_path / "missing.plan.json")
    assert found is False
    assert issues == ["planning_artifact_missing"]


def test_inspect_note_plan_reports_invalid_json(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text("{not-json", encoding="utf-8")

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert issues == ["planning_artifact_invalid_json"]


def test_inspect_note_plan_reports_missing_required_fields(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text(json.dumps({"paper_type": "AI_method"}), encoding="utf-8")

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert "planning_required_fields_missing" in issues


def test_inspect_note_plan_rejects_invalid_paper_type(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "method",
                "paper_type_rationale": "The model-facing plan should use the shared paper type enum.",
                "dominant_domain": "reasoning",
                "must_cover": ["方法主線"],
                "key_numbers": ["42"],
                "real_comparisons": ["baseline"],
                "central_claims": [
                    {
                        "claim": "The method improves a target behavior.",
                        "supporting_evidence": [{"section_id": "sec:method"}],
                        "what_it_actually_proves": "The source states the mechanism and reported setting.",
                        "what_it_does_not_prove": "It does not prove all deployment cases.",
                    }
                ],
                "claim_boundaries": ["The claim is limited to reported settings."],
                "negative_or_limiting_results": ["No external failure case is reported."],
                "mechanism_result_map": ["The mechanism explains the reported target behavior."],
                "comparative_positioning": ["The plan names the relevant baseline comparison."],
                "reuse_takeaways": ["Track the mechanism separately from the final result."],
                "followup_questions": ["Check whether the mechanism transfers to a new dataset."],
                "section_plan": [{"section": "方法主線"}],
            }
        ),
        encoding="utf-8",
    )

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert "planning_paper_type_invalid" in issues


def test_inspect_note_plan_reports_invalid_field_types(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "The paper proposes a model mechanism.",
                "dominant_domain": "reasoning",
                "must_cover": "method",
                "key_numbers": [],
                "real_comparisons": [],
                "central_claims": "not-a-list",
                "claim_boundaries": [],
                "negative_or_limiting_results": [],
                "mechanism_result_map": [],
                "comparative_positioning": [],
                "reuse_takeaways": [],
                "followup_questions": [],
                "section_plan": [{"section": "方法主線"}],
            }
        ),
        encoding="utf-8",
    )

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert "planning_required_fields_invalid" in issues


def test_inspect_note_plan_reports_empty_section_plan(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "The paper proposes a model mechanism.",
                "dominant_domain": "reasoning",
                "must_cover": [],
                "key_numbers": [],
                "real_comparisons": [],
                "central_claims": [],
                "claim_boundaries": [],
                "negative_or_limiting_results": [],
                "mechanism_result_map": [],
                "comparative_positioning": [],
                "reuse_takeaways": [],
                "followup_questions": [],
                "section_plan": [],
            }
        ),
        encoding="utf-8",
    )

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert issues == [
        "planning_must_cover_empty",
        "planning_key_numbers_empty",
        "planning_real_comparisons_empty",
        "planning_central_claims_empty",
        "planning_claim_boundaries_empty",
        "planning_negative_or_limiting_results_empty",
        "planning_mechanism_result_map_empty",
        "planning_comparative_positioning_empty",
        "planning_reuse_takeaways_empty",
        "planning_followup_questions_empty",
        "planning_section_plan_empty",
    ]


def test_inspect_note_plan_accepts_valid_plan(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "The paper proposes a model mechanism.",
                "dominant_domain": "reasoning",
                "must_cover": ["方法主線"],
                "key_numbers": ["42"],
                "real_comparisons": ["baseline"],
                "central_claims": [
                    {
                        "claim": "The method improves a target behavior.",
                        "supporting_evidence": [{"section_id": "sec:method"}],
                        "what_it_actually_proves": "The source states the mechanism and reported setting.",
                        "what_it_does_not_prove": "It does not prove all deployment cases.",
                    }
                ],
                "claim_boundaries": ["The claim is limited to reported settings."],
                "negative_or_limiting_results": ["No external failure case is reported."],
                "mechanism_result_map": ["The mechanism explains the reported target behavior."],
                "comparative_positioning": ["The plan names the relevant baseline comparison."],
                "reuse_takeaways": ["Track the mechanism separately from the final result."],
                "followup_questions": ["Check whether the mechanism transfers to a new dataset."],
                "section_plan": [{"section": "方法主線"}],
            }
        ),
        encoding="utf-8",
    )

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert issues == []
