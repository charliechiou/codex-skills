#!/usr/bin/env python3
"""Scaffolded JSON contracts for the paper-deep-notes core workflow."""

from __future__ import annotations

from typing import Any, TypedDict

NOTE_REQUIRED_SECTIONS: tuple[str, ...] = (
    "核心資訊",
    "原文摘要翻譯",
    "創新點",
    "一句話總結",
    "研究問題",
    "資料與任務定義",
    "方法主線",
    "關鍵結果",
    "深度分析",
    "侷限",
    "我的筆記",
    "引用",
)

PAPER_TYPE_VALUES: tuple[str, ...] = (
    "AI_method",
    "benchmark_or_dataset",
    "clinical_or_psychology_empirical",
    "humanities_or_social_science",
    "survey_or_review",
)

NOTE_PLAN_STRING_FIELDS: tuple[str, ...] = (
    "paper_type",
    "paper_type_rationale",
    "dominant_domain",
)

NOTE_PLAN_LIST_FIELDS: tuple[str, ...] = (
    "must_cover",
    "key_numbers",
    "real_comparisons",
    "central_claims",
    "claim_boundaries",
    "negative_or_limiting_results",
    "mechanism_result_map",
    "comparative_positioning",
    "reuse_takeaways",
    "followup_questions",
    "section_plan",
)

NOTE_PLAN_REQUIRED_FIELDS: tuple[str, ...] = NOTE_PLAN_STRING_FIELDS + NOTE_PLAN_LIST_FIELDS

PAPER_TYPE_SECTION_PROFILES: dict[str, dict[str, dict[str, Any]]] = {
    "AI_method": {
        "section_semantics": {
            "研究問題": "方法要解決的具體技術問題和現有方法短板。",
            "資料與任務定義": "資料集、輸入輸出、評測任務和實驗設定。",
            "方法主線": "模型、演算法、訓練或推理機制。",
            "關鍵結果": "主結果、強基線、消融和關鍵數字。",
            "深度分析": "方法為什麼有效、何處脆弱、重現和擴充套件代價。",
        },
        "recommended_subsections": {
            "方法主線": ["機制流程", "模型結構", "訓練目標", "推理與取樣鏈路", "關鍵實現細節"],
            "關鍵結果": ["主結果與強基線", "消融到底說明瞭什麼", "失敗或不穩定設定"],
            "深度分析": ["為什麼有效", "複雜度與擴充套件性", "重現注意點"],
        },
    },
    "benchmark_or_dataset": {
        "section_semantics": {
            "研究問題": "這個 benchmark/dataset 想補足的評測或資料缺口。",
            "資料與任務定義": "資料來源、任務拆分、標籤/題目定義、樣本範圍。",
            "方法主線": "資料建構、篩選、標註和評測協議，不寫成模型 pipeline。",
            "關鍵結果": "基線表現、難度分佈、覆蓋範圍和偏差。",
            "深度分析": "它真正測到了什麼，以及不能代表什麼。",
        },
        "recommended_subsections": {
            "資料與任務定義": ["資料來源", "任務拆分", "標註/篩選協議"],
            "方法主線": ["建構流程", "評測協議", "Baseline 設定"],
            "關鍵結果": ["基線表現", "難度分佈", "覆蓋與偏差"],
            "深度分析": ["benchmark 真正測到了什麼", "適用邊界"],
        },
    },
    "clinical_or_psychology_empirical": {
        "section_semantics": {
            "研究問題": "臨床、心理學或行為科學中的研究問題、假設或變數關係。",
            "資料與任務定義": "樣本來源、納排標準、變數/量表、測量方式。",
            "方法主線": "研究設計、分組、測量流程和統計分析路徑。",
            "關鍵結果": "主要效應、相關性、組間差異、不確定性或顯著性。",
            "深度分析": "結果解釋、因果邊界、臨床/心理學意義和外推限制。",
        },
        "recommended_subsections": {
            "資料與任務定義": ["樣本與納排標準", "變數與量表", "測量流程"],
            "方法主線": ["研究設計", "分析模型", "主要比較"],
            "關鍵結果": ["主要效應", "不確定性與顯著性", "臨床或心理學解釋"],
            "深度分析": ["因果解釋邊界", "外推限制"],
        },
    },
    "humanities_or_social_science": {
        "section_semantics": {
            "研究問題": "作者要解釋的社會、文化、歷史、制度或理論問題。",
            "資料與任務定義": "材料、案例、文字、訪談、檔案或語料範圍，不寫成 ML task。",
            "方法主線": "理論框架、概念區分和論證路徑。",
            "關鍵結果": "核心解釋性發現、概念貢獻或對既有觀點的修正。",
            "深度分析": "論證強度、材料邊界、解釋替代性和可遷移性。",
        },
        "recommended_subsections": {
            "資料與任務定義": ["材料範圍", "選擇標準", "案例或語料邊界"],
            "方法主線": ["理論框架", "概念區分", "論證路徑"],
            "關鍵結果": ["核心解釋性發現", "概念貢獻"],
            "深度分析": ["論證強度", "替代解釋", "材料邊界"],
        },
    },
    "survey_or_review": {
        "section_semantics": {
            "研究問題": "綜述試圖整理的領域問題、爭議或知識缺口。",
            "資料與任務定義": "納入文獻範圍、檢索/篩選標準和綜述物件。",
            "方法主線": "分類體系、綜述組織方式和證據綜合邏輯，不寫成單篇方法架構。",
            "關鍵結果": "領域共識、分歧、趨勢、代表性方向和開放問題。",
            "深度分析": "綜述覆蓋的盲區、分類體系的解釋力和未來研究機會。",
        },
        "recommended_subsections": {
            "資料與任務定義": ["綜述範圍", "納入/排除標準", "文獻覆蓋"],
            "方法主線": ["分類體系", "方法譜系", "證據組織方式"],
            "關鍵結果": ["代表性方向", "共識與分歧", "開放問題"],
            "深度分析": ["分類體系的侷限", "未覆蓋區域", "後續研究機會"],
        },
    },
}

PAPER_TYPE_CONTRACTS: dict[str, dict[str, Any]] = {
    "AI_method": {
        "paper_type": "AI_method",
        "reader_lens": "面向能重現方法機制的技術讀者",
        "section_focus": [
            "問題設定",
            "方法機制",
            "訓練/推理流程",
            "關鍵公式",
            "比較基線",
            "消融與失敗邊界",
        ],
        "required_checks": ["需要說明機制流程、關鍵公式、實驗設計、消融含義和失敗邊界。"],
        "formula_rules": ["僅保留理解方法必需的 1 到 3 個關鍵公式，並解釋其工程含義。"],
        "avoid_rules": ["不要把非 AI_method 論文強行改寫成模型架構。"],
        "boundary_questions": [
            "核心機制的收益由哪個實驗或消融支撐，而不是隻由主結果暗示？",
            "哪些比較只能證明在當前資料、基線、算力或協議下有效，不能外推到通用場景？",
            "論文是否給出失敗、退化、不穩定或成本上升的證據；如果沒有，結論邊界是什麼？",
        ],
        **PAPER_TYPE_SECTION_PROFILES["AI_method"],
        "mechanism_flow_contract": {
            "apply_when_paper_type_in": ["AI_method"],
            "required_step_count": "3_to_4",
            "required_step_fields": ["input", "operation", "output_destination"],
        },
    },
    "benchmark_or_dataset": {
        "paper_type": "benchmark_or_dataset",
        "reader_lens": "面向要判斷 benchmark/dataset 可用性和偏差邊界的研究者",
        "section_focus": [
            "任務拆分",
            "資料來源與建構流程",
            "標註協議",
            "評測指標",
            "覆蓋範圍與偏差",
            "樣本統計與資料開放限制",
        ],
        "required_checks": [
            "需要說明資料來源、建構/標註流程、評測指標、基線表現、樣本統計、資料開放或隱私限制和適用邊界。"
        ],
        "formula_rules": ["僅保留核心評測指標、取樣規則或劃分定義。"],
        "avoid_rules": ["不要把資料建構流程寫成模型 pipeline。"],
        "boundary_questions": [
            "這個 benchmark/dataset 實際測量的構念是什麼，哪些能力只是間接近似？",
            "任務、標籤、取樣、過濾或評測協議會引入哪些覆蓋缺口或偏差？",
            "基線結果證明了評測集有區分度，還是隻證明某類模型適應該協議？",
            "樣本時長、語料長度、人口統計、類別分佈、資料可訪問性或隱私限制如何影響重現和外推？",
        ],
        **PAPER_TYPE_SECTION_PROFILES["benchmark_or_dataset"],
    },
    "clinical_or_psychology_empirical": {
        "paper_type": "clinical_or_psychology_empirical",
        "reader_lens": "面向關注臨床/心理學樣本、變數關係和外推邊界的研究讀者",
        "section_focus": [
            "樣本來源",
            "納排標準",
            "變數或量表",
            "分析管線",
            "效應量與不確定性",
            "樣本統計、倫理和資料可訪問性",
        ],
        "required_checks": [
            "需要區分相關、預測、組間差異和因果解釋，說明樣本統計、倫理/隱私約束與外推邊界。"
        ],
        "formula_rules": ["僅保留核心統計模型、效應量、置信區間或量表定義。"],
        "avoid_rules": ["不要把相關性、預測效能或組間差異寫成未經證明的因果結論。"],
        "boundary_questions": [
            "樣本來源、納排標準、測量工具和標註流程如何限制外推？",
            "結果支援相關、預測、組間差異還是因果解釋；不要越過論文設計能證明的範圍。",
            "臨床或心理學意義是否依賴未觀測混雜、量表閾值、文字/語音缺失或場景約束？",
            "樣本構成、資料缺失、隱私限制或材料不可公開會怎樣限制重現與再分析？",
        ],
        **PAPER_TYPE_SECTION_PROFILES["clinical_or_psychology_empirical"],
    },
    "humanities_or_social_science": {
        "paper_type": "humanities_or_social_science",
        "reader_lens": "面向關注理論框架、材料解釋和論證結構的研究讀者",
        "section_focus": ["研究物件", "材料來源", "理論框架", "論證路徑", "概念貢獻", "解釋邊界"],
        "required_checks": ["需要區分作者論證、材料證據、規範性判斷和實驗事實。"],
        "formula_rules": ["通常不強行保留公式；僅保留核心形式化定義或編碼規則。"],
        "avoid_rules": ["不要把規範性判斷、文字解釋或案例分析寫成實驗事實。"],
        "boundary_questions": [
            "作者的解釋依賴哪些材料、案例或理論前提？",
            "是否存在同樣能解釋材料的替代解釋，論文如何排除或沒有排除？",
            "哪些結論是概念貢獻或規範性判斷，而不是可直接當作經驗事實？",
        ],
        **PAPER_TYPE_SECTION_PROFILES["humanities_or_social_science"],
    },
    "survey_or_review": {
        "paper_type": "survey_or_review",
        "reader_lens": "面向需要梳理綜述脈絡、分類體系和證據邊界的研究讀者",
        "section_focus": [
            "綜述範圍",
            "納入排除標準",
            "主題分類",
            "方法譜系",
            "共識與分歧",
            "開放問題",
        ],
        "required_checks": ["需要說明綜述範圍、文獻選擇、分類體系、共識分歧和開放問題。"],
        "formula_rules": ["僅保留分類軸、納入排除準則、證據彙總規則或 meta-analysis 統計量。"],
        "avoid_rules": ["不要把綜述中的代表性結論寫成作者自己完成的單項實驗結果。"],
        "boundary_questions": [
            "檢索範圍、納入排除標準或分類軸會遺漏哪些研究路線？",
            "綜述給出的是領域共識、作者分類，還是尚未解決的分歧？",
            "哪些趨勢結論來自覆蓋範圍內的文獻分佈，不能直接當作技術成熟度判斷？",
        ],
        **PAPER_TYPE_SECTION_PROFILES["survey_or_review"],
    },
}

WRITING_CONTRACT_RULES: dict[str, Any] = {
    "required_sections": NOTE_REQUIRED_SECTIONS,
    "paper_type_values": PAPER_TYPE_VALUES,
    "note_plan_required_fields": NOTE_PLAN_REQUIRED_FIELDS,
    "grounding_required_sections": (
        "研究問題",
        "資料與任務定義",
        "方法主線",
        "關鍵結果",
        "深度分析",
        "侷限",
    ),
    "allowed_grounding_reference_forms": ("section_id", "pages"),
    "old_bundle_reference_prefixes": (
        "synthesis_bundle.evidence",
        "bundle.evidence",
        "synthesis_bundle.candidate_chunks",
        "synthesis_bundle.section_texts",
        "synthesis_bundle.summary",
        "bundle.candidate_chunks",
        "bundle.section_texts",
        "bundle.summary",
    ),
    "old_evidence_reference_tokens": (
        "evidence_pack",
        "summary.paper_type",
        "problem_evidence",
        "task_evidence",
        "data_evidence",
        "method_evidence",
        "mechanism_evidence",
        "results_evidence",
        "ablation_evidence",
        "limitations_evidence",
        "candidate_chunks",
        "section_texts",
    ),
    "figure_decision_values": ("insert", "placeholder", "low_priority", "visual_defect", "skip"),
    "usable_insert_candidate": {
        "kinds": ("figure", "table"),
        "visual_quality_status": "usable_candidate",
        "requires_source_image_path": True,
    },
    "allowed_usable_placeholder_reasons": (
        "visual_defect",
        "materialization_blocked",
    ),
    "manual_visual_review_required_statuses": (
        "usable_candidate",
        "needs_visual_quality_check",
        "review",
    ),
    "automatic_fail_closed_visual_statuses": (
        "reject_visual_quality",
        "asset_candidate_missing",
    ),
    "note_plan_depth_requirements": {
        "required_section_focus_min_chars": 20,
        "required_section_focus_fields": ("focus", "reading_goal", "purpose"),
        "generic_focus_phrases": (
            "use the raw source to explain",
            "paper-specific role of",
            "explain the paper-specific role",
            "explain this section",
            "summarize this section",
        ),
    },
    "analysis_coverage_contract": {
        "central_claim_fields": (
            "claim",
            "supporting_evidence",
            "what_it_actually_proves",
            "what_it_does_not_prove",
        ),
        "required_plan_fields": (
            "central_claims",
            "claim_boundaries",
            "negative_or_limiting_results",
            "mechanism_result_map",
            "comparative_positioning",
            "reuse_takeaways",
            "followup_questions",
        ),
        "final_quality_review_checks": (
            "central_claims_are_supported_by_raw_sections_or_pages",
            "key_experimental_settings_and_numbers_are_present",
            "mechanisms_or_protocol_choices_are_mapped_to_results",
            "comparisons_explain_positioning_against_alternatives",
            "discussion_or_limitation_claims_are_explained_mechanistically",
            "proven_claims_are_separated_from_unproven_or_unvalidated_claims",
            "research_or_engineering_takeaways_are_specific_and_reusable",
            "followup_questions_are_specific_to_replication_or_extension",
        ),
    },
}


class MetadataRecord(TypedDict, total=False):
    title: str
    translated_title: str
    paper_id: str
    source_type: str
    source_url: str
    year: str
    authors: list[str]
    affiliations: list[str]
    venue: str
    doi: str
    abstract: str
    code_url: str
    project_url: str
    zotero_key: str
    arxiv_id: str
    metadata_sources: list[str]
    identity_confidence: str
    identity_confidence_reasons: list[str]


class EvidenceItem(TypedDict, total=False):
    claim: str
    evidence: str
    source_section: str
    page_hint: str


class CandidateChunk(TypedDict, total=False):
    text: str
    source_section: str
    actual_source_section: str
    is_abstract_fallback: bool
    page_hint: str
    kind_hint: str


class EquationCandidate(TypedDict, total=False):
    equation: str
    source_section: str
    kind_hint: str


class ReferenceCandidate(TypedDict, total=False):
    raw_text: str
    display_text: str
    page_hint: str
    doi: str
    arxiv_id: str
    wikilink: str
    vault_target: str
    match_status: str
    match_reason: str


class FigureQualitySignals(TypedDict, total=False):
    visual_quality_status: str
    quality_reason_codes: list[str]
    page_coverage_ratio: float
    visual_rect_count: int
    visual_body_ratio: float
    paragraph_text_chars: int
    table_body_rows: int
    caption_text_chars: int


class FigureAssetCandidate(TypedDict, total=False):
    filename: str
    path: str
    width: int
    height: int
    size_bytes: int
    label: str
    extraction_level: str
    quality_signals: FigureQualitySignals
    candidate_status: str


class SectionExtractionCoverage(TypedDict, total=False):
    coverage_status: str
    recognized_sections: list[str]
    core_sections_found: list[str]
    missing_core_sections: list[str]
    section_text_chars: dict[str, int]
    fallback_sections: list[str]


class PdfCoverage(TypedDict, total=False):
    total_pages: int | None
    text_max_pages: int | None
    text_pages_scanned: int
    truncated_due_to_page_limit: bool
    appendix_detected: bool
    appendix_start_page: int | None
    references_start_page: int | None
    section_stop_reason: str
    section_stop_page: int | None


class AppendixIndex(TypedDict, total=False):
    appendix_detected: bool
    start_page: int | None
    sections: list[dict[str, Any]]
    figure_captions: list[dict[str, Any]]
    table_captions: list[dict[str, Any]]


class AppendixEvidenceItem(TypedDict, total=False):
    evidence: str
    source_section: str
    page_hint: str
    kind_hint: str


class EvidencePack(TypedDict, total=False):
    paper_id: str
    problem_evidence: list[EvidenceItem]
    task_evidence: list[EvidenceItem]
    data_evidence: list[EvidenceItem]
    method_evidence: list[EvidenceItem]
    mechanism_evidence: list[EvidenceItem]
    results_evidence: list[EvidenceItem]
    ablation_evidence: list[EvidenceItem]
    limitations_evidence: list[EvidenceItem]
    equation_candidates: list[EquationCandidate]
    reference_candidates: list[ReferenceCandidate]
    figure_captions: list[dict[str, Any]]
    table_captions: list[dict[str, Any]]
    sections: list[dict[str, Any]]
    section_texts: dict[str, str]
    candidate_chunks: dict[str, list[CandidateChunk]]
    language_hint: str
    section_sources: dict[str, str]
    section_extraction_coverage: SectionExtractionCoverage
    pdf_coverage: PdfCoverage
    appendix_index: AppendixIndex
    appendix_evidence: dict[str, list[AppendixEvidenceItem]]
    quotes: list[dict[str, Any]]
    evidence_quality: str
    extraction_failures: list[str]


class FigurePlanItem(TypedDict, total=False):
    id: str
    caption: str
    kind: str
    section: str
    reason: str
    priority: int
    anchor_text: str
    insert_mode: str
    figure_asset_candidate: FigureAssetCandidate
    candidate_pages: list[dict[str, Any]]
    candidate_status: str
    matching_strategy: str


class FigurePlan(TypedDict, total=False):
    paper_id: str
    figures: list[FigurePlanItem]


class SynthesisBundle(TypedDict, total=False):
    paper_id: str
    title: str
    metadata: dict[str, Any]
    evidence_quality: str
    coverage: dict[str, Any]
    source_manifest: dict[str, Any]
    source_index: dict[str, Any]
    references: dict[str, Any]
    figure_plan: dict[str, Any]
    figure_table_manifest: dict[str, Any]
    pdf_assets: dict[str, Any]
    writing_contract: dict[str, Any]


def empty_metadata() -> MetadataRecord:
    return MetadataRecord(
        title="",
        paper_id="",
        source_type="",
        source_url="",
        year="",
        authors=[],
        affiliations=[],
        metadata_sources=[],
        identity_confidence="",
        identity_confidence_reasons=[],
    )


def empty_evidence_pack() -> EvidencePack:
    return EvidencePack(
        paper_id="",
        problem_evidence=[],
        task_evidence=[],
        data_evidence=[],
        method_evidence=[],
        mechanism_evidence=[],
        results_evidence=[],
        ablation_evidence=[],
        limitations_evidence=[],
        equation_candidates=[],
        reference_candidates=[],
        figure_captions=[],
        table_captions=[],
        sections=[],
        section_texts={},
        candidate_chunks={},
        language_hint="unknown",
        section_sources={},
        section_extraction_coverage={},
        pdf_coverage={},
        appendix_index={},
        appendix_evidence={},
        quotes=[],
        extraction_failures=[],
        evidence_quality="unknown",
    )


def empty_figure_plan() -> FigurePlan:
    return FigurePlan(paper_id="", figures=[])


def empty_synthesis_bundle() -> SynthesisBundle:
    return SynthesisBundle(
        paper_id="",
        title="",
        metadata={},
        evidence_quality="unknown",
        coverage={},
        source_manifest={},
        source_index={},
        references={},
        figure_plan={},
        figure_table_manifest={},
        pdf_assets={},
        writing_contract={},
    )
