import argparse
import ast
from html.parser import HTMLParser
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_CHAPTERS = 10
EXPECTED_SECTIONS = 127
EXPECTED_EXERCISES = "103"
EXPECTED_INTERACTIVE_EXERCISES = 50
MIN_HTML_ANCHOR_LINKS = 10
MIN_MARKDOWN_ANCHOR_LINKS = 10
EXPECTED_CONCEPT_IMAGES = [
    "attention-flow.svg",
    "bpe-pipeline.svg",
    "gpt-params.svg",
    "gpu-memory.svg",
    "mha-gqa-mla.svg",
    "rlhf-dpo-grpo.svg",
    "rope-rotation.svg",
    "sampling-strategies.svg",
    "training-loop.svg",
    "transformer-arch.svg",
    "transformer-block.svg",
]
RENDER_SMOKE_PAGES = ["index.html"] + [f"chapters/ch{chapter:02d}.html" for chapter in range(1, EXPECTED_CHAPTERS + 1)]
EXPECTED_ASSIGNMENTS = [
    "ch01_bpe",
    "ch02_embeddings",
    "ch03_attention",
    "ch04_multihead",
    "ch05_block",
    "ch06_gpt",
    "ch07_training",
    "ch08_generation",
    "ch09_alignment",
    "ch10_inference",
    "ch11_classic_nlp",
]
EXPECTED_CONCEPT_MODULES = [
    "Ch01 Tokenization / BPE",
    "Ch02 Embedding / Position Encoding / RoPE",
    "Ch03 Scaled Dot-Product Attention",
    "Ch04 MHA / GQA / MLA",
    "Ch05 Transformer Block / Norm / FFN",
    "Ch06 GPT Assembly / MoE",
    "Ch07 Training Loop",
    "Ch08 Generation / Decoding",
    "Ch09 SFT / LoRA / DPO / GRPO",
    "Ch10 Inference / RAG / Serving",
    "Ch11 Classic NLP / Evaluation",
]
EXPECTED_AUTOGRADER_SECTIONS = [
    "Ch01 Tokenization / BPE",
    "Ch02 Embedding / Position Encoding / RoPE",
    "Ch03 Scaled Dot-Product Attention",
    "Ch04 MHA / GQA / MLA",
    "Ch05 Transformer Block / Norm / FFN",
    "Ch06 GPT Assembly / MoE",
    "Ch07 Training Loop",
    "Ch08 Generation / Decoding",
    "Ch09 Fine-tuning / Alignment",
    "Ch10 Inference / RAG / Serving",
    "Ch11 Classic NLP and Evaluation",
]
EXPECTED_WRITTEN_ASSESSMENT_SECTIONS = [
    ("Ch01 Tokenization / BPE", "Ch01 Tokenization / BPE", 3),
    ("Ch02 Embedding / Position Encoding / RoPE", "Ch02 Embedding / Position Encoding / RoPE", 3),
    ("Ch03 Scaled Dot-Product Attention", "Ch03 Scaled Dot-Product Attention", 3),
    ("Ch04 MHA / GQA / MLA", "Ch04 MHA / GQA / MLA", 3),
    ("Ch05 Transformer Block / Norm / FFN", "Ch05 Transformer Block / Norm / FFN", 3),
    ("Ch06 GPT Assembly / MoE", "Ch06 GPT Assembly / MoE", 3),
    ("Ch07 Training Loop", "Ch07 Training Loop", 4),
    ("Ch08 Generation / Decoding", "Ch08 Generation / Decoding", 4),
    ("Ch09 Fine-tuning / Alignment", "Ch09 Fine-tuning / Alignment", 4),
    ("Ch10 Inference / RAG / Serving", "Ch10 Inference / RAG / Serving", 5),
    ("经典 NLP 专题题", "经典 NLP 专题", 5),
]
CHAPTER_QUALITY_MARKERS = [
    "学习目标",
    "课前阅读",
    "课后阅读",
    "评估证据",
]
CHAPTER_SOURCE_GUIDANCE_MARKERS = [
    "本章来源与准确性复核",
    "../docs/chapter-source-map.md",
    "../docs/reading-list.md",
    "../docs/external-source-inventory.md",
    "../docs/external-source-verification.md",
    "../docs/claim-audit-worksheet.md",
]
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HTML_MARKDOWN_DOC_LINK_RE = re.compile(r"\[[^\]\n]+\]\((?:\.\./docs/|docs/|[^)\s]+\.md)(?:#[^)]+)?\)")
EXTERNAL_LINK_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
)
HTML_SKIP_LINK_PREFIXES = EXTERNAL_LINK_PREFIXES + (
    "javascript:",
    "data:",
    "#",
)
ALLOWED_CONTROL_CHARS = {"\n", "\r", "\t"}
MALFORMED_DATA_EXPR_RE = re.compile(r'data-expr="[^"]*"[^ >][^>]*>')
MALFORMED_EXERCISE_ATTR_RE = re.compile(r'<div class="exercise"[^>]*data-explain="[^"]*"[^>]*[\u4e00-\u9fffA-Za-z][^>]*>')
SUSPICIOUS_FORMULA_TEXT_RE = re.compile(
    r"\\text\{vec\("
    r"|\\text\{[^}\n]*(?:——|—|–)"
    r"|\\(?:operatorname|mathrm|mathbf|mathbb|mathcal|text)\{[^}\n]*$"
)
EXTERNAL_URL_RE = re.compile(r"https?://[^\s\"'<>`)]+")
UNRESOLVED_RELEASE_PLACEHOLDER_RE = re.compile(r"\b(?:TODO|Todo|TBD|FIXME)\b|待填|待补|待完善|暂缺|占位|YYYY-MM-DD")
BARE_COURSE_COMMAND_RE = re.compile(
    r"(?<!\.venv/bin/)python\s+(?:verify_course\.py|run_assignment_tests\.py|assignments/|tests\.py)"
)
VISIBLE_TEX_COMMAND_RE = re.compile(
    r"\\(?:text|operatorname|frac|sum|prod|mathbf|mathbb|mathcal|partial|sqrt|cdot|times|"
    r"theta|Theta|infty|leq|geq|approx|log|exp|left|right|top|Delta|nabla|alpha|"
    r"beta|gamma|lambda|mu|sigma|pi|mathsf|mathrm|begin|end)\b"
)
HTML_RAW_TEXT_TAGS = {"script", "style", "pre", "code", "textarea"}
BRACKET_PAIRS = {
    "{": "}",
    "[": "]",
    "(": ")",
}
UNQUALIFIED_CLAIM_PATTERNS = [
    (re.compile(r"贪心 BPE 非常接近最优"), "BPE optimality must be qualified"),
    (re.compile(r"为什么合并最高频 pair 是最优的"), "BPE frequency choice must be framed as a heuristic"),
    (re.compile(r"无衰减.*无损.*反向传播"), "Pre-Norm gradient flow must be qualified"),
    (re.compile(r"残差流完全不受影响"), "Pre-Norm residual claims must be qualified"),
    (re.compile(r"可以训练 1000\+ 层网络"), "depth scalability must be qualified"),
    (re.compile(r"革命性替代"), "frontier architecture claims must be qualified"),
    (re.compile(r"保证训练稳定"), "training stability guarantees must be qualified"),
    (re.compile(r"永远不会超过 1"), "spectral norm claims must state assumptions"),
    (re.compile(r"不会导致梯度爆炸"), "gradient explosion claims must be qualified"),
    (re.compile(r"几乎总是使用"), "training defaults must be qualified"),
    (re.compile(r"被证明对大规模训练最有效"), "learning-rate schedule optimality must be qualified"),
    (re.compile(r"无损[\"'“”]?加速"), "speculative decoding must use distribution-preserving wording"),
    (re.compile(r"完全不使用人类标注的 CoT"), "R1-Zero training-data claims must be source-scoped"),
    (re.compile(r"只要奖励函数设计得当"), "RL outcome claims must be qualified"),
    (re.compile(r"人类不需要知道.*只需要能评判"), "alignment claims must be qualified"),
    (re.compile(r"raw 频率.*互信息最高"), "BPE frequency must not be equated with PMI"),
    (re.compile(r"等价于考虑了 PMI"), "WordPiece/PMI relationship must be described as intuition, not equivalence"),
    (re.compile(r"等价于贪心最长匹配"), "BPE merge-rank encoding must not be equated with generic longest matching"),
    (re.compile(r"编码是贪心最长匹配"), "BPE merge-rank encoding must not be equated with generic longest matching"),
    (re.compile(r"效果极好"), "empirical effectiveness claims must be qualified"),
    (re.compile(r"注意力层对序列顺序完全"), "permutation equivariance must be stated precisely"),
    (re.compile(r"模型内部表示完全等价"), "missing-position claims must distinguish equivariance from equality"),
    (re.compile(r"确保每层.*守恒"), "mHC conservation intuition must be qualified"),
    (re.compile(r"训练更稳定且无需调参"), "MoE routing stability claims must be source-scoped"),
    (re.compile(r"等价于一种.*隐式微调"), "few-shot prompting must not be equated with parameter fine-tuning"),
    (re.compile(r"最简单却最有效的 prompt 技巧"), "prompting techniques must not be ranked without task/model conditions"),
    (re.compile(r"形成[\"“]?自激振荡"), "generation degeneration must not be over-attributed to one attention mechanism"),
    (re.compile(r"无穷无尽的重复输出"), "decoding failure descriptions must be qualified"),
    (re.compile(r"直接转化为更低的训练成本"), "training-system efficiency claims must include workload and cost conditions"),
    (re.compile(r"使 405B 模型可在 128 个 A100 上训练"), "ZeRO examples must not infer trainability from parameter sharding alone"),
    (re.compile(r"所有顶级 LLM 现在都是"), "current model capability claims must be version-scoped"),
    (re.compile(r"实时语音延迟已低于 300ms"), "latency claims must include product version and measurement conditions"),
    (re.compile(r"全是[\"“]?语言"), "multimodal analogies must distinguish sequence modeling from linguistic equivalence"),
    (re.compile(r"PPL = 1.*总是 100% 确定"), "PPL explanations must distinguish limiting cases from real data uncertainty"),
    (re.compile(r"训练稳定性远超 RLHF"), "DPO stability claims must be qualified by data and optimization conditions"),
    (re.compile(r"降低 0\\.2-0\\.5 的困惑度"), "activation-function PPL gains must not be fixed without a specific source and setting"),
    (re.compile(r"指数级收敛.*唯一的双随机矩阵"), "Sinkhorn-Knopp convergence claims must state assumptions and approximation limits"),
    (re.compile(r"点积上限变小.*自然的远程衰减"), "RoPE distance effects must not be stated as guaranteed monotonic score decay"),
    (re.compile(r"点积的上限应降低"), "RoPE distance effects must not be stated as guaranteed monotonic score decay"),
    (re.compile(r"远离对角线时值衰减"), "RoPE score tests must not require monotonic distance decay"),
    (re.compile(r"分数逐渐衰减.*位置衰减"), "RoPE distance effects must not be stated as guaranteed monotonic score decay"),
    (re.compile(r"衰减趋势"), "RoPE examples must not present monotonic decay as the property being verified"),
    (re.compile(r"保证了 RoPE 只编码位置信息而不改变.*语义"), "RoPE norm preservation must not be equated with semantic preservation"),
    (re.compile(r"所有现代 LLM.*Decoder-only"), "decoder-only architecture claims must be scoped to mainstream autoregressive LLMs"),
    (re.compile(r"确保梯度始终在有效范围"), "attention scaling must not guarantee gradients are always effective"),
    (re.compile(r"有效温度.*恒定为 1"), "attention scaling must be stated under variance assumptions"),
    (re.compile(r"实际中不会发生"), "empirical diversity claims must not be absolute"),
    (re.compile(r"矩阵吸收.*免费"), "MLA matrix absorption must not imply free attention or free projection work"),
    (re.compile(r"消除了 PPO 中最不稳定的组件"), "GRPO component simplification must not be stated as a stability guarantee"),
    (re.compile(r"有效解决了不同 prompt 之间奖励尺度不一致"), "GRPO whitening should be framed as mitigation, not complete solution"),
    (re.compile(r"对不同 prompt 的奖励尺度天然鲁棒"), "GRPO robustness must be qualified"),
]
INVENTORY_EXEMPT_DOMAINS = {
    "127.0.0.1",
    "localhost",
    "img.shields.io",
}
SOURCE_INVENTORY_LAYERS = {
    "A-stable",
    "A-volatile",
    "B-implementation",
    "C-background",
    "Runtime asset",
}
FRONTIER_SOURCE_LEVELS = {"A", "B", "C", "D"}
COURSE_DOCS = {
    "docs/syllabus.md": [
        "课程目标",
        "CS224N Benchmark Crosswalk",
        "CS224N Current Benchmark Snapshot",
        "先修要求",
        "评分结构",
        "10 周 / 20 讲 Lecture Plan",
        "Lecture Slide Outline",
        "Lecture Notes Index",
        "Board Derivation and Instructor Notes Pack",
        "Classroom Demo Runbook",
        "Compute Resource and Cost Guide",
        "逐周阅读清单与复盘 Handout",
        "Assignment Handout Pack",
        "Autograder 与隐藏测试设计指南",
        "Capstone Proposal and Milestone Guide",
        "Capstone Project Gallery and Idea Bank",
        "Project Report Template and Reproducibility Checklist",
        "Data and Ethics Review",
        "Course Staff Runbook",
        "Participation and Feedback Guide",
        "Quiz and Checkpoint Guide",
        "Assessment Administration and Exam Integrity Policy",
        "Staff Assistance and Code Review Boundary Policy",
        "Experimental Rigor and Evaluation Statistics Guide",
        "Concept Mastery and Misconception Map",
        "Midterm and Final Review Pack",
        "Gradebook and LMS Operations Guide",
        "Frontier Seminar Handout",
        "Student FAQ and Troubleshooting Guide",
        "Course Materials Index",
        "周安排",
        "作业节奏",
        "Assignment Submission and Release Guide",
        "Capstone 里程碑",
        "同伴 review",
        "迟交与复核",
        "协作与 AI 工具",
        "External Source Inventory",
        "学生支持与可及性",
        "Accessibility and Student Support Guide",
        "Prerequisite Diagnostic",
        "课程验收命令",
    ],
    "docs/course-outcome-map.md": [
        "Course Outcome Map",
        "证据等级",
        "Outcome 1: 解释 Decoder-only LLM 数据流",
        "Outcome 2: 用 PyTorch 实现核心模块",
        "Outcome 3: 推导关键公式与复杂度",
        "Outcome 4: 复现训练与推理工程实验",
        "Compute Resource and Cost Guide",
        "Outcome 5: 区分来源等级与前沿不确定性",
        "Outcome 6: 理解经典 NLP 与评测专题",
        "自动门禁覆盖矩阵",
        "人工审查清单",
    ],
    "docs/course-operations-log.md": [
        "Course Operations and Improvement Log",
        "使用范围",
        "dry-run baseline",
        "live offering",
        "每周运行记录",
        "Quiz 与阶段 Checkpoint 记录",
        "Demo Dry Run 记录",
        "学生 FAQ 更新记录",
        "算力额度与成本记录",
        "作业复盘记录",
        "隐藏测试统计",
        "讨论课与 Office Hours 记录",
        "项目复现记录",
        "阅读复盘与来源审计记录",
        "课堂参与与反馈调查记录",
        "复核与评分争议记录",
        "Pre-Semester Readiness Audit",
        "CS224N current benchmark snapshot",
        "scripts/generate_course_evidence_manifest.py",
        "前沿来源更新记录",
        "改进任务看板",
        "期末课程复盘",
    ],
    "docs/weekly-teaching-reflection-adjustment-log.md": [
        "Weekly Teaching Reflection and Adjustment Log",
        "复核日期：2026-06-05",
        "Reflection Schema",
        "Evidence Sources",
        "Adjustment Action Bank",
        "Current Reflection Records",
        "Next-Lecture Patch Template",
        "Staff Workflow",
        "Release Checklist",
        "WTR-QUICK",
        "WTR-A-RECAP",
        "WTR-2026-L03-MASK",
        "student site release",
        "course-operations-log.md",
    ],
    "docs/university-course-quality-audit.md": [
        "目标标准",
        "CS224N Benchmark Crosswalk",
        "CS224N Current Benchmark Snapshot",
        "高校课程对标",
        "建议评分方案",
        "推荐周历",
        "学习目标证据",
        "评分一致性",
        "阶段性测验",
        "Midterm and Final Review Pack",
        "阶段检查",
        "授课执行",
        "Demo Runbook",
        "Lecture Notes Index",
        "Board Derivation and Instructor Notes Pack",
        "材料发布",
        "参与与反馈",
        "学生 FAQ",
        "学生支持与可及性",
        "算力与成本",
        "External Source Inventory",
        "外部来源复核",
        "运行改进闭环",
        "开课前 readiness audit",
        "Pre-Semester Readiness Audit",
        "前沿专题讨论",
        "内容准确性维护规则",
        "最终验收 Rubric",
    ],
    "docs/presemester-readiness-audit.md": [
        "Pre-Semester Readiness Audit",
        "复核日期：2026-06-05",
        "release-candidate",
        "Audit Scope",
        "CS224N current benchmark",
        "matched_marker_count=38",
        "missing_marker_count=0",
        "COURSE VERIFY: PASS",
        "ASSIGNMENT TESTS: PASS (11 suite(s))",
        "browser render smoke",
        "release smoke",
        "Release Safety Evidence",
        "Known Human Sign-Off Boundaries",
        "Full Capstone Acceptance Evidence",
        "pass_rate: 5/5 = 100.0%",
        "SLO: PASS",
        "tokens_per_second: 299.2739 >= 100.0000",
        "latency_ms.p95: 306.9216 <= 2000.0000",
        "final_step: 12",
        "LMS / Gradescope configuration",
        "School-specific policy",
        "Hidden tests",
        "Pre-Semester Checklist",
        ".venv/bin/python verify_course.py --capstone --training",
        "Next Audit Actions",
        "course_evidence_manifest",
        "verification_status: pass",
        "scripts/generate_course_evidence_manifest.py",
    ],
    "docs/cs224n-benchmark-crosswalk.md": [
        "CS224N Benchmark Crosswalk",
        "CS224N Current Benchmark Snapshot",
        "复核日期：2026-06-05",
        "当前公开页复核摘要",
        "Stanford / Winter 2026",
        "Assignments 48%",
        "Final Project 49%",
        "Lecture videos",
        "Lecture Media Access Policy",
        "Course calendar and deadlines",
        "Course Calendar and Deadline Ledger",
        "Python/PyTorch review sessions",
        "Python and PyTorch Review Session",
        "Participation 3%",
        "对标范围",
        "内容覆盖对照",
        "权重对照",
        "仍需人工确认的项目",
        "发布前 Checklist",
        "Course homepage and logistics",
        "Prerequisites",
        "Final project with proposal, milestone, poster/report",
        "Default Final Project Guide",
        "Experimental Rigor and Evaluation Statistics Guide",
        "Final Project Showcase and Archive Policy",
        "Assignment Handout Pack",
        "Computing resources for projects",
        "Schedule and lecture slides",
        "Current schedule topic evidence",
        "Hugging Face tutorial",
        "Benchmarking and Evaluation",
        "Reasoning",
        "Tokenization and Multilinguality",
        "Tinker and LoRA",
        "Honor code and AI policy",
        "Academic Integrity Case Process",
        "Interpretability, multimodality, social impact, open questions",
        "Frontier Seminar Handout",
    ],
    "docs/cs224n-current-benchmark-snapshot.md": [
        "CS224N Current Benchmark Snapshot",
        "复核日期：2026-06-05",
        "基准来源：https://web.stanford.edu/class/cs224n/",
        "Stanford / Winter 2026",
        "当前公开页要点",
        "当前 Schedule 主题证据矩阵",
        "History of NLP",
        "Word Vectors",
        "Python Review Session",
        "Backpropagation and Neural Network Basics",
        "PyTorch Tutorial Session",
        "Hugging Face Transformers Tutorial Session",
        "Benchmarking and Evaluation",
        "Reasoning 1 / Reasoning 2",
        "Tokenization and Multilinguality",
        "Tinker and LoRA Without Regret",
        "Assignment 1-4 release/due events",
        "Project proposal, milestone, report, poster session",
        "Assignments 48%",
        "Final Project 49%",
        "Participation 3%",
        "proposal 8%",
        "milestone 6%",
        "poster 3%",
        "Archived project reports",
        "report 32%",
        "6 late days",
        "Honor code / academic integrity",
        "AI tools policy",
        "Academic Integrity Case Process",
        "Accessibility / well-being",
        "Interpretability",
        "Multimodality",
        "Open Questions",
        "Experimental Rigor",
        "Experimental Rigor and Evaluation Statistics Guide",
        "frontier-seminar-handout.md",
        "差异解释",
        "发布前 Checklist",
    ],
    "docs/lecture-plan.md": [
        "10 周 / 20 讲 Lecture Plan",
        "授课结构",
        "Week 1 Lecture 1",
        "Week 5 Lecture 10",
        "Week 8 Lecture 15",
        "Week 10 Lecture 20",
        "Discussion Section 模板",
        "Office Hours 模板",
        "Exit Ticket 模板",
    ],
    "docs/lecture-slide-outline.md": [
        "Lecture Slide Outline",
        "使用规则",
        "Lecture Notes Index",
        "Lecture Notes Quality and Review Standard",
        "Board Derivation and Instructor Notes Pack",
        "Slide Deck 模板",
        "20 讲课件大纲",
        "L1",
        "L10",
        "L20",
        "教师备注模板",
        "发布前 Checklist",
        "frontier-source-audit.md",
    ],
    "docs/lecture-notes-index.md": [
        "Lecture Notes Index",
        "Lecture Notes Quality and Review Standard",
        "Lecture Notes Review Ledger",
        "Lecture Note Sample Pack",
        "Lecture Note Core Pack",
        "Board Derivation and Instructor Notes Pack",
        "使用规则",
        "Notes 发布状态",
        "20 讲 Lecture Notes 索引",
        "L1",
        "L10",
        "L20",
        "Notes 模板",
        "Review record",
        "学生复盘模板",
        "发布前 Checklist",
    ],
    "docs/lecture-note-sample-pack.md": [
        "Lecture Note Sample Pack",
        "复核日期：2026-06-05",
        "Sample Packet Rubric",
        "Sample L1: Tokenization and BPE",
        "Sample L3: Scaled Dot-Product Attention",
        "Sample L9: Cross Entropy and AdamW",
        "Sample L18: Serving SLO and Capacity",
        "TA Review Checklist",
        "Release Checklist",
        "Learning goals",
        "Notation ledger",
        "Core derivation",
        "Shape checks",
        "Code binding",
        "Common misconceptions",
        "Source boundary",
        "Accessibility notes",
        "Quick check",
        "Post-lecture evidence",
    ],
    "docs/lecture-note-core-pack.md": [
        "Lecture Note Core Pack",
        "复核日期：2026-06-05",
        "Coverage Contract",
        "Core L2: Embedding, Analogy, and RoPE",
        "Core L4: Causal Mask and Cross-Entropy Gradient",
        "Core L6: MHA, GQA, MLA, Norm, and Block Boundaries",
        "Core L12: Speculative Decoding, Constraints, and Frontier Source Boundaries",
        "Core L15: Classic NLP, Encoder-Decoder, BERT, and Evaluation",
        "TA Review Checklist",
        "Release Checklist",
        "Learning goals",
        "Notation ledger",
        "Core derivation",
        "Shape checks",
        "Code binding",
        "Common misconceptions",
        "Source boundary",
        "Accessibility notes",
        "Quick check",
        "Post-lecture evidence",
    ],
    "docs/notation-shape-glossary.md": [
        "Notation and Shape Glossary",
        "复核日期：2026-06-05",
        "Global Symbols",
        "Module Shape Contracts",
        "Mask and Broadcast Rules",
        "Loss, Objective, and Optimizer Symbols",
        "Serving and Evaluation Units",
        "Disambiguation Rules",
        "Assessment Use",
        "Maintenance Workflow",
        "Release Checklist",
        "NS-01",
        "NS-15",
        "MASK-CAUSAL",
        "MASK-LABEL",
        "beta_dpo",
        "TTFT",
        "UAS",
        "student site release",
    ],
    "docs/worked-example-pack.md": [
        "Worked Example Pack",
        "复核日期：2026-06-05",
        "Example Schema",
        "Core Worked Examples",
        "Recitation Use",
        "Assessment Coverage",
        "Maintenance Workflow",
        "Release Checklist",
        "WE-CH01-BPE",
        "WE-CH02-ROPE",
        "WE-CH03-ATTN",
        "WE-CH04-GQA",
        "WE-CH05-NORM",
        "WE-CH06-PARAMS",
        "WE-CH07-ADAMW",
        "WE-CH08-TOPP",
        "WE-CH09-DPO",
        "WE-CH10-KVCACHE",
        "WE-CH11-METRICS",
        "common failure",
        "source boundary",
        "student site release",
    ],
    "docs/lecture-slide-sample-pack.md": [
        "Lecture Slide Sample Pack",
        "复核日期：2026-06-05",
        "Slide Sample Rubric",
        "Sample Deck S1",
        "Sample Deck S4",
        "Slide sequence",
        "Visual plan",
        "Speaker note",
        "Accessibility text",
        "Source boundary",
        "Quick check",
        "Post-lecture evidence",
        "Deck Accessibility Checklist",
        "Release Checklist",
        "lecture-slide-outline.md",
        "lecture-note-sample-pack.md",
        "lecture-notes-quality-review.md",
        "course-materials-index.md",
        "demo-runbook.md",
        "recitation-worksheet-pack.md",
        "paper-to-code-traceability-matrix.md",
    ],
    "docs/recitation-worksheet-pack.md": [
        "Recitation Worksheet Pack",
        "复核日期：2026-06-05",
        "Worksheet Schema",
        "Worksheet W1",
        "Worksheet W6",
        "shape_table",
        "Failure drill",
        "Paper-to-code link",
        "Exit ticket",
        "Staff Feedback Rubric",
        "Release Checklist",
        "discussion-office-hours-guide.md",
        "concept-misconception-map.md",
        "paper-to-code-traceability-matrix.md",
        "mathematical-derivation-audit.md",
        "assignment-handout-pack.md",
        "participation-feedback-guide.md",
    ],
    "docs/learning-analytics-remediation-plan.md": [
        "Learning Analytics and Remediation Plan",
        "复核日期：2026-06-05",
        "Data Sources",
        "Trigger Thresholds",
        "Remediation Playbooks",
        "Weekly Review Workflow",
        "Student-Facing Feedback Template",
        "Operations Log Template",
        "Privacy and Fairness Rules",
        "Release Checklist",
        "LA-QUIZ",
        "TR-SHAPE-30",
        "RP-SHAPE",
        "quiz-checkpoint-guide.md",
        "concept-misconception-map.md",
        "recitation-worksheet-pack.md",
        "gradebook-lms-operations.md",
        "participation-feedback-guide.md",
        "learning-outcome-attainment-report.md",
        "teaching-observation-course-evaluation.md",
        "staff-runbook.md",
        "course-operations-log.md",
    ],
    "docs/learning-outcome-attainment-report.md": [
        "Learning Outcome Attainment Report",
        "复核日期：2026-06-05",
        "Attainment Evidence Taxonomy",
        "Outcome Attainment Targets",
        "Current Dry-Run Attainment Matrix",
        "Direct Evidence Collection Plan",
        "Indirect Evidence and Triangulation",
        "Attainment Status Codes",
        "Closing the Loop Actions",
        "Release Checklist",
        "dry-run evidence does not prove real student attainment",
        "CO1",
        "CO6",
        "design_ready",
        "LOA-AUTO-ASSIGN",
        "LOA-PROJECT-CLINIC",
    ],
    "docs/teaching-observation-course-evaluation.md": [
        "Teaching Observation and Course Evaluation Dossier",
        "复核日期：2026-06-05",
        "Evaluation Sources",
        "Peer Observation Rubric",
        "Midterm Feedback Response Protocol",
        "End-of-Term Course Review",
        "Current Evaluation Ledger",
        "Student-Visible Response Memo Template",
        "Staff Observation Note Template",
        "Release Checklist",
        "CE-PEER-OBS",
        "CE-MID-SURVEY",
        "CE-END-SURVEY",
        "learning_goal_alignment",
        "technical_accuracy",
        "CE-2026-ITEM-W5",
    ],
    "docs/workload-pacing-calibration.md": [
        "Workload and Pacing Calibration",
        "复核日期：2026-06-05",
        "Calibration Assumptions",
        "Weekly Workload Budget",
        "Difficulty Ladder",
        "Assignment Load Guardrails",
        "Overload Signals and Pacing Actions",
        "10-to-12 Week Expansion Map",
        "Student Time-Planning Template",
        "Staff Review Protocol",
        "Release Checklist",
        "syllabus.md",
        "course-calendar-deadline-ledger.md",
        "assignment-handout-pack.md",
        "recitation-worksheet-pack.md",
        "reading-list.md",
        "learning-analytics-remediation-plan.md",
        "course-operations-log.md",
    ],
    "docs/lecture-notes-review-ledger.md": [
        "Lecture Notes Review Ledger",
        "Review Ledger",
        "Review Exceptions and Follow-Up",
        "Evidence Requirements",
        "发布前 Checklist",
        "L1",
        "L10",
        "L20",
        "notation_checked",
        "derivation_checked",
        "code_binding_checked",
        "source_boundary_checked",
        "accessibility_checked",
        "none-current",
        ".venv/bin/python verify_course.py --capstone --training",
    ],
    "docs/lecture-notes-quality-review.md": [
        "Lecture Notes Quality and Review Standard",
        "Lecture Notes Review Ledger",
        "适用范围",
        "Notes Quality Rubric",
        "Per-Lecture Review Checklist",
        "Sample Lecture Note Packet",
        "Review Record Template",
        "Correction Workflow",
        "Evidence Matrix",
        "Staff Checklist",
        "发布前 Checklist",
        "Notation ledger",
        "Derivation completeness",
        "Shape and units",
        "Code binding",
        "Source boundary",
        "review_date",
        "verification_command",
        "notation_checked",
        "source_boundary_checked",
    ],
    "docs/board-derivation-pack.md": [
        "Board Derivation and Instructor Notes Pack",
        "复核日期：2026-06-05",
        "符号约定",
        "课堂板书脚本",
        "BPE Merge 不是全局最优压缩",
        "Embedding Lookup 等价于 One-Hot 矩阵乘法",
        "Sinusoidal / RoPE 的相对位置结构",
        "Attention Scaling",
        "Causal Mask 的 Logit 级应用",
        "MHA / GQA / MLA 的参数与 KV Cache 区分",
        "LayerNorm / RMSNorm 的依赖关系",
        "Next-Token NLL / Cross Entropy",
        "AdamW 与 Adam + L2 的区别",
        "DPO Log-Ratio 的方向",
        "GRPO Group Advantage Whitening",
        "KV Cache 显存公式",
        "20 讲 Quick Check 对照",
        "评分使用规则",
        "发布前 Checklist",
    ],
    "docs/mathematical-derivation-audit.md": [
        "Mathematical Derivation Audit",
        "复核日期：2026-06-05",
        "Audit Schema",
        "Audited Derivations",
        "Executable Gate Coverage",
        "Instructor Review Protocol",
        "发布前 Checklist",
        "DER-01",
        "DER-02",
        "DER-03",
        "DER-04",
        "DER-05",
        "DER-06",
        "DER-07",
        "DER-08",
        "DER-09",
        "DER-10",
        "DER-11",
        "DER-12",
        "DER-13",
        "DER-14",
        "Assumptions",
        "Shape / units",
        "Executable evidence",
        "Boundary",
        "check_mathematical_derivation_audit()",
    ],
    "docs/demo-runbook.md": [
        "Classroom Demo Runbook",
        "使用规则",
        "Demo 环境检查",
        "20 讲 Demo 清单",
        "L1",
        "L10",
        "L20",
        "失败排查模板",
        "发布前 Checklist",
    ],
    "docs/compute-resource-guide.md": [
        "Compute Resource and Cost Guide",
        "资源原则",
        "推荐资源档位",
        "每周资源预期",
        "配额与公平使用",
        "成本记录模板",
        "CPU Fallback 要求",
        "安全与数据边界",
        "Staff Checklist",
        "发布前 Checklist",
    ],
    "docs/course-materials-index.md": [
        "Course Materials Index",
        "Board Derivation and Instructor Notes Pack",
        "Assignment Handout Pack",
        "使用规则",
        "发布状态",
        "20 讲材料索引",
        "Demo 与代码发布规则",
        "Slides / Notes / Recording 规则",
        "Lecture Slide Outline",
        "Lecture Notes Index",
        "Classroom Demo Runbook",
        "Concept Mastery and Misconception Map",
        "Lecture Media Access Policy",
        "Material Versioning and Archive Policy",
        "Frontier Seminar Handout",
        "Default Final Project Guide",
        "default-final-project-guide.md",
        "Project Report Template and Reproducibility Checklist",
        "project-report-template.md",
        "Environment and Reproducibility Guide",
        "environment-reproducibility.md",
        "Compute Resource and Cost Guide",
        "scripts/build_course_site_release.py",
        "SITE_RELEASE_MANIFEST.json",
        "版本记录",
        "发布前 Checklist",
        "Week 1 reading",
        "assignments/ch11_classic_nlp/tests.py",
        ".venv/bin/python verify_course.py",
    ],
    "docs/material-versioning-archive-policy.md": [
        "Material Versioning and Archive Policy",
        "版本状态",
        "材料类型规则",
        "学生站点发布规则",
        "旧材料与历史报告",
        "版本记录字段",
        "归档记录样例",
        "发布前 Checklist",
        "current",
        "release-candidate",
        "archived",
        "retired",
        "instructor-only",
        "SITE_RELEASE_MANIFEST.json",
        "RELEASE_MANIFEST.json",
    ],
    "docs/course-calendar-deadline-ledger.md": [
        "Course Calendar and Deadline Ledger",
        "single source of truth",
        "时间字段",
        "10 周台账模板",
        "作业与项目截止台账",
        "变更控制",
        "Release Freeze",
        "Staff Checklist",
        "发布前 Checklist",
        "timezone",
        "release_at",
        "due_at",
        "late day",
        "regrade window",
        "LMS / Gradescope",
        "Course Communication and Announcement Policy",
        ".venv/bin/python verify_course.py --capstone --training",
    ],
    "docs/concept-misconception-map.md": [
        "Concept Mastery and Misconception Map",
        "core-concept-glossary.md",
        "掌握等级",
        "逐章误区与补救地图",
        "跨章节高风险边界",
        "Quick Check 题型模板",
        "维护 Checklist",
        "Shape first",
        "Mask before probability",
        "Norm vs semantics",
        "Metric vs quality",
        "Public tests vs mastery",
        "Frontier claims",
        "Ready",
        "Borderline",
        "Not ready",
    ],
    "docs/core-concept-glossary.md": [
        "Core Concept Glossary",
        "复核日期：2026-06-05",
        "Definition Schema",
        "Core Concepts",
        "Cross-Reference Map",
        "Definition Quality Rules",
        "Maintenance Workflow",
        "Release Checklist",
        "CG-TOKEN-BPE",
        "CG-ATTN",
        "CG-GQA",
        "CG-DPO",
        "CG-RAG",
        "CG-SLO",
        "CG-EVAL-METRIC",
        "CG-SOURCE-BOUNDARY",
        "source boundary",
        "student site release",
    ],
    "docs/topic-dependency-map.md": [
        "Topic Dependency and Spiral Review Map",
        "复核日期：2026-06-05",
        "Dependency Layers",
        "Chapter Dependency Graph",
        "Spiral Review Schedule",
        "Dependency Failure Signals",
        "Student Navigation Rules",
        "Staff Review Workflow",
        "Release Checklist",
        "TD-L0-PREREQ",
        "TD-L8-CAPSTONE",
        "TD-CH01",
        "TD-CH11",
        "TD-SR-W1",
        "TD-SR-W10",
        "TD-F-SHAPE",
        "student site release",
    ],
    "docs/frontier-seminar-handout.md": [
        "Frontier Seminar Handout",
        "Interpretability",
        "Multimodality",
        "Social and Broader Impacts",
        "Open Questions in NLP and LLM Engineering",
        "评分 Rubric",
        "最低交付",
        "attention heatmap",
        "multimodal LLM",
        "风险登记表",
        "可评测假设",
        "CS224N Current Benchmark Snapshot",
    ],
    "docs/discussion-office-hours-guide.md": [
        "Discussion Section and Office Hours Guide",
        "Course Staff and Office Hours Directory",
        "讨论课结构",
        "Week 1: BPE / Embedding / RoPE",
        "Week 5: Training Loop",
        "Week 8: Classic NLP / Evaluation / Safety",
        "Week 10: Capstone Rehearsal",
        "Office Hours Triage",
        "高频问题记录模板",
        "Exit Ticket 汇总",
    ],
    "docs/course-communication-policy.md": [
        "Course Communication and Announcement Policy",
        "Course Staff and Office Hours Directory",
        "Course Errata and Correction Ledger",
        "渠道总览",
        "公告规则",
        "公开讨论区规则",
        "私密渠道规则",
        "Office Hours 规则",
        "评分和复核沟通",
        "课程勘误和内容更正",
        "Staff 使用规范",
        "发布前 Checklist",
        "课程公告",
        "公开讨论区",
        "私密消息或课程邮箱",
        "学校正式支持渠道",
        "queue policy",
        "escalation matrix",
        ".venv/bin/python verify_course.py --capstone --training",
    ],
    "docs/course-errata-correction-ledger.md": [
        "Course Errata and Correction Ledger",
        "复核日期：2026-06-05",
        "Severity Levels",
        "Ledger Schema",
        "Current Errata Ledger",
        "Intake and Triage Workflow",
        "Announcement Template",
        "SLA and Escalation",
        "Cross-Update Rules",
        "Student-Facing Report Form",
        "Release Checklist",
        "ERR-2026-06-05-CH02-01",
        "S1 grading-impacting",
        "source-drift",
    ],
    "docs/course-staff-office-hours-directory.md": [
        "Course Staff and Office Hours Directory",
        "Staff Assistance and Code Review Boundary Policy",
        "学生可见 Staff 角色",
        "联系渠道",
        "Office Hours 类型",
        "排班与覆盖要求",
        "Queue Policy",
        "Escalation Matrix",
        "Public Directory Template",
        "Staff Handoff Fields",
        "Staff Checklist",
        "发布前 Checklist",
        "Instructor",
        "Course Manager",
        "Head TA",
        "Discussion TA",
        "Project Mentor",
        "Autograder Contact",
        "concept / math",
        "coding / debugging",
        "minimal_reproduction",
        "limited_code_view",
        "pseudocode",
        "fairness_followup",
        "backup_contact",
    ],
    "docs/enrollment-audit-public-use-policy.md": [
        "Enrollment, Audit, and Public Use Policy",
        "身份与权限",
        "成绩与证书边界",
        "平台与访问控制",
        "旁听与公开学习规则",
        "Staff Checklist",
        "发布前 Checklist",
        "正式选课 / enrolled for credit",
        "Credit / No Credit",
        "旁听 / auditor",
        "自学者 / public learner",
        "Teaching staff / mentor",
        "official transcript",
        "certificate",
        "LMS / Gradescope",
        "hidden tests",
        "compute credits",
        "project mentor",
        "reference_solution.py",
        "scripts/build_course_site_release.py",
        "scripts/build_assignment_release.py",
    ],
    "docs/lecture-media-access-policy.md": [
        "Lecture Media Access Policy",
        "媒体类型与访问边界",
        "发布与替代材料",
        "隐私、版权与剪辑规则",
        "可访问性要求",
        "平台与链接记录",
        "Staff Checklist",
        "发布前 Checklist",
        "live stream",
        "current lecture recording",
        "public historical video",
        "demo screencast",
        "caption / transcript",
        "enrolled students",
        "public learner",
        "Canvas / Panopto",
        "scripts/build_course_site_release.py",
    ],
    "docs/student-faq-troubleshooting.md": [
        "Student FAQ and Troubleshooting Guide",
        "Course Communication and Announcement Policy",
        "Environment and Reproducibility Guide",
        "使用规则",
        "环境与命令",
        '.venv/bin/python -c "import sys, torch;',
        ".venv/bin/python verify_course.py",
        ".venv/bin/python run_assignment_tests.py",
        "作业测试",
        "Shape / Mask / Tensor Debugging",
        "章节概念 FAQ",
        "Capstone Troubleshooting",
        "Office Hours 提问模板",
        "评分与复核",
        "发布前 Checklist",
    ],
    "docs/quiz-checkpoint-guide.md": [
        "Quiz and Checkpoint Guide",
        "Midterm and Final Review Pack",
        "Assessment Item Bank Ledger",
        "Assessment Administration and Exam Integrity Policy",
        "评估类型",
        "出题原则",
        "题型池",
        "每周 Quick Check 蓝图",
        "Midterm Checkpoint",
        "补救路径",
        "评分与诚信边界",
        "allowed materials",
        "makeup assessment",
        "题目轮换记录",
        "2026-06-05 dry-run baseline",
        "发布前 Checklist",
    ],
    "docs/midterm-final-review-pack.md": [
        "Midterm and Final Review Pack",
        "复核日期：2026-06-05",
        "Comprehensive Review Study Guide",
        "Assessment Administration and Exam Integrity Policy",
        "使用规则",
        "Midterm Checkpoint Sample",
        "题 1：BPE 与 Embedding Shape",
        "题 2：RoPE 与 Attention Scaling",
        "题 3：Causal Mask 与 MHA/GQA Cache",
        "题 4：GPT / MoE / Training Loop",
        "题 5：来源与复现边界",
        "Midterm Remediation Map",
        "Final Review Sample",
        "题 A：Generation / Decoding",
        "题 B：SFT / LoRA / DPO / GRPO",
        "题 C：Classic NLP / Evaluation",
        "题 D：Inference / RAG / Serving",
        "题 E：Capstone Evidence and Source Audit",
        "Final Review Rubric",
        "assessment_id",
        "allowed materials",
        "makeup",
        "发布前 Checklist",
    ],
    "docs/comprehensive-review-study-guide.md": [
        "Comprehensive Review Study Guide",
        "复核日期：2026-06-05",
        "Review Outcomes",
        "Two-Pass Review Schedule",
        "Self-Diagnostic Checklist",
        "Error Log Template",
        "Practice Set Sequence",
        "Staff Use",
        "Release Checklist",
        "CR-O1",
        "CR-S6",
        "CR-D-SOURCE",
        "CR-P-PROJECT",
        "CR-STAFF-CALIBRATE",
        "student site release",
    ],
    "docs/assessment-item-bank-ledger.md": [
        "Assessment Item Bank Ledger",
        "复核日期：2026-06-05",
        "Exposure Levels",
        "Item Metadata Schema",
        "Public-Safe Item Bank",
        "Rotation Procedure",
        "Equivalence and Makeup Rules",
        "Release Checklist",
        "QC-W1-BPE-01",
        "QC-W2-MASK-01",
        "QC-W3-CACHE-01",
        "QC-W5-TRAIN-01",
        "QC-W6-SAMPLING-01",
        "QC-W7-DPO-01",
        "QC-W8-EVAL-01",
        "QC-W9-SLO-01",
        "QC-W10-SOURCE-01",
        "QC-MAKEUP-EQUIV-01",
        "public_sample",
        "practice_variant",
        "active_assessment",
        "retired",
    ],
    "docs/assessment-blueprint-coverage-matrix.md": [
        "Assessment Blueprint and Coverage Matrix",
        "复核日期：2026-06-05",
        "Blueprint Dimensions",
        "Outcome Coverage Matrix",
        "Assessment Channel Balance",
        "Cognitive Level Ladder",
        "Sampling and Rotation Rules",
        "Evidence and Grading Gates",
        "Gap Audit",
        "Release Checklist",
        "CO1",
        "CO2",
        "CO3",
        "CO4",
        "CO5",
        "CO6",
        "remember",
        "understand",
        "apply",
        "analyze",
        "evaluate",
        "create",
        "auto_gate",
        "capstone_gate",
    ],
    "docs/assessment-item-analysis-psychometrics.md": [
        "Assessment Item Analysis and Psychometrics Guide",
        "复核日期：2026-06-05",
        "Item Analysis Scope",
        "Metric Definitions",
        "Decision Thresholds",
        "Analysis Record Schema",
        "Current Dry-Run Analysis Records",
        "Post-Assessment Workflow",
        "Fairness and Privacy Rules",
        "Release Checklist",
        "item_difficulty_p",
        "item_discrimination_d",
        "distractor_efficiency",
        "short_answer_rubric_fit",
        "subgroup_review_flag",
        "IA-DIFF-HARD",
        "IA-RUBRIC-DRIFT",
        "QC-W9-SLO-01",
    ],
    "docs/assessment-administration-policy.md": [
        "Assessment Administration and Exam Integrity Policy",
        "Assessment Item Bank Ledger",
        "Assessment Types",
        "Scheduling and Announcement",
        "Allowed Materials Matrix",
        "Item Security and Rotation",
        "Proctoring and Identity",
        "Accommodations and Makeup",
        "Integrity Incident Flow",
        "Grading and Feedback Release",
        "Post-Assessment Review",
        "Staff Checklist",
        "发布前 Checklist",
        "assessment_id",
        "allowed_materials",
        "makeup_assessment",
        "item_bank_id",
        "integrity_hold",
    ],
    "docs/participation-feedback-guide.md": [
        "Participation and Feedback Guide",
        "评分范围",
        "参与评分 Rubric",
        "讨论区贡献规则",
        "期中反馈调查",
        "期末反馈调查",
        "嘉宾讲座或外部报告",
        "Guest Speaker and External Seminar Policy",
        "参与证据记录",
        "Week 1 dry-run baseline",
        "学生提交模板",
        "Staff Checklist",
    ],
    "docs/guest-speaker-seminar-policy.md": [
        "Guest Speaker and External Seminar Policy",
        "适用范围",
        "活动准入",
        "日程与公告",
        "参与分规则",
        "替代任务",
        "学生提交模板",
        "Rubric",
        "讲者材料与录制边界",
        "项目与伦理升级",
        "记录模板",
        "Staff Checklist",
        "发布前 Checklist",
        "guest lecture",
        "external seminar",
        "technical reflection",
        "Q&A note",
        "source audit",
        "privacy_review",
    ],
    "docs/staff-runbook.md": [
        "Course Staff Runbook",
        "Course Communication and Announcement Policy",
        "角色与职责",
        "开课前 Checklist",
        "Classroom Demo Runbook",
        "Compute Resource and Cost Guide",
        "权限与工具",
        "公告模板",
        "每周 Staff Meeting",
        "Student FAQ and Troubleshooting Guide",
        "Participation and Feedback Guide",
        "作业发布与评分交接",
        "Office Hours 排班",
        "事故与升级流程",
        "期末收尾",
        "Staff Handoff Template",
    ],
    "docs/course-policies.md": [
        "协作边界",
        "AI 工具使用",
        "引用与来源",
        "复现要求",
        "Gradebook and LMS Operations Guide",
        "regrade_status",
        "regrade_decision_id",
        "学生支持与隐私",
        "Accessibility and Student Support Guide",
        "Academic Integrity Case Process",
    ],
    "docs/academic-integrity-case-process.md": [
        "Academic Integrity Case Process",
        "适用范围",
        "允许 / 禁止 / 必须披露",
        "Signals and Triage",
        "Automated Checks",
        "Manual Review Flow",
        "Student Rights and Privacy",
        "AI Tools Review",
        "Similarity Report Interpretation",
        "Project Integrity",
        "Case Record Template",
        "Staff Checklist",
        "发布前 Checklist",
        "reference_solution.py",
        "hidden tests",
        "similarity report",
        "student_response",
        "grade_action",
    ],
    "docs/accessibility-student-support.md": [
        "Accessibility and Student Support Guide",
        "适用范围",
        "学术便利安排",
        "课程材料可访问性",
        "学生支持渠道",
        "学习困难与干预",
        "公平评分与便利边界",
        "团队项目支持",
        "记录与反馈闭环",
        "教师发布前 Checklist",
    ],
    "docs/prerequisite-diagnostic.md": [
        "Prerequisite Diagnostic",
        "通过标准",
        "诊断结构",
        "Python 基础",
        "PyTorch 基础",
        "线性代数、概率与统计",
        "ML Foundations",
        "ML Foundations Prerequisite Bridge",
        "反向传播与数值稳定性",
        "复现与调试纪律",
        "补救任务",
        "教师使用建议",
        "学生提交模板",
    ],
    "docs/python-pytorch-review-session.md": [
        "Python and PyTorch Review Session",
        "Session 目标",
        "课前准备",
        "Python Review Session 议程",
        "Python Drill",
        "PyTorch Tutorial Session 议程",
        "PyTorch Drill",
        "常见失败与处理",
        "学生提交模板",
        "Staff Checklist",
        "发布前 Checklist",
        "CS224N Winter 2026",
        "STUDENT_MODULE=starter .venv/bin/python assignments/ch01_bpe/tests.py",
        "STUDENT_MODULE=starter .venv/bin/python assignments/ch02_embeddings/tests.py",
        "next-token CE",
        "autograd",
        "shape trace",
    ],
    "docs/math-prerequisites.md": [
        "线性代数最小集合",
        "统计与 ML Foundations 入口",
        "ML Foundations Prerequisite Bridge",
        "Cross Entropy 推导检查",
        "LayerNorm 推导检查",
        "DPO/GRPO 推导检查",
    ],
    "docs/ml-foundations-prerequisite-bridge.md": [
        "ML Foundations Prerequisite Bridge",
        "覆盖范围",
        "Diagnostic Add-on",
        "Mini-Lecture: Calculus to Backprop",
        "Mini-Lecture: Probability and Language Models",
        "Mini-Lecture: Statistics for Experiments",
        "Mini-Lecture: ML Objectives and Generalization",
        "Project Evidence Checklist",
        "补救任务",
        "Staff Checklist",
        "发布前 Checklist",
    ],
    "docs/reading-list.md": [
        "逐周阅读清单与复盘 Handout",
        "Paper Recap Calibration Pack",
        "Reading Discussion Question Bank",
        "阅读复盘评分",
        "Week 0: 先修与 ML Foundations Bridge",
        "ML Foundations Prerequisite Bridge",
        "Stanford CS224N",
        "Week 1: Tokenization 与 Word Vectors",
        "Week 5: Training Loop",
        "Week 8: 经典 NLP",
        "Week 10: Capstone",
        "来源等级速查",
        "提交模板",
    ],
    "docs/paper-recap-calibration-pack.md": [
        "Paper Recap Calibration Pack",
        "复核日期：2026-06-05",
        "Recap Rubric",
        "Anchor Samples",
        "Required Evidence Fields",
        "TA Calibration Procedure",
        "Student Submission Template",
        "Release Checklist",
        "PR-A1",
        "PR-A2",
        "PR-B1",
        "PR-B2",
        "PR-C1",
        "PR-C2",
        "PR-NP1",
        "PR-NP2",
        "source_record",
        "core_claim",
        "technical_detail",
        "course_link",
        "boundary",
        "discussion_question",
    ],
    "docs/reading-discussion-question-bank.md": [
        "Reading Discussion Question Bank",
        "复核日期：2026-06-05",
        "Question Schema",
        "Core Question Bank",
        "Discussion Formats",
        "Assessment Sampling Rules",
        "Maintenance Workflow",
        "Release Checklist",
        "RDQ-W0-CLAIM",
        "RDQ-W10-AUDIT",
        "RDQ-F-RECAP",
        "RDQ-R5",
        "question_type",
        "expected_evidence",
        "student site release",
    ],
    "docs/paper-to-code-traceability-matrix.md": [
        "Paper-to-Code Traceability Matrix",
        "复核日期：2026-06-05",
        "Traceability Matrix",
        "Coverage Requirements",
        "Instructor Review Protocol",
        "Release Checklist",
        "P2C-01",
        "P2C-14",
        "A-stable",
        "A-volatile",
        "B-implementation",
        "DER-01",
        "DER-14",
        "assignments/ch01_bpe",
        "assignments/ch11_classic_nlp",
        "reading-list.md",
        "chapter-source-map.md",
        "external-source-inventory.md",
        "mathematical-derivation-audit.md",
        "assignment-handout-pack.md",
        "paper-recap-calibration-pack.md",
    ],
    "docs/chapter-source-map.md": [
        "Chapter Source and Accuracy Map",
        "使用规则",
        "External Source Inventory",
        "External Source Verification Guide",
        "Claim Audit Worksheet",
        "Chapter Claim Audit Ledger",
        "Course Errata and Correction Ledger",
        "Ch01 Tokenization / BPE",
        "Ch02 Embedding / Position Encoding / RoPE",
        "Ch03 Scaled Dot-Product Attention",
        "Ch04 MHA / GQA / MLA",
        "Ch05 Transformer Block / Norm / FFN",
        "Ch06 GPT Assembly / MoE",
        "Ch07 Training Loop",
        "Ch08 Generation / Decoding",
        "Ch09 Fine-tuning / Alignment",
        "Ch10 Inference / RAG / Serving",
        "经典 NLP 与评测专题",
        "维护检查清单",
    ],
    "docs/chapter-claim-audit-ledger.md": [
        "Chapter Claim Audit Ledger",
        "Course Errata and Correction Ledger",
        "Ledger Schema",
        "Audited Claims",
        "High-Risk Claim Gates",
        "Maintenance Workflow",
        "发布前 Checklist",
        "CH01-C01",
        "CH02-C01",
        "CH03-C01",
        "CH04-C01",
        "CH05-C01",
        "CH06-C01",
        "CH07-C01",
        "CH08-C01",
        "CH09-C01",
        "CH10-C01",
        "CH11-C01",
        "stable theory",
        "implementation",
        "frontier model card",
        "benchmark",
        "course inference",
        "optimality_gate",
        "formula_gate",
        "systems_gate",
        "frontier_gate",
        "evaluation_gate",
    ],
    "docs/external-source-inventory.md": [
        "External Source Inventory",
        "Chapter Claim Audit Ledger",
        "Claim Audit Worksheet",
        "复核日期：2026-06-05",
        "来源分层规则",
        "基础论文与教材",
        "前沿模型与厂商来源",
        "框架与工程文档",
        "课程与学习资源",
        "非来源外链",
        "发布前 Checklist",
        "A-stable",
        "A-volatile",
        "Runtime asset",
    ],
    "docs/external-source-verification.md": [
        "External Source Verification Guide",
        "External Source Inventory",
        "Claim Audit Worksheet",
        "适用范围",
        "复核频率",
        "复核记录字段",
        "复核流程",
        "CS224N 当前页半自动复核",
        "scripts/verify_cs224n_snapshot.py",
        "cs224n-snapshot-2026-06-05.json",
        "外部链接失效处理",
        "高风险 Claim Checklist",
        "学生项目复核",
        "复核日志样例",
        "发布前 Checklist",
    ],
    "docs/external-expert-review-dossier.md": [
        "External Expert Review Dossier",
        "复核日期：2026-06-05",
        "Review Scope",
        "Reviewer Independence Rules",
        "Review Rubric",
        "Current External Review Ledger",
        "Response and Closure Workflow",
        "Evidence Packet Template",
        "Severity and Required Response",
        "Release Checklist",
        "ER-CONTENT",
        "ER-MATH",
        "ER-SOURCES",
        "ER-ASSIGNMENTS",
        "ER-ASSESSMENT",
        "ER-PROJECTS",
        "ER-ACCESSIBILITY",
        "ER-RELEASE",
        "technical_accuracy",
        "mathematical_rigor",
        "source_traceability",
        "ER-2026-MATH-ROPE",
        "student site release",
    ],
    "docs/claim-audit-worksheet.md": [
        "Claim Audit Worksheet",
        "Chapter Claim Audit Ledger",
        "使用场景",
        "Claim 分类",
        "复核表模板",
        "示例记录",
        "逐章最低审查清单",
        "Ch01",
        "Ch05",
        "Ch10",
        "Ch11",
        "发布前 Checklist",
    ],
    "docs/written-problem-set.md": [
        "评分规则",
        "Ch01 Tokenization / BPE",
        "Ch02 Embedding / Position Encoding / RoPE",
        "Ch03 Scaled Dot-Product Attention",
        "Ch04 MHA / GQA / MLA",
        "Ch05 Transformer Block / Norm / FFN",
        "Ch06 GPT Assembly / MoE",
        "Ch07 Training Loop",
        "Ch08 Generation / Decoding",
        "Ch09 Fine-tuning / Alignment",
        "Ch10 Inference / RAG / Serving",
        "经典 NLP 专题题",
    ],
    "docs/instructor-solution-guide.md": [
        "使用规则",
        "书面题选择与证据矩阵",
        "正式作业建议题",
        "满分证据下限",
        "人工复核重点",
        "10 分制",
        "Ch01 Tokenization / BPE",
        "Ch02 Embedding / Position Encoding / RoPE",
        "Ch03 Scaled Dot-Product Attention",
        "Ch04 MHA / GQA / MLA",
        "Ch05 Transformer Block / Norm / FFN",
        "Ch06 GPT Assembly / MoE",
        "Ch07 Training Loop",
        "Ch08 Generation / Decoding",
        "Ch09 Fine-tuning / Alignment",
        "Ch10 Inference / RAG / Serving",
        "经典 NLP 专题",
        "常见扣分",
    ],
    "docs/grading-calibration.md": [
        "Grading Calibration Guide",
        "Gradebook and LMS Operations Guide",
        "Grading Anchor Sample Feedback Pack",
        "Grading Drift Audit Ledger",
        "校准流程",
        "双评一致性规则",
        "书面题校准样例",
        "编程作业校准",
        "Capstone 报告校准",
        "阅读复盘校准",
        "同伴 Review 校准",
        "复核请求处理",
        "regrade_decision_id",
        "校准记录模板",
    ],
    "docs/grading-drift-audit-ledger.md": [
        "Grading Drift Audit Ledger",
        "复核日期：2026-06-05",
        "Drift Signals",
        "Calibration Session Schema",
        "Current Calibration Sessions",
        "Double-Grading Sampling Plan",
        "Drift Audit Metrics",
        "Pause and Recalibration Triggers",
        "Regrade and Batch Correction Linkage",
        "Staff Review Workflow",
        "Release Checklist",
        "GD-DELTA-03",
        "GD-DELTA-08",
        "GD-HIDDEN-BUG",
        "CAL-2026-CH02-PRE",
        "CAL-2026-CAPSTONE-PRE",
        "staff-facing",
    ],
    "docs/ta-training-certification.md": [
        "TA Training and Certification Dossier",
        "复核日期：2026-06-05",
        "Certification Scope",
        "Competency Modules",
        "Certification Matrix",
        "Calibration Practicum",
        "Office Hours Simulation Bank",
        "Privacy, Accessibility, and Integrity Scenario Bank",
        "Current Certification Ledger",
        "Recertification and Escalation",
        "Release Checklist",
        "TA-GRADING",
        "TA-PRIVACY",
        "CAL-WRITTEN-01",
        "OH-SHAPE-01",
        "PAI-ACCESS-01",
        "student site release",
    ],
    "docs/grading-anchor-sample-feedback-pack.md": [
        "Grading Anchor Sample Feedback Pack",
        "Grading Calibration Guide",
        "Grading Drift Audit Ledger",
        "Instructor Solution Guide",
        "Assignment Handout Pack",
        "Gradebook and LMS Operations Guide",
        "Use Rules",
        "Written Anchor Samples",
        "Programming Anchor Samples",
        "Capstone Anchor Samples",
        "Reading And Peer Review Anchor Samples",
        "Regrade Anchor Samples",
        "Feedback Templates",
        "Double-Grading Resolution",
        "Release Checklist",
        "anchor_id",
        "rubric_item",
        "feedback_to_student",
        "calibration_note",
        "second_reader_delta",
        "final_decision",
        "full_credit",
        "partial_credit",
        "borderline",
        "not_passing",
        "no hidden tests",
        "no reference_solution.py",
        "regrade_decision_id",
    ],
    "docs/staff-assistance-code-review-policy.md": [
        "Staff Assistance and Code Review Boundary Policy",
        "Assistance Levels",
        "Assignment Assistance Matrix",
        "Final Project and Capstone Boundary",
        "Office Hours Interaction Rules",
        "Public Forum and Private Channel Boundary",
        "Regrade and Academic Integrity Boundary",
        "Staff Assistance Log",
        "Staff Checklist",
        "发布前 Checklist",
        "limited_code_view",
        "pseudocode_review",
        "artifact_review",
        "rubric_explanation",
        "fairness_followup",
    ],
    "docs/assignment-submission-guide.md": [
        "Assignment Submission and Release Guide",
        "Assignment Handout Pack",
        "Environment and Reproducibility Guide",
        "Gradebook and LMS Operations Guide",
        "Staff Assistance and Code Review Boundary Policy",
        "发布前 Checklist",
        '.venv/bin/python -c "import sys, torch;',
        ".venv/bin/python verify_course.py",
        ".venv/bin/python run_assignment_tests.py",
        ".venv/bin/python verify_course.py --capstone --training",
        "学生提交包",
        "minimal reproduction",
        "attempted fix",
        "学生发布包构建",
        "学生站点发布包构建",
        "scripts/build_assignment_release.py",
        "scripts/build_course_site_release.py",
        "SITE_RELEASE_MANIFEST.json",
        "RELEASE_MANIFEST.json",
        "LMS / Gradescope 配置",
        "运行命令规范",
        "成绩发布说明模板",
        "release_batch",
        "rubric_version",
        "weighted gradebook",
        "regrade_decision_id",
        "复核材料",
        "发布后复盘",
    ],
    "docs/gradebook-lms-operations.md": [
        "Gradebook and LMS Operations Guide",
        "Gradebook Schema",
        "Weight Reconciliation",
        "Late-Day Ledger",
        "Grade Release Checklist",
        "Regrade Workflow",
        "Privacy and Access Control",
        "Operations Log Hooks",
        "Staff Checklist",
        "发布前 Checklist",
        "student_id",
        "grade_category",
        "weight_percent",
        "late_days_used",
        "release_batch",
        "regrade_decision_id",
        "integrity_hold",
    ],
    "docs/environment-reproducibility.md": [
        "Environment and Reproducibility Guide",
        "本仓库当前验证环境",
        "Python",
        "3.12.3",
        "PyTorch",
        "2.12.0+cu130",
        "CUDA 可用性",
        "推荐本地命令",
        '.venv/bin/python -c "import sys, torch;',
        ".venv/bin/python verify_course.py",
        ".venv/bin/python run_assignment_tests.py",
        ".venv/bin/python verify_course.py --capstone --training",
        "依赖版本策略",
        "CPU/GPU 边界",
        "提交日志模板",
        "发布前 Checklist",
    ],
    "docs/autograder-hidden-tests.md": [
        "Autograder 与隐藏测试设计指南",
        "Assignment Handout Pack",
        "Private Autograder Operations Guide",
        "评分分层",
        "scripts/build_assignment_release.py",
        "scripts/run_private_autograder.py",
        "隐藏边界测试",
        "隐藏性质测试",
        "数值容差建议",
        "Ch01 Tokenization / BPE",
        "Ch10 Inference / RAG / Serving",
        "Capstone 隐藏验收",
        "学术诚信与防投机检查",
        "失败日志规范",
    ],
    "docs/private-autograder-operations.md": [
        "Private Autograder Operations Guide",
        "Autograder 与隐藏测试设计指南",
        "Assignment Submission and Release Guide",
        "Grading Anchor Sample Feedback Pack",
        "Gradebook and LMS Operations Guide",
        "scripts/run_private_autograder.py",
        "Directory Boundary",
        "Runbook",
        "Manifest Schema",
        "Rubric Mapping",
        "Failure Log Contract",
        "LMS And Gradescope Entrypoint",
        "Integrity Checks",
        "Regrade And Batch Correction",
        "Release Checklist",
        "private_autograder/hidden_tests/",
        "hidden_tests_stored_in_repo",
        "student_release_excludes",
        "public_unit_tests",
        "hidden_boundary_tests",
        "hidden_property_tests",
        "written_explanation_code_quality",
        "regrade_decision_id",
        "hidden test exact input",
        "reference_solution.py",
    ],
    "docs/assignment-handout-pack.md": [
        "Assignment Handout Pack",
        "统一提交结构",
        "Assignment 1: Tokenization and BPE",
        "Assignment 2: Embeddings and Position Encoding",
        "Assignment 3: Scaled Dot-Product Attention",
        "Assignment 4: Multi-Head Attention, GQA, and MLA",
        "Assignment 5: Transformer Block, Norm, and FFN",
        "Assignment 6: GPT Assembly and MoE",
        "Assignment 7: Training Loop",
        "Assignment 8: Generation and Constrained Decoding",
        "Assignment 9: SFT, LoRA, DPO, and GRPO",
        "Assignment 10: Inference Engineering",
        "Assignment 11: Classic NLP and Evaluation",
        "Written questions",
        "Programming parts",
        "隐藏测试",
        "发布前 Checklist",
    ],
    "docs/capstone-proposal-milestone.md": [
        "Capstone Proposal and Milestone Guide",
        "交付时间线",
        "项目提案模板",
        "Project Report Template and Reproducibility Checklist",
        "Project Submission Dossier",
        "Experimental Rigor and Evaluation Statistics Guide",
        "Compute Resource and Cost Guide",
        "CPU/GPU",
        "Project Team and Mentor Policy",
        "训练工程提案加项",
        "推理工程提案加项",
        "Milestone 模板",
        "训练 milestone 检查表",
        "推理 milestone 检查表",
        "默认最终项目任务包",
        "Milestone 评分",
        "导师反馈记录",
        "最终提交包",
        "project-submission-dossier.md",
        "split_card",
        "metric_card",
        "uncertainty_record",
        "claim_audit",
        "statistics_gate",
        "contamination/leakage",
    ],
    "docs/default-final-project-guide.md": [
        "Default Final Project Guide",
        "Project Report Template and Reproducibility Checklist",
        "项目目标",
        "默认任务包",
        "Task A: Tiny GPT 语言建模",
        "Task B: 生成质量与采样对比",
        "Task C: 固定评测与服务化",
        "Proposal 必填字段",
        "Milestone 必交证据",
        "Final Report 结构",
        "评分细则",
        "不通过条件",
        "发布前 Checklist",
    ],
    "docs/project-team-mentor-policy.md": [
        "Project Team and Mentor Policy",
        "团队规模",
        "组队规则",
        "Mentor 匹配",
        "外部协作者与共享项目",
        "贡献声明",
        "不均衡贡献处理",
        "Mentor Checkpoint 模板",
        "发布前 Checklist",
        "1 人",
        "2 人",
        "3 人",
        "external collaborators",
        "shared project",
        "自评贡献比例",
        "downgrade_trigger",
    ],
    "docs/capstone-project-gallery.md": [
        "Capstone Project Gallery and Idea Bank",
        "使用目标",
        "项目类型",
        "Final Project Showcase and Archive Policy",
        "默认最终项目任务包",
        "选题库",
        "训练工程方向",
        "推理工程方向",
        "经典 NLP 与评测方向",
        "自定义项目边界",
        "导师匹配",
        "贡献声明",
        "项目报告归档",
        "发布前 Checklist",
    ],
    "docs/final-project-showcase-archive-policy.md": [
        "Final Project Showcase and Archive Policy",
        "Project Submission Dossier",
        "Project Report Exemplar Pack",
        "Showcase 形式",
        "Poster Session 运行规则",
        "公开归档资格",
        "Redaction Checklist",
        "Artifact Retention",
        "Archive Record Template",
        "学生说明",
        "Staff Checklist",
        "发布前 Checklist",
        "poster session",
        "archived final report",
        "staff-only evaluation packet",
        "consent",
        "redaction",
        "artifact_manifest",
        "archived public report",
        "staff-only",
    ],
    "docs/project-report-exemplar-pack.md": [
        "Project Report Exemplar Pack",
        "Project Report Template and Reproducibility Checklist",
        "Capstone 项目报告 Rubric",
        "Experimental Rigor and Evaluation Statistics Guide",
        "Final Project Showcase and Archive Policy",
        "Capstone Project Gallery and Idea Bank",
        "Use Rules",
        "Exemplar Overview",
        "EX-INF-A-01",
        "EX-TRAIN-B-01",
        "EX-DEFAULT-C-01",
        "EX-NP-FAIL-01",
        "Rubric Mapping",
        "Exemplar Review Worksheet",
        "Archive Boundary",
        "synthetic_status",
        "score_band",
        "student_visible",
        "claim_audit",
        "uncertainty_record",
        "split_card",
        "metric_card",
        "artifact_manifest",
        "archived_label",
        "not_passing",
    ],
    "docs/project-submission-dossier.md": [
        "Project Submission Dossier",
        "复核日期：2026-06-05",
        "Dossier Stages",
        "Required File Map",
        "Structured Templates",
        "Stage Acceptance Matrix",
        "TA Review Procedure",
        "Common Downgrade Decisions",
        "Student Final Checklist",
        "Release Checklist",
        "DSR-PROPOSAL",
        "DSR-MILESTONE",
        "DSR-FINAL",
        "DSR-PRESENTATION",
        "DSR-ARCHIVE",
        "artifact_manifest",
        "split_card",
        "metric_card",
        "uncertainty_record",
        "claim_audit",
        "leakage_check",
    ],
    "docs/data-ethics-review.md": [
        "Data and Ethics Review",
        "Safety and Societal Impact Casebook",
        "适用范围",
        "提交格式",
        "数据来源与许可证",
        "Dataset, Model, and Artifact Provenance Registry",
        "隐私与 PII",
        "偏见与代表性",
        "评测污染与数据泄漏",
        "安全边界",
        "模型卡与 API 文档",
        "最终报告必含小节",
        "评分 Rubric",
        "审查记录模板",
    ],
    "docs/safety-societal-impact-casebook.md": [
        "Safety and Societal Impact Casebook",
        "复核日期：2026-06-05",
        "Case Analysis Schema",
        "Core Cases",
        "Classroom Use",
        "Assessment Rubric",
        "Staff Review Workflow",
        "Release Checklist",
        "SSI-RAG-MED",
        "SSI-HIRING-BIAS",
        "SSI-PROMPT-INJECT",
        "SSI-LLM-JUDGE",
        "privacy",
        "bias",
        "student site release",
    ],
    "docs/model-benchmark-card-guide.md": [
        "Model and Benchmark Card Guide",
        "复核日期：2026-06-05",
        "Card Schema",
        "Model Card Checklist",
        "Benchmark Card Checklist",
        "Course Card Examples",
        "Claim Rewrite Rules",
        "Student Submission Template",
        "Staff Review Workflow",
        "Release Checklist",
        "MBC-MODEL-ID",
        "MBC-BENCH-TASK",
        "MBC-EX-VOLATILE-CONTEXT",
        "MBC-R6",
        "student site release",
    ],
    "docs/capstone-defense-oral-exam-bank.md": [
        "Capstone Defense and Oral Exam Question Bank",
        "复核日期：2026-06-05",
        "Defense Format",
        "Question Schema",
        "Core Defense Questions",
        "Track-Specific Follow-Ups",
        "Scoring Rubric",
        "Sampling Rules",
        "Oral Record Template",
        "Staff Workflow",
        "Release Checklist",
        "DEF-CONTRIB-01",
        "DEF-EXP-05",
        "DEF-SOURCE-01",
        "DEF-SAMPLE-CO4",
        "student site release",
    ],
    "docs/programming-assignment-code-quality-rubric.md": [
        "Programming Assignment Code Quality Rubric",
        "复核日期：2026-06-05",
        "Rubric Dimensions",
        "Assignment-Specific Review Cues",
        "Manual Review Triggers",
        "Student Self-Check",
        "TA Review Workflow",
        "Release Checklist",
        "CQR-API",
        "CQR-SHAPE",
        "CQR-VECTOR",
        "CQR-NUMERIC",
        "CQR-CH11",
        "CQR-TRIG-HARDCODE",
        "student site release",
    ],
    "docs/dataset-model-artifact-registry.md": [
        "Dataset, Model, and Artifact Provenance Registry",
        "复核日期：2026-06-05",
        "Artifact Type Taxonomy",
        "Registry Schema",
        "Course Artifact Registry",
        "License and Access Rules",
        "Contamination and Privacy Gates",
        "Student Submission Requirements",
        "Staff Review Workflow",
        "Release Checklist",
        "Project Submission Dossier",
        "artifact_manifest",
        "ART-CH07-SAMPLE-CORPUS",
        "ART-PROJECT-STUDENT-DATA",
    ],
    "docs/classic-nlp-handout.md": [
        "Dependency Parsing",
        "Seq2Seq / Neural Machine Translation",
        "Encoder-only / BERT",
        "Worked Example",
        "Beam Search Length Bias",
        "BERT-style MLM Tensor",
        "Metric Failure Cases",
        "Mini-Recitation Checklist",
        "Ethics / Safety",
    ],
    "docs/classic-nlp-deep-dive-module.md": [
        "Classic NLP Deep-Dive Teaching Module",
        "Module Outcomes",
        "Suggested Lecture Split",
        "Dependency Parsing Deep Dive",
        "Seq2Seq / NMT Deep Dive",
        "Encoder-only / BERT Deep Dive",
        "Assessment Pack",
        "Teaching Misconception Register",
        "Source And Update Boundary",
        "CL-NLP-1",
        "CL-NLP-2",
        "CL-NLP-3",
        "CL-NLP-4",
        "CL-NLP-5",
        "UAS =",
        "LAS =",
        "p(y | x)",
        "L_MLM",
        "encoder-only",
        "encoder-decoder",
        "decoder-only",
    ],
    "docs/nlp-evaluation-coverage.md": [
        "Dependency Parsing",
        "Seq2Seq / NMT",
        "Encoder-only / BERT",
        "Classic NLP Deep-Dive Teaching Module",
        "Evaluation",
        "assignments/ch11_classic_nlp/",
        "Ethics / Safety",
        "Experimental Rigor and Evaluation Statistics Guide",
        "bootstrap confidence interval",
        "seed sensitivity",
        "significance claim gate",
        "contamination/leakage gate",
    ],
    "docs/experimental-rigor-evaluation-statistics.md": [
        "Experimental Rigor and Evaluation Statistics Guide",
        "Scope",
        "Evaluation Split Protocol",
        "Metric Selection and Limits",
        "Uncertainty and Confidence Intervals",
        "Significance Claim Gate",
        "Error Analysis and Failure Taxonomy",
        "Contamination and Leakage Gate",
        "Minimum Evidence Packet",
        "TA Audit Checklist",
        "发布前 Checklist",
        "split_card",
        "metric_card",
        "uncertainty_record",
        "claim_audit",
        "bootstrap confidence interval",
        "repeated-run seed sensitivity",
        "single_seed_limit",
        "benchmark contamination",
    ],
    "docs/project-report-rubric.md": [
        "Project Report Template and Reproducibility Checklist",
        "Experimental Rigor and Evaluation Statistics Guide",
        "Project Report Exemplar Pack",
        "通用评分",
        "训练工程加分检查",
        "推理工程加分检查",
        "默认最终项目加分检查",
        "不通过条件",
    ],
    "docs/project-report-template.md": [
        "Project Report Template and Reproducibility Checklist",
        "Experimental Rigor and Evaluation Statistics Guide",
        "Project Report Exemplar Pack",
        "Title and Metadata",
        "Final Project Showcase and Archive Policy",
        "Abstract",
        "Problem Definition",
        "Method and Implementation",
        "Data, Ethics, and Limitations",
        "Experiments",
        "Results",
        "Error Analysis",
        "Cost and Reproducibility",
        "Contributions and Disclosure",
        "Conclusion and Open Questions",
        "Final Submission Checklist",
        "TA Review Checklist",
    ],
    "docs/presentation-peer-review.md": [
        "展示评分",
        "Final Project Showcase and Archive Policy",
        "同伴 Review 表单",
        "阅读复盘",
        "来源审计",
        "提交要求",
    ],
    "docs/frontier-source-audit.md": [
        "复核日期：2026-06-05",
        "来源等级",
        "DeepSeek 技术声明复核表",
        "External Source Verification Guide",
        "monitor-only",
    ],
    "docs/frontier-source-evidence-cards.md": [
        "Frontier Source Evidence Cards",
        "复核日期：2026-06-05",
        "Evidence Card Schema",
        "Current Evidence Cards",
        "Upgrade and Downgrade Rules",
        "Release Checklist",
        "FSEC-DSA-2026-0605",
        "FSEC-V4-ARCH-2026-0605",
        "FSEC-V4-MTP-MONITOR-2026-0605",
        "FSEC-ENGRAM-MONITOR-2026-0605",
        "monitor-only",
        "not for scoring",
    ],
}


def ok(message: str) -> None:
    print(f"PASS {message}")


def fail(message: str) -> None:
    raise RuntimeError(message)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def extract_first_score_table(text: str, marker: str) -> list[int]:
    marker_line = None
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if marker in line:
            marker_line = index
            break
    if marker_line is None:
        fail(f"missing rubric marker: {marker}")

    table_lines: list[str] = []
    in_table = False
    for line in lines[marker_line + 1 :]:
        if line.startswith("|"):
            in_table = True
            table_lines.append(line)
        elif in_table:
            break

    scores: list[int] = []
    for line in table_lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        score_cell = cells[1].replace("%", "").strip()
        if re.fullmatch(r"\d+", score_cell):
            scores.append(int(score_cell))
    if not scores:
        fail(f"rubric marker has no numeric scores: {marker}")
    return scores


def extract_first_score_rows(text: str, marker: str) -> list[tuple[str, int]]:
    marker_line = None
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if marker in line:
            marker_line = index
            break
    if marker_line is None:
        fail(f"missing rubric marker: {marker}")

    table_lines: list[str] = []
    in_table = False
    for line in lines[marker_line + 1 :]:
        if line.startswith("|"):
            in_table = True
            table_lines.append(line)
        elif in_table:
            break

    rows: list[tuple[str, int]] = []
    for line in table_lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        score_cell = cells[1].replace("%", "").strip()
        if re.fullmatch(r"\d+", score_cell):
            rows.append((cells[0], int(score_cell)))
    if not rows:
        fail(f"rubric marker has no labeled numeric scores: {marker}")
    return rows


def extract_markdown_table_after(text: str, marker: str) -> list[list[str]]:
    lines = text.splitlines()
    marker_index = None
    for index, line in enumerate(lines):
        if marker in line:
            marker_index = index
            break
    if marker_index is None:
        fail(f"missing table marker: {marker}")

    table_lines: list[str] = []
    in_table = False
    for line in lines[marker_index + 1 :]:
        if line.startswith("|"):
            in_table = True
            table_lines.append(line)
        elif in_table:
            break

    rows: list[list[str]] = []
    for line in table_lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        rows.append(cells)
    return rows


def markdown_files() -> list[Path]:
    files = [ROOT / "README.md"]
    files.extend(sorted((ROOT / "docs").glob("*.md")))
    files.extend(sorted((ROOT / "assignments").glob("*/README.md")))
    files.extend(sorted((ROOT / "projects").glob("*/README.md")))
    return [path for path in files if path.exists()]


def normalize_wrapped_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if not target:
        return ""
    if (target[0] == target[-1]) and target.startswith(("'", '"')):
        target = target[1:-1].strip()
    return target


def split_link_target(raw_target: str) -> tuple[str, str]:
    target = normalize_wrapped_link_target(raw_target)
    path_part, fragment = (target.split("#", 1) + [""])[:2]
    return path_part.strip(), fragment.strip()


def markdown_slug(heading: str) -> str:
    text = re.sub(r"<[^>]+>", "", heading.strip().lower())
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"[^\w\u4e00-\u9fff\- ]", "", text)
    return re.sub(r"\s+", "-", text).strip("-")


def markdown_anchors(path: Path) -> set[str]:
    anchors = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*#*$", line)
        if match:
            anchors.add(markdown_slug(match.group(2)))
    return anchors


def check_markdown_links() -> None:
    broken = []
    checked = 0
    anchors_checked = 0
    markdown_anchor_cache: dict[Path, set[str]] = {}
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            raw_target = match.group(1)
            target, fragment = split_link_target(raw_target)
            normalized_target = normalize_wrapped_link_target(raw_target)
            if normalized_target.startswith(EXTERNAL_LINK_PREFIXES):
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", normalized_target):
                continue

            target_path = path if not target else (path.parent / unquote(target)).resolve()
            if target:
                checked += 1
                if not str(target_path).startswith(str(ROOT)):
                    broken.append((path.relative_to(ROOT), raw_target, "target escapes repository"))
                    continue
                if not target_path.exists():
                    broken.append((path.relative_to(ROOT), raw_target, "missing target"))
                    continue

            if fragment and target_path.suffix == ".md" and target_path.exists():
                anchors_checked += 1
                anchors = markdown_anchor_cache.setdefault(target_path, markdown_anchors(target_path))
                if unquote(fragment).lower() not in anchors:
                    broken.append((path.relative_to(ROOT), raw_target, "missing markdown anchor"))

    if broken:
        details = "; ".join(f"{source}: {target} ({reason})" for source, target, reason in broken[:10])
        fail(f"broken markdown links: {details}")
    if anchors_checked < MIN_MARKDOWN_ANCHOR_LINKS:
        fail(
            "markdown anchor coverage is too low: "
            f"{anchors_checked} checked, expected at least {MIN_MARKDOWN_ANCHOR_LINKS}"
        )
    ok(f"markdown internal links are valid ({checked} targets, {anchors_checked} anchors checked)")


def split_markdown_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def is_markdown_separator_row(line: str) -> bool:
    if "|" not in line:
        return False
    cells = split_markdown_table_row(line)
    if not cells:
        return False
    return all(re.fullmatch(r":?-+:?", cell.strip()) for cell in cells)


def markdown_table_blocks(path: Path) -> list[list[tuple[int, str]]]:
    blocks: list[list[tuple[int, str]]] = []
    current: list[tuple[int, str]] = []
    in_fence = False
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            if current:
                blocks.append(current)
                current = []
            continue
        if in_fence:
            continue
        if stripped.startswith("|"):
            current.append((lineno, line))
        else:
            if current:
                blocks.append(current)
                current = []
    if current:
        blocks.append(current)
    return blocks


def check_markdown_table_structure() -> None:
    issues = []
    table_count = 0

    for path in markdown_files():
        rel = path.relative_to(ROOT)
        lines = path.read_text(encoding="utf-8").splitlines()
        for block in markdown_table_blocks(path):
            if len(block) == 1:
                lineno, line = block[0]
                next_line = lines[lineno] if lineno < len(lines) else ""
                if is_markdown_separator_row(next_line) and not next_line.strip().startswith("|"):
                    issues.append(f"{rel}:{lineno + 1} separator row must start with |")
                continue

            header_lineno, header = block[0]
            separator_lineno, separator = block[1]
            header_cells = split_markdown_table_row(header)
            separator_cells = split_markdown_table_row(separator)

            if not is_markdown_separator_row(separator):
                issues.append(f"{rel}:{separator_lineno} invalid markdown table separator")
                continue
            if len(separator_cells) != len(header_cells):
                issues.append(
                    f"{rel}:{separator_lineno} separator has {len(separator_cells)} cells, "
                    f"header at line {header_lineno} has {len(header_cells)}"
                )
                continue

            table_count += 1
            for data_lineno, data_line in block[2:]:
                data_cells = split_markdown_table_row(data_line)
                if len(data_cells) != len(header_cells):
                    issues.append(
                        f"{rel}:{data_lineno} row has {len(data_cells)} cells, "
                        f"header at line {header_lineno} has {len(header_cells)}"
                    )

    if issues:
        fail(f"malformed markdown tables: {'; '.join(issues[:10])}")
    ok(f"markdown tables have valid separator rows and column counts ({table_count} tables)")


class LocalLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str, str]] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {attr: value for attr, value in attrs if value}
        for attr in ("id", "name"):
            if attr in attr_map:
                self.anchors.add(attr_map[attr] or "")
        for attr, value in attrs:
            if attr in {"href", "src"} and value:
                self.links.append((tag, attr, value))


class ImageAccessibilityParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[tuple[int, str, str]] = []
        self.diagram_stack: list[dict[str, object]] = []
        self.diagrams: list[dict[str, object]] = []
        self.pending_diagram: dict[str, object] | None = None
        self.in_caption = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name: value or "" for name, value in attrs}
        classes = set(attr_map.get("class", "").split())
        if tag == "div" and "svg-diagram" in classes:
            self.diagram_stack.append({"line": self.getpos()[0], "images": 0, "caption": ""})
        elif tag == "img":
            src = attr_map.get("src", "")
            alt = attr_map.get("alt", "")
            self.images.append((self.getpos()[0], src, alt))
            if self.diagram_stack:
                self.diagram_stack[-1]["images"] = int(self.diagram_stack[-1]["images"]) + 1
        elif tag == "p" and "diagram-caption" in classes:
            self.in_caption = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self.diagram_stack:
            self.pending_diagram = self.diagram_stack.pop()
            self.diagrams.append(self.pending_diagram)
        elif tag == "p" and self.in_caption:
            self.in_caption = False
            self.pending_diagram = None

    def handle_data(self, data: str) -> None:
        if self.in_caption and self.pending_diagram is not None:
            self.pending_diagram["caption"] = str(self.pending_diagram.get("caption", "")) + data


class KatexExpressionParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.expressions: list[tuple[int, str, str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {attr: value for attr, value in attrs}
        if "data-expr" in attr_map:
            self.expressions.append(
                (
                    self.getpos()[0],
                    tag,
                    attr_map["data-expr"] or "",
                    attr_map.get("aria-label") or "",
                    attr_map.get("role") or "",
                )
            )


class VisibleTextTexParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tag_stack: list[str] = []
        self.line = 1
        self.hits: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tag_stack.append(tag.lower())

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        for index in range(len(self.tag_stack) - 1, -1, -1):
            if self.tag_stack[index] == tag:
                del self.tag_stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if not any(tag in HTML_RAW_TEXT_TAGS for tag in self.tag_stack):
            match = VISIBLE_TEX_COMMAND_RE.search(data)
            if match:
                snippet = " ".join(data.strip().split())
                self.hits.append((self.line, snippet[:120]))
        self.line += data.count("\n")


class ExerciseWidgetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.current: dict[str, object] | None = None
        self.exercises: list[dict[str, object]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name: value or "" for name, value in attrs}
        classes = set(attr_map.get("class", "").split())
        if tag == "div" and "exercise" in classes:
            self.current = {
                "line": self.getpos()[0],
                "answer": attr_map.get("data-answer", ""),
                "explain": attr_map.get("data-explain", ""),
                "inputs": [],
                "onclicks": [],
                "has_feedback": False,
            }
            self.stack.append("exercise")
            return

        if self.current is not None:
            if tag == "input" and attr_map.get("type") == "radio":
                self.current["inputs"].append((attr_map.get("name", ""), attr_map.get("value", "")))
                return
            elif tag == "button" and attr_map.get("onclick", "").startswith("LLM.checkMC"):
                self.current["onclicks"].append(attr_map.get("onclick", ""))
            elif tag == "div" and "feedback" in classes:
                self.current["has_feedback"] = True
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if self.current is None or not self.stack:
            return
        if self.stack[-1] == "exercise" and tag == "div":
            self.exercises.append(self.current)
            self.current = None
            self.stack.pop()
            return
        self.stack.pop()


class PythonCodeBlockParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_code = False
        self.depth = 0
        self.start_line = 0
        self.current: list[str] = []
        self.blocks: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name: value or "" for name, value in attrs}
        classes = set(attr_map.get("class", "").split())
        if tag == "div" and "code-block" in classes and attr_map.get("data-lang") == "python":
            self.in_code = True
            self.depth = 1
            self.start_line = self.getpos()[0]
            self.current = []
            return
        if self.in_code:
            self.depth += 1

    def handle_endtag(self, tag: str) -> None:
        if not self.in_code:
            return
        self.depth -= 1
        if self.depth == 0:
            self.blocks.append((self.start_line, "".join(self.current)))
            self.in_code = False

    def handle_data(self, data: str) -> None:
        if self.in_code:
            self.current.append(data)


def html_files() -> list[Path]:
    files = sorted(ROOT.glob("*.html"))
    files.extend(sorted((ROOT / "chapters").glob("*.html")))
    return files


def strip_html_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    target = target.split("#", 1)[0].split("?", 1)[0].strip()
    return target


def is_skipped_local_link(raw_target: str) -> bool:
    raw_stripped = raw_target.strip()
    if not raw_stripped:
        return True
    if raw_stripped.startswith(HTML_SKIP_LINK_PREFIXES) and not raw_stripped.startswith("#"):
        return True
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw_stripped))


def check_html_links() -> None:
    broken = []
    checked = 0
    anchors_checked = 0
    parser_cache: dict[Path, LocalLinkParser] = {}
    for html_path in html_files():
        parser = LocalLinkParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        parser_cache[html_path] = parser

    for path, parser in parser_cache.items():
        for tag, attr, raw_target in parser.links:
            target = strip_html_link_target(raw_target)
            raw_stripped = raw_target.strip()
            if is_skipped_local_link(raw_target):
                continue

            target_path = path if not target else (path.parent / unquote(target)).resolve()
            if target:
                checked += 1
                if not str(target_path).startswith(str(ROOT)):
                    broken.append((path.relative_to(ROOT), tag, attr, raw_target, "target escapes repository"))
                    continue
                if not target_path.exists():
                    broken.append((path.relative_to(ROOT), tag, attr, raw_target, "missing target"))
                    continue

            if "#" in raw_target and target_path.suffix == ".html" and target_path.exists():
                fragment = raw_target.split("#", 1)[1].split("?", 1)[0].strip()
                if fragment:
                    anchors_checked += 1
                    target_parser = parser_cache.get(target_path)
                    if target_parser is None:
                        target_parser = LocalLinkParser()
                        target_parser.feed(target_path.read_text(encoding="utf-8"))
                        parser_cache[target_path] = target_parser
                    if unquote(fragment) not in target_parser.anchors:
                        broken.append((path.relative_to(ROOT), tag, attr, raw_target, "missing html anchor"))

    if broken:
        details = "; ".join(
            f"{source}: <{tag} {attr}={target!r}> ({reason})"
            for source, tag, attr, target, reason in broken[:10]
        )
        fail(f"broken html local links: {details}")
    if anchors_checked < MIN_HTML_ANCHOR_LINKS:
        fail(
            "html anchor coverage is too low: "
            f"{anchors_checked} checked, expected at least {MIN_HTML_ANCHOR_LINKS}"
        )
    ok(f"html local links are valid ({checked} targets, {anchors_checked} anchors checked)")


def collect_release_local_links(release_root: Path) -> tuple[int, list[str]]:
    broken: list[str] = []
    checked = 0

    for html_path in sorted(release_root.rglob("*.html")):
        parser = LocalLinkParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        for tag, attr, raw_target in parser.links:
            if is_skipped_local_link(raw_target):
                continue
            target = strip_html_link_target(raw_target)
            if not target:
                continue
            target_path = (html_path.parent / unquote(target)).resolve()
            checked += 1
            if not str(target_path).startswith(str(release_root.resolve())):
                broken.append(
                    f"{html_path.relative_to(release_root)}: <{tag} {attr}={raw_target!r}> escapes release root"
                )
            elif not target_path.exists():
                broken.append(
                    f"{html_path.relative_to(release_root)}: <{tag} {attr}={raw_target!r}> missing target"
                )

    for markdown_path in sorted(release_root.rglob("*.md")):
        text = markdown_path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            raw_target = match.group(1).strip()
            if is_skipped_local_link(raw_target):
                continue
            target = strip_html_link_target(raw_target)
            if not target:
                continue
            target_path = (markdown_path.parent / unquote(target)).resolve()
            checked += 1
            if not str(target_path).startswith(str(release_root.resolve())):
                broken.append(f"{markdown_path.relative_to(release_root)}: markdown link {raw_target!r} escapes release root")
            elif not target_path.exists():
                broken.append(f"{markdown_path.relative_to(release_root)}: markdown link {raw_target!r} missing target")

    return checked, broken


def check_image_accessibility() -> None:
    readme = read("README.md")
    missing_inventory = []
    for image_name in EXPECTED_CONCEPT_IMAGES:
        image_path = ROOT / "images" / image_name
        if not image_path.exists():
            missing_inventory.append(f"missing image file: images/{image_name}")
        if image_name not in readme:
            missing_inventory.append(f"README image inventory missing: {image_name}")
    if "11 张 SVG 概念示意图 + favicon" not in readme:
        missing_inventory.append("README image inventory must state 11 concept SVGs plus favicon")

    image_hits = []
    diagram_hits = []
    diagram_images: set[str] = set()
    diagram_count = 0
    for path in sorted((ROOT / "chapters").glob("ch*.html")):
        parser = ImageAccessibilityParser()
        parser.feed(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT)
        for line, src, alt in parser.images:
            if src.startswith("../images/") and src.endswith(".svg"):
                image_name = Path(src).name
                diagram_images.add(image_name)
                if image_name not in EXPECTED_CONCEPT_IMAGES:
                    image_hits.append((rel, line, f"unexpected concept image {image_name}"))
                if not alt.strip() or len(alt.strip()) < 6:
                    image_hits.append((rel, line, f"missing or too-short alt for {src}"))

        for diagram in parser.diagrams:
            diagram_count += 1
            line = int(diagram["line"])
            images = int(diagram["images"])
            caption = str(diagram.get("caption", "")).strip()
            if images != 1:
                diagram_hits.append((rel, line, f"expected one image in svg diagram, got {images}"))
            if not caption.startswith("图 ") and not caption.startswith("图"):
                diagram_hits.append((rel, line, "missing diagram caption"))

    missing_diagrams = sorted(set(EXPECTED_CONCEPT_IMAGES) - diagram_images)
    extra_diagrams = sorted(diagram_images - set(EXPECTED_CONCEPT_IMAGES))
    if missing_diagrams:
        missing_inventory.append(f"chapter diagrams missing expected images: {', '.join(missing_diagrams)}")
    if extra_diagrams:
        missing_inventory.append(f"chapter diagrams include unexpected images: {', '.join(extra_diagrams)}")
    if diagram_count != len(EXPECTED_CONCEPT_IMAGES):
        missing_inventory.append(
            f"expected {len(EXPECTED_CONCEPT_IMAGES)} chapter diagrams, got {diagram_count}"
        )

    if missing_inventory or image_hits or diagram_hits:
        details = "; ".join(
            missing_inventory[:5]
            + [f"{path}:{line} {reason}" for path, line, reason in (image_hits + diagram_hits)[:10]]
        )
        fail(f"image accessibility/inventory issues: {details}")
    ok(f"chapter diagrams have accessible alt text and captions ({diagram_count} diagrams)")


def text_format_files() -> list[Path]:
    files = [ROOT / "README.md"]
    files.extend(sorted((ROOT / "docs").glob("*.md")))
    files.extend(sorted((ROOT / "assignments").glob("**/*.py")))
    files.extend(sorted((ROOT / "assignments").glob("*/README.md")))
    files.extend(sorted((ROOT / "chapters").glob("*.html")))
    return [path for path in files if path.exists()]


def external_source_files() -> list[Path]:
    files = [ROOT / "README.md"]
    files.extend(sorted((ROOT / "docs").glob("*.md")))
    files.extend(sorted((ROOT / "chapters").glob("*.html")))
    files.extend(sorted((ROOT / "assignments").glob("**/*.py")))
    files.extend(sorted((ROOT / "assignments").glob("*/README.md")))
    files.extend(sorted((ROOT / "projects").glob("**/*.py")))
    files.extend(sorted((ROOT / "projects").glob("*/README.md")))
    return [path for path in files if path.exists()]


def normalize_external_url(raw_url: str) -> str:
    return raw_url.rstrip(".,;:|]}")


def strip_escaped_chars(expr: str) -> str:
    result = []
    i = 0
    while i < len(expr):
        if expr[i] == "\\" and i + 1 < len(expr):
            result.append("  ")
            i += 2
        else:
            result.append(expr[i])
            i += 1
    return "".join(result)


def validate_formula_structure(expr: str) -> list[str]:
    errors = []
    if "&lt;" in expr or "&gt;" in expr or "&amp;" in expr:
        errors.append("contains raw HTML entity after parser decoding")
    if SUSPICIOUS_FORMULA_TEXT_RE.search(expr):
        errors.append("suspicious text/formula boundary, such as \\text{vec( or dash inside \\text{...}")
    if any(dash in expr for dash in ("——", "—", "–")):
        errors.append("contains prose dash inside formula expression")

    begin_envs = re.findall(r"\\begin\{([^}]+)\}", expr)
    end_envs = re.findall(r"\\end\{([^}]+)\}", expr)
    if begin_envs != end_envs:
        errors.append(f"begin/end mismatch: begin={begin_envs}, end={end_envs}")

    stripped = strip_escaped_chars(expr)
    stack: list[tuple[str, int]] = []
    for index, char in enumerate(stripped):
        if char in BRACKET_PAIRS:
            stack.append((char, index))
        elif char in BRACKET_PAIRS.values():
            if not stack:
                errors.append(f"unmatched closing {char!r}")
                continue
            opening, _ = stack.pop()
            if BRACKET_PAIRS[opening] != char:
                errors.append(f"mismatched {opening!r} ... {char!r}")
    if stack:
        opening, _ = stack[-1]
        errors.append(f"unclosed {opening!r}")

    return errors


def check_external_source_inventory_coverage() -> None:
    inventory_path = ROOT / "docs/external-source-inventory.md"
    if not inventory_path.exists():
        fail("missing external source inventory")

    inventory = inventory_path.read_text(encoding="utf-8")
    missing_domains: dict[str, set[str]] = {}
    discovered_domains: set[str] = set()
    discovered_urls = 0
    for path in external_source_files():
        text = path.read_text(encoding="utf-8")
        for match in EXTERNAL_URL_RE.finditer(text):
            url = normalize_external_url(match.group(0))
            if "{" in url or "}" in url:
                continue
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            if not domain:
                continue
            if "@" in domain:
                domain = domain.rsplit("@", 1)[-1]
            if ":" in domain:
                domain = domain.split(":", 1)[0]
            if domain in INVENTORY_EXEMPT_DOMAINS:
                continue
            discovered_urls += 1
            discovered_domains.add(domain)
            if domain not in inventory:
                rel = str(path.relative_to(ROOT))
                missing_domains.setdefault(domain, set()).add(rel)

    if missing_domains:
        details = "; ".join(
            f"{domain} in {', '.join(sorted(paths)[:3])}"
            for domain, paths in sorted(missing_domains.items())[:10]
        )
        fail(f"external source inventory missing domains: {details}")

    ok(f"external source inventory covers {len(discovered_domains)} domains / {discovered_urls} external URLs")


def check_dataset_model_artifact_registry() -> None:
    rel = "docs/dataset-model-artifact-registry.md"
    text = read(rel)

    linked_docs = [
        "data-ethics-review.md",
        "external-source-inventory.md",
        "environment-reproducibility.md",
        "experimental-rigor-evaluation-statistics.md",
        "project-report-template.md",
        "paper-to-code-traceability-matrix.md",
        "compute-resource-guide.md",
    ]
    issues: list[str] = []
    for linked_doc in linked_docs:
        if linked_doc not in text:
            issues.append(f"registry missing linked governance doc: {linked_doc}")

    taxonomy_rows = extract_markdown_table_after(text, "## Artifact Type Taxonomy")
    taxonomy_types = {cells[0] for cells in taxonomy_rows[1:] if cells}
    required_types = {
        "dataset",
        "synthetic_fixture",
        "evaluation_set",
        "tokenizer",
        "model_artifact",
        "runtime_asset",
        "generated_sample",
        "student_project_data",
    }
    missing_types = sorted(required_types - taxonomy_types)
    if missing_types:
        issues.append(f"registry taxonomy missing types: {', '.join(missing_types)}")

    schema_rows = extract_markdown_table_after(text, "## Registry Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    required_schema_fields = {
        "artifact_id",
        "artifact_type",
        "course_use",
        "storage_location",
        "source_or_origin",
        "license_or_access",
        "pii_risk",
        "contamination_risk",
        "student_action",
        "review_gate",
    }
    missing_schema = sorted(required_schema_fields - schema_fields)
    if missing_schema:
        issues.append(f"registry schema missing fields: {', '.join(missing_schema)}")

    registry_rows = extract_markdown_table_after(text, "## Course Artifact Registry")
    registry_ids: set[str] = set()
    registry_types: set[str] = set()
    risk_values = {"none", "low", "medium", "high"}
    bad_rows: list[str] = []
    for cells in registry_rows[1:]:
        if len(cells) != 10:
            bad_rows.append(f"expected 10 cells, got {len(cells)}: {cells[:2]}")
            continue
        artifact_id, artifact_type, _, location, origin, license_or_access, pii_risk, contamination_risk, student_action, review_gate = cells
        registry_ids.add(artifact_id)
        registry_types.add(artifact_type)
        if artifact_type not in taxonomy_types:
            bad_rows.append(f"{artifact_id}: unknown artifact_type {artifact_type!r}")
        if not location or not origin or not license_or_access or not student_action or not review_gate:
            bad_rows.append(f"{artifact_id}: incomplete provenance row")
        if pii_risk not in risk_values:
            bad_rows.append(f"{artifact_id}: invalid pii_risk {pii_risk!r}")
        if contamination_risk not in risk_values:
            bad_rows.append(f"{artifact_id}: invalid contamination_risk {contamination_risk!r}")
    if len(registry_ids) < 14:
        issues.append(f"expected at least 14 artifact registry rows, got {len(registry_ids)}")
    if bad_rows:
        issues.extend(bad_rows[:8])

    required_artifact_ids = {
        "ART-CH01-BPE-ROUNDTRIP",
        "ART-CH02-TOY-EMBED",
        "ART-CH03-ATTN-MASKS",
        "ART-CH04-KV-CACHE-TOY",
        "ART-CH07-SAMPLE-CORPUS",
        "ART-CH07-CHAR-TOKENIZER",
        "ART-TRAIN-CHECKPOINT-LATEST",
        "ART-CH08-GENERATION-PROMPTS",
        "ART-CH09-TINY-CHAT-DATA",
        "ART-CH10-RAG-EVAL-CASES",
        "ART-CH11-NLP-METRIC-EXAMPLES",
        "ART-CS224N-SNAPSHOT-MARKERS",
        "ART-KATEX-CDN",
        "ART-PROJECT-STUDENT-DATA",
        "ART-PROJECT-MODEL-CARD",
    }
    missing_ids = sorted(required_artifact_ids - registry_ids)
    if missing_ids:
        issues.append(f"registry missing required artifact IDs: {', '.join(missing_ids)}")

    expected_registry_types = {"dataset", "synthetic_fixture", "evaluation_set", "tokenizer", "model_artifact", "runtime_asset", "student_project_data"}
    missing_registry_types = sorted(expected_registry_types - registry_types)
    if missing_registry_types:
        issues.append(f"registry rows missing artifact types: {', '.join(missing_registry_types)}")

    required_gates = [
        "license_gate",
        "redistribution_gate",
        "runtime_asset_gate",
        "pii_gate",
        "contamination_gate",
        "split_gate",
        "hidden_test_gate",
        "artifact_size_gate",
        "model_card_gate",
        "safety_boundary_gate",
    ]
    for gate in required_gates:
        if gate not in text:
            issues.append(f"registry missing review gate: {gate}")

    linked_files = {
        "README.md": "Dataset, Model, and Artifact Provenance Registry",
        "docs/data-ethics-review.md": "dataset-model-artifact-registry.md",
        "docs/external-source-inventory.md": "dataset-model-artifact-registry.md",
        "docs/environment-reproducibility.md": "dataset-model-artifact-registry.md",
        "docs/project-report-template.md": "dataset-model-artifact-registry.md",
        "docs/experimental-rigor-evaluation-statistics.md": "dataset-model-artifact-registry.md",
        "scripts/build_course_site_release.py": "dataset-model-artifact-registry.md",
        "scripts/generate_course_evidence_manifest.py": "docs/dataset-model-artifact-registry.md",
    }
    for linked_file, marker in linked_files.items():
        if marker not in read(linked_file):
            issues.append(f"{linked_file} missing registry link/marker: {marker}")

    if issues:
        fail(f"dataset/model artifact registry incomplete: {'; '.join(issues[:12])}")
    ok(
        "dataset/model artifact registry covers taxonomy, schema, required artifact IDs, "
        f"risk gates, and release links ({len(registry_ids)} artifacts)"
    )


def check_source_governance_docs() -> None:
    inventory = read("docs/external-source-inventory.md")
    frontier = read("docs/frontier-source-audit.md")
    source_map = read("docs/chapter-source-map.md")

    required_inventory_markers = [
        "复核日期：2026-06-05",
        "A-stable",
        "A-volatile",
        "B-implementation",
        "C-background",
        "Runtime asset",
        "发布前 Checklist",
    ]
    for marker in required_inventory_markers:
        if marker not in inventory:
            fail(f"external source inventory missing governance marker: {marker}")

    inventory_sections = [
        "## 基础论文与教材",
        "## 前沿模型与厂商来源",
        "## 框架与工程文档",
        "## 课程与学习资源",
    ]
    bad_inventory_rows = []
    row_count = 0
    for section in inventory_sections:
        rows = extract_markdown_table_after(inventory, section)
        for cells in rows[1:]:
            if len(cells) != 6:
                bad_inventory_rows.append(f"{section}: expected 6 cells, got {len(cells)}")
                continue
            row_count += 1
            layer = cells[3]
            review_frequency = cells[4]
            boundary = cells[5]
            if layer not in SOURCE_INVENTORY_LAYERS:
                bad_inventory_rows.append(f"{section}: invalid layer {layer!r}")
            if not review_frequency or "待填" in review_frequency:
                bad_inventory_rows.append(f"{section}: missing review frequency for {cells[0]!r}")
            if not boundary or "待填" in boundary:
                bad_inventory_rows.append(f"{section}: missing boundary for {cells[0]!r}")
    if row_count < 15:
        bad_inventory_rows.append(f"expected at least 15 governed source rows, got {row_count}")

    frontier_rows = extract_markdown_table_after(frontier, "## DeepSeek 技术声明复核表")
    bad_frontier_rows = []
    frontier_claim_count = 0
    for cells in frontier_rows[1:]:
        if len(cells) != 4:
            bad_frontier_rows.append(f"expected 4 cells, got {len(cells)}")
            continue
        frontier_claim_count += 1
        level = cells[2]
        conclusion = cells[3]
        if level not in FRONTIER_SOURCE_LEVELS:
            bad_frontier_rows.append(f"invalid frontier source level {level!r} for {cells[0]!r}")
        if "待加强" in cells[2] or "待加强" in conclusion:
            bad_frontier_rows.append(f"frontier row still uses 待加强 instead of A/B/C/D plus action for {cells[0]!r}")
        if level == "D" and not all(term in conclusion for term in ("monitor", "不作为当前课程事实")):
            bad_frontier_rows.append(f"D-level frontier row lacks monitor-only and non-fact boundary for {cells[0]!r}")
    if frontier_claim_count < 9:
        bad_frontier_rows.append(f"expected at least 9 frontier claim rows, got {frontier_claim_count}")

    if ".venv/bin/python verify_course.py" not in frontier:
        bad_frontier_rows.append("frontier audit must use .venv/bin/python verify_course.py")
    if ".venv/bin/python verify_course.py --capstone --training" not in source_map:
        bad_inventory_rows.append("chapter source map must include .venv publish gate command")

    if bad_inventory_rows or bad_frontier_rows:
        details = "; ".join((bad_inventory_rows + bad_frontier_rows)[:10])
        fail(f"source governance docs are incomplete: {details}")
    ok(
        "source governance docs have valid layers, review frequencies, and frontier claim levels "
        f"({row_count} source rows, {frontier_claim_count} frontier claims)"
    )


def check_frontier_source_evidence_cards() -> None:
    text = read("docs/frontier-source-evidence-cards.md")
    issues = []

    for marker in [
        "Frontier Source Evidence Cards",
        "复核日期：2026-06-05",
        "Evidence Card Schema",
        "Current Evidence Cards",
        "Upgrade and Downgrade Rules",
        "Release Checklist",
        "frontier-source-audit.md",
        "external-source-inventory.md",
        "external-source-verification.md",
        "chapter-claim-audit-ledger.md",
        "claim-audit-worksheet.md",
        "model-benchmark-card-guide.md",
        "course-operations-log.md",
    ]:
        if marker not in text:
            issues.append(f"frontier source evidence cards missing marker: {marker}")

    schema_rows = extract_markdown_table_after(text, "## Evidence Card Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    for field in [
        "card_id",
        "claim",
        "source_url",
        "source_kind",
        "access_date",
        "evidence_summary",
        "boundary",
        "course_action",
        "student_use",
    ]:
        if field not in schema_fields:
            issues.append(f"frontier evidence schema missing field: {field}")

    card_rows = extract_markdown_table_after(text, "## Current Evidence Cards")
    card_ids = {cells[0] for cells in card_rows[1:] if cells}
    for card_id in [
        "FSEC-DSA-2026-0605",
        "FSEC-V4-ARCH-2026-0605",
        "FSEC-V4-EFF-2026-0605",
        "FSEC-V4-REASON-2026-0605",
        "FSEC-V4-MTP-MONITOR-2026-0605",
        "FSEC-ENGRAM-MONITOR-2026-0605",
        "FSEC-R1-UNIFY-MONITOR-2026-0605",
        "FSEC-V2V3-REPORTS-2026-0605",
    ]:
        if card_id not in card_ids:
            issues.append(f"frontier evidence cards missing card: {card_id}")
    actions = set()
    source_kinds = set()
    monitor_count = 0
    for cells in card_rows[1:]:
        if len(cells) != 9:
            issues.append(f"frontier evidence card row expected 9 cells, got {len(cells)}: {cells[:2]}")
            continue
        actions.add(cells[7])
        source_kinds.add(cells[3])
        if cells[4] != "2026-06-05":
            issues.append(f"{cells[0]} access_date must be 2026-06-05, got {cells[4]}")
        if not cells[5] or not cells[6]:
            issues.append(f"{cells[0]} missing evidence summary or boundary")
        if cells[7] in {"monitor-only", "downgrade"}:
            monitor_count += 1
            if "not for scoring" not in cells[8]:
                issues.append(f"{cells[0]} monitor/downgrade card must be not for scoring")
        if cells[3] == "unsupported" and "no supporting primary source" not in cells[2]:
            issues.append(f"{cells[0]} unsupported card must state no supporting primary source")
    for action in ["qualify", "monitor-only", "downgrade"]:
        if action not in actions:
            issues.append(f"frontier evidence cards missing action: {action}")
    for source_kind in ["API news", "model card", "technical report", "unsupported"]:
        if source_kind not in source_kinds:
            issues.append(f"frontier evidence cards missing source kind: {source_kind}")
    if monitor_count < 3:
        issues.append(f"expected at least 3 monitor/downgrade cards, got {monitor_count}")

    rules_rows = extract_markdown_table_after(text, "## Upgrade and Downgrade Rules")
    if len(rules_rows) < 6:
        issues.append("frontier source evidence cards need at least 5 upgrade/downgrade rules")
    for rule_marker in [
        "A primary source supports",
        "screenshots, social posts",
        "numeric benchmark",
        "official source changes",
    ]:
        if rule_marker not in text:
            issues.append(f"frontier source evidence cards missing rule marker: {rule_marker}")

    for linked_doc in [
        "README.md",
        "docs/frontier-source-audit.md",
        "docs/external-source-inventory.md",
        "docs/external-source-verification.md",
        "docs/course-operations-log.md",
    ]:
        if "frontier-source-evidence-cards.md" not in read(linked_doc):
            issues.append(f"{linked_doc} missing frontier source evidence cards link")
    if "frontier-source-evidence-cards.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing frontier source evidence cards")
    if "docs/frontier-source-evidence-cards.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing frontier source evidence cards")

    if issues:
        fail(f"frontier source evidence cards are incomplete: {'; '.join(issues[:10])}")
    ok("frontier source evidence cards cover dated source support, monitor-only downgrades, rules, release links, and manifest coverage")


def check_frontier_source_verifier_script() -> None:
    script = ROOT / "scripts/verify_frontier_sources.py"
    if not script.exists():
        fail("missing frontier source verifier: scripts/verify_frontier_sources.py")
    script_text = script.read_text(encoding="utf-8")
    compile(script_text, str(script), "exec")

    for marker in [
        "frontier_source_evidence_verification",
        "SOURCE_CHECKS",
        "deepseek_v32_exp_api_news",
        "deepseek_v4_pro_model_card",
        "deepseek_v2_arxiv",
        "deepseek_v3_arxiv",
        "FSEC-DSA-2026-0605",
        "FSEC-V4-ARCH-2026-0605",
        "FSEC-V4-MTP-MONITOR-2026-0605",
        "FSEC-ENGRAM-MONITOR-2026-0605",
        "absent_markers",
        "unexpected_absent_marker_hits",
        "--fixture-dir",
        "--json-out",
    ]:
        if marker not in script_text:
            fail(f"frontier source verifier missing marker: {marker}")

    for doc_path in [
        "docs/external-source-verification.md",
        "docs/presemester-readiness-audit.md",
        "docs/course-operations-log.md",
        "scripts/generate_course_evidence_manifest.py",
    ]:
        text = read(doc_path)
        if "scripts/verify_frontier_sources.py" not in text:
            fail(f"{doc_path} missing frontier source verifier command/link")
    if "frontier_source_evidence" not in read("scripts/generate_course_evidence_manifest.py"):
        fail("course evidence manifest missing frontier source evidence gate")

    ok("frontier source verifier script defines official source checks, absent-marker checks, fixture support, JSON output, and readiness links")


def check_cs224n_snapshot_refresh_script() -> None:
    script = ROOT / "scripts/verify_cs224n_snapshot.py"
    if not script.exists():
        fail("missing CS224N snapshot verifier: scripts/verify_cs224n_snapshot.py")
    script_text = script.read_text(encoding="utf-8")
    compile(script_text, str(script), "exec")

    required_script_markers = [
        "https://web.stanford.edu/class/cs224n/",
        "EXPECTED_MARKERS",
        "Stanford / Winter 2026",
        "Assignments (48%)",
        "Final Project (49%)",
        "Participation (3%)",
        "Hugging Face Transformers Tutorial Session",
        "Benchmarking and Evaluation",
        "Reasoning 1",
        "Reasoning 2",
        "Tokenization and Multilinguality",
        "Tinker and LoRA Without Regret",
        "Open Questions in NLP 2026",
        "cs224n_current_snapshot_verification",
    ]
    for marker in required_script_markers:
        if marker not in script_text:
            fail(f"CS224N snapshot verifier missing marker: {marker}")

    marker_strings = re.findall(r'^\s+"([^"]+)",$', script_text, re.M)
    if len(marker_strings) < 30:
        fail(f"CS224N snapshot verifier has too few expected markers: {len(marker_strings)}")

    with tempfile.TemporaryDirectory(prefix="cs224n-snapshot-fixture-") as tmp:
        fixture = Path(tmp) / "cs224n.html"
        json_out = Path(tmp) / "manifest.json"
        fixture.write_text(
            "<html><body>" + "\n".join(f"<p>{marker}</p>" for marker in marker_strings) + "</body></html>",
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(script), "--html-file", str(fixture), "--json-out", str(json_out)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            fail(f"CS224N snapshot verifier fixture run failed: {result.stderr or result.stdout}")
        if not json_out.exists():
            fail("CS224N snapshot verifier did not write JSON manifest")
        manifest = json.loads(json_out.read_text(encoding="utf-8"))

    if manifest.get("mode") != "cs224n_current_snapshot_verification":
        fail(f"unexpected CS224N snapshot verifier mode: {manifest.get('mode')}")
    if manifest.get("status") != "pass":
        fail(f"CS224N snapshot verifier fixture status is not pass: {manifest.get('missing_markers')}")
    if manifest.get("matched_marker_count") != manifest.get("expected_marker_count"):
        fail("CS224N snapshot verifier did not match all expected markers in fixture")

    docs_to_check = [
        "docs/external-source-verification.md",
        "docs/cs224n-current-benchmark-snapshot.md",
        "docs/cs224n-benchmark-crosswalk.md",
    ]
    for doc in docs_to_check:
        text = read(doc)
        if "scripts/verify_cs224n_snapshot.py" not in text:
            fail(f"{doc} missing CS224N snapshot verifier command")
    ok(f"CS224N snapshot verifier script emits pass manifest for {manifest['expected_marker_count']} expected markers")


def check_presemester_readiness_audit() -> None:
    text = read("docs/presemester-readiness-audit.md")
    issues = []

    required_commands = [
        ".venv/bin/python -m py_compile verify_course.py scripts/verify_cs224n_snapshot.py",
        ".venv/bin/python scripts/verify_cs224n_snapshot.py",
        ".venv/bin/python scripts/verify_frontier_sources.py",
        ".venv/bin/python scripts/generate_course_evidence_manifest.py --check",
        ".venv/bin/python verify_course.py",
        ".venv/bin/python run_assignment_tests.py",
        ".venv/bin/python verify_course.py --capstone --training",
    ]
    for command in required_commands:
        if command not in text:
            issues.append(f"missing readiness command: {command}")

    for marker in [
        "status=pass",
        "course_evidence_manifest",
        "verification_status: pass",
        "matched_marker_count=38",
        "missing_marker_count=0",
        "COURSE VERIFY: PASS",
        "ASSIGNMENT TESTS: PASS (11 suite(s))",
        "ACCEPTANCE: PASS",
        "pass_rate: 5/5 = 100.0%",
        "SLO: PASS",
        "tokens_per_second: 299.2739 >= 100.0000",
        "latency_ms.p95: 306.9216 <= 2000.0000",
        "ttft_ms.p95: 3.1919 <= 800.0000",
        "tpot_ms.p95: 6.5226 <= 40.0000",
        "fits_gpu: True",
        "estimated_cost_usd: 0.42",
        "final_step: 12",
        "device: cpu",
        "strips inline solutions",
        "excludes instructor-only docs",
        "reference_solution.py",
        "student_solution",
        "11 pages",
        "397 rendered KaTeX nodes",
        "376 KaTeX nodes",
        "Known Human Sign-Off Boundaries",
        "Instructor / Course Manager",
        "Head TA",
    ]:
        if marker not in text:
            issues.append(f"missing readiness evidence marker: {marker}")

    boundary_rows = extract_markdown_table_after(text, "## Known Human Sign-Off Boundaries")
    if len(boundary_rows) < 7:
        issues.append(f"expected at least 6 human sign-off rows, got {max(0, len(boundary_rows) - 1)}")

    next_actions = extract_markdown_table_after(text, "## Next Audit Actions")
    if len(next_actions) < 5:
        issues.append(f"expected at least 4 next audit actions, got {max(0, len(next_actions) - 1)}")

    for linked_doc in (
        "course-operations-log.md",
        "university-course-quality-audit.md",
        "external-source-verification.md",
        "cs224n-current-benchmark-snapshot.md",
        "cs224n-benchmark-crosswalk.md",
        "frontier-seminar-handout.md",
        "external-source-inventory.md",
    ):
        if linked_doc not in text:
            issues.append(f"readiness audit missing linked doc: {linked_doc}")

    for doc_path in ("README.md", "docs/course-operations-log.md", "docs/university-course-quality-audit.md"):
        if "presemester-readiness-audit.md" not in read(doc_path):
            issues.append(f"{doc_path} missing presemester readiness audit link")

    if issues:
        fail(f"pre-semester readiness audit is incomplete: {'; '.join(issues[:10])}")
    ok("pre-semester readiness audit captures command evidence, release safety, and human sign-off boundaries")


def check_course_evidence_manifest_script() -> None:
    script = ROOT / "scripts/generate_course_evidence_manifest.py"
    if not script.exists():
        fail("missing course evidence manifest generator: scripts/generate_course_evidence_manifest.py")
    script_text = script.read_text(encoding="utf-8")
    compile(script_text, str(script), "exec")

    required_script_markers = [
        "course_evidence_manifest",
        "verification_status",
        "REQUIRED_EVIDENCE_FILES",
        "MARKER_CHECKS",
        "verification_gates",
        "human_signoff_boundaries",
        "release_safety_invariants",
        "scripts/verify_cs224n_snapshot.py",
        "scripts/verify_frontier_sources.py",
        "frontier_source_evidence",
        "expected_marker_count",
        "38",
    ]
    for marker in required_script_markers:
        if marker not in script_text:
            fail(f"course evidence manifest generator missing marker: {marker}")

    with tempfile.TemporaryDirectory(prefix="course-evidence-manifest-") as tmp:
        json_out = Path(tmp) / "course-evidence.json"
        result = subprocess.run(
            [sys.executable, str(script), "--check", "--json-out", str(json_out)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            fail(f"course evidence manifest check failed: {result.stderr or result.stdout}")
        if not json_out.exists():
            fail("course evidence manifest generator did not write JSON manifest")
        manifest = json.loads(json_out.read_text(encoding="utf-8"))

    if manifest.get("mode") != "course_evidence_manifest":
        fail(f"unexpected course evidence manifest mode: {manifest.get('mode')}")
    if manifest.get("verification_status") != "pass":
        fail(
            "course evidence manifest status is not pass: "
            f"files={manifest.get('missing_required_files')} markers={manifest.get('missing_required_markers')}"
        )
    if manifest.get("missing_required_files"):
        fail(f"course evidence manifest missing files: {manifest['missing_required_files']}")
    if manifest.get("missing_required_markers"):
        fail(f"course evidence manifest missing markers: {manifest['missing_required_markers']}")

    benchmark = manifest.get("course_benchmark", {})
    if benchmark.get("url") != "https://web.stanford.edu/class/cs224n/":
        fail(f"course evidence manifest has unexpected benchmark URL: {benchmark.get('url')}")
    if benchmark.get("expected_marker_count") != 38:
        fail(f"course evidence manifest has unexpected CS224N marker count: {benchmark.get('expected_marker_count')}")

    gate_commands = {gate.get("command") for gate in manifest.get("verification_gates", [])}
    for command in [
        ".venv/bin/python verify_course.py",
        ".venv/bin/python run_assignment_tests.py",
        ".venv/bin/python verify_course.py --capstone --training",
        ".venv/bin/python scripts/verify_frontier_sources.py --json-out frontier-sources-2026-06-05.json",
    ]:
        if command not in gate_commands:
            fail(f"course evidence manifest missing verification gate: {command}")

    for boundary in [
        "LMS / Gradescope configuration",
        "School-specific policy",
        "Real staff roster",
        "Hidden tests",
        "Live lecture quality",
        "Project report quality",
    ]:
        if boundary not in manifest.get("human_signoff_boundaries", []):
            fail(f"course evidence manifest missing human sign-off boundary: {boundary}")

    for doc in ["README.md", "docs/presemester-readiness-audit.md", "docs/course-operations-log.md"]:
        if "scripts/generate_course_evidence_manifest.py" not in read(doc):
            fail(f"{doc} missing course evidence manifest generator link")

    ok("course evidence manifest generator emits pass JSON with verification gates and sign-off boundaries")


def check_chapter_claim_audit_ledger() -> None:
    ledger = read("docs/chapter-claim-audit-ledger.md")
    issues = []

    for heading in [
        "Ledger Schema",
        "Audited Claims",
        "High-Risk Claim Gates",
        "Maintenance Workflow",
        "发布前 Checklist",
    ]:
        markdown_section(ledger, heading)

    rows = extract_markdown_table_after(ledger, "## Audited Claims")
    if len(rows) < 24:
        issues.append(f"expected header plus at least 23 audited claim rows, got {len(rows)}")

    valid_types = {"stable theory", "implementation", "frontier model card", "benchmark", "course inference"}
    valid_levels = {"A-stable", "A-volatile", "B-implementation", "C-background"}
    valid_actions = {"keep", "qualify", "downgrade", "remove", "replace"}
    per_chapter: dict[str, int] = {f"CH{index:02d}": 0 for index in range(1, 12)}
    seen_ids: set[str] = set()
    claim_types: set[str] = set()
    actions: set[str] = set()

    for cells in rows[1:]:
        if len(cells) != 8:
            issues.append(f"audited claim row expected 8 cells, got {len(cells)}: {cells[:2]}")
            continue
        claim_id, location, claim_text, claim_type, source_level, student_use, boundary, action = cells
        if not re.fullmatch(r"CH(?:0[1-9]|10|11)-C\d{2}", claim_id):
            issues.append(f"invalid claim id: {claim_id}")
            continue
        if claim_id in seen_ids:
            issues.append(f"duplicate claim id: {claim_id}")
        seen_ids.add(claim_id)
        chapter = claim_id.split("-", 1)[0]
        per_chapter[chapter] += 1
        claim_types.add(claim_type)
        actions.add(action)
        if claim_type not in valid_types:
            issues.append(f"{claim_id}: invalid claim type {claim_type!r}")
        if source_level not in valid_levels:
            issues.append(f"{claim_id}: invalid source level {source_level!r}")
        if action not in valid_actions:
            issues.append(f"{claim_id}: invalid action {action!r}")
        if not location or not claim_text or not student_use or not boundary:
            issues.append(f"{claim_id}: missing location, claim text, student use, or boundary")
        if action == "downgrade" and any(use in student_use for use in ("assignment", "quiz", "exam")):
            issues.append(f"{claim_id}: downgraded claim must not enter assignment/quiz/exam facts")

    for chapter, count in sorted(per_chapter.items()):
        if count < 2:
            issues.append(f"{chapter}: expected at least 2 audited claims, got {count}")

    for required_type in valid_types:
        if required_type not in claim_types:
            issues.append(f"claim ledger missing claim type: {required_type}")
    for required_action in ("keep", "qualify", "downgrade"):
        if required_action not in actions:
            issues.append(f"claim ledger missing action: {required_action}")

    gates = extract_markdown_table_after(ledger, "## High-Risk Claim Gates")
    gate_names = {cells[0] for cells in gates[1:] if cells}
    for gate in ("optimality_gate", "formula_gate", "systems_gate", "frontier_gate", "evaluation_gate"):
        if gate not in gate_names:
            issues.append(f"claim ledger missing high-risk gate: {gate}")

    for doc_path in [
        "docs/chapter-source-map.md",
        "docs/claim-audit-worksheet.md",
        "docs/external-source-inventory.md",
        "README.md",
    ]:
        if "chapter-claim-audit-ledger.md" not in read(doc_path):
            issues.append(f"{doc_path} missing chapter claim audit ledger link")

    if issues:
        fail(f"chapter claim audit ledger is incomplete: {'; '.join(issues[:10])}")
    ok("chapter claim audit ledger covers all modules, source levels, actions, boundaries, and high-risk gates")


def check_mathematical_derivation_audit() -> None:
    text = read("docs/mathematical-derivation-audit.md")
    issues = []

    for marker in [
        "Mathematical Derivation Audit",
        "复核日期：2026-06-05",
        "Audit Schema",
        "Audited Derivations",
        "Executable Gate Coverage",
        "Instructor Review Protocol",
        "发布前 Checklist",
        "Assumptions",
        "Shape / units",
        "Executable evidence",
        "Boundary",
        "Board Derivation and Instructor Notes Pack",
        "Chapter Claim Audit Ledger",
        "Course Outcome Map",
    ]:
        if marker not in text:
            issues.append(f"missing derivation audit marker: {marker}")

    rows = extract_markdown_table_after(text, "## Audited Derivations")
    expected_ids = {f"DER-{index:02d}" for index in range(1, 15)}
    seen_ids = set()
    chapter_refs = set()

    for cells in rows[1:]:
        if len(cells) != 7:
            issues.append(f"audited derivation row expected 7 cells, got {len(cells)}: {cells[:2]}")
            continue
        derivation_id = cells[0]
        seen_ids.add(derivation_id)
        chapter_refs.update(re.findall(r"Ch(?:0[1-9]|10|11)", cells[1]))
        for field_name, cell_index in {
            "assumptions": 3,
            "shape": 4,
            "evidence": 5,
            "boundary": 6,
        }.items():
            value = cells[cell_index]
            if not value or value in {"-", "N/A"}:
                issues.append(f"{derivation_id} missing {field_name}")
        if not any(term in cells[5] for term in ("tests", "capstone", "verifier")):
            issues.append(f"{derivation_id} executable evidence must reference tests, capstone, or verifier")
        if any(term in cells[6] for term in ("不适用", "无", "None")):
            issues.append(f"{derivation_id} boundary must not be empty or waived")

    missing_ids = sorted(expected_ids - seen_ids)
    extra_ids = sorted(seen_ids - expected_ids)
    if missing_ids:
        issues.append(f"missing derivation IDs: {missing_ids}")
    if extra_ids:
        issues.append(f"unexpected derivation IDs: {extra_ids}")

    for chapter in [f"Ch{index:02d}" for index in range(1, 11)] + ["Ch11"]:
        if chapter not in chapter_refs:
            issues.append(f"derivation audit missing chapter coverage: {chapter}")

    gate_rows = extract_markdown_table_after(text, "## Executable Gate Coverage")
    gate_text = "\n".join(" | ".join(row) for row in gate_rows)
    for gate_marker in [
        ".venv/bin/python run_assignment_tests.py",
        ".venv/bin/python verify_course.py",
        ".venv/bin/python verify_course.py --capstone --training",
        "check_text_and_formula_format()",
        "check_key_derivation_consistency()",
        "check_chapter_claim_audit_ledger()",
        "check_source_governance_docs()",
    ]:
        if gate_marker not in gate_text:
            issues.append(f"derivation audit missing executable gate: {gate_marker}")

    linked_docs = [
        "board-derivation-pack.md",
        "chapter-claim-audit-ledger.md",
        "written-problem-set.md",
        "course-outcome-map.md",
        "external-source-verification.md",
        "frontier-source-audit.md",
    ]
    for linked_doc in linked_docs:
        if linked_doc not in text:
            issues.append(f"derivation audit missing linked doc: {linked_doc}")

    for doc_path in [
        "README.md",
        "docs/board-derivation-pack.md",
        "docs/chapter-claim-audit-ledger.md",
        "docs/course-outcome-map.md",
    ]:
        if "mathematical-derivation-audit.md" not in read(doc_path):
            issues.append(f"{doc_path} missing mathematical derivation audit link")

    if issues:
        fail(f"mathematical derivation audit is incomplete: {'; '.join(issues[:10])}")
    ok("mathematical derivation audit covers 14 derivations with assumptions, shapes, evidence, and boundaries")


def check_paper_recap_calibration_pack() -> None:
    text = read("docs/paper-recap-calibration-pack.md")
    issues = []

    for marker in [
        "Paper Recap Calibration Pack",
        "复核日期：2026-06-05",
        "Recap Rubric",
        "Anchor Samples",
        "Required Evidence Fields",
        "TA Calibration Procedure",
        "Student Submission Template",
        "Release Checklist",
        "source_record",
        "core_claim",
        "technical_detail",
        "course_link",
        "boundary",
        "discussion_question",
        "reading-list.md",
        "reading-discussion-question-bank.md",
        "participation-feedback-guide.md",
        "chapter-claim-audit-ledger.md",
        "mathematical-derivation-audit.md",
        "external-source-verification.md",
    ]:
        if marker not in text:
            issues.append(f"missing paper recap calibration marker: {marker}")

    rubric_rows = extract_markdown_table_after(text, "## Recap Rubric")
    rubric_dimensions = {cells[0] for cells in rubric_rows[1:] if cells}
    for dimension in [
        "Core claim",
        "Technical detail",
        "Course connection",
        "Source audit",
        "Critical question",
        "Citation hygiene",
    ]:
        if dimension not in rubric_dimensions:
            issues.append(f"paper recap rubric missing dimension: {dimension}")

    anchor_rows = extract_markdown_table_after(text, "## Anchor Samples")
    if len(anchor_rows) < 9:
        issues.append(f"expected 8 paper recap anchor samples, got {max(0, len(anchor_rows) - 1)}")
    levels = set()
    anchor_ids = set()
    for cells in anchor_rows[1:]:
        if len(cells) != 6:
            issues.append(f"paper recap anchor row expected 6 cells, got {len(cells)}: {cells[:2]}")
            continue
        anchor_id, level, topic_source, evidence, score, feedback = cells
        anchor_ids.add(anchor_id)
        levels.add(level)
        if not topic_source or not evidence or not feedback:
            issues.append(f"{anchor_id}: missing topic/source, evidence, or feedback")
        try:
            numeric_score = int(score)
        except ValueError:
            issues.append(f"{anchor_id}: score is not an integer: {score}")
            continue
        if not (0 <= numeric_score <= 100):
            issues.append(f"{anchor_id}: score out of range: {numeric_score}")
    for expected_id in ["PR-A1", "PR-A2", "PR-B1", "PR-B2", "PR-C1", "PR-C2", "PR-NP1", "PR-NP2"]:
        if expected_id not in anchor_ids:
            issues.append(f"missing paper recap anchor sample: {expected_id}")
    for level in ["A", "B", "C", "Not passing"]:
        if level not in levels:
            issues.append(f"paper recap anchors missing level: {level}")

    field_rows = extract_markdown_table_after(text, "## Required Evidence Fields")
    field_names = {cells[0].strip("`") for cells in field_rows[1:] if cells}
    for field in [
        "source_record",
        "core_claim",
        "technical_detail",
        "course_link",
        "boundary",
        "discussion_question",
    ]:
        if field not in field_names:
            issues.append(f"paper recap required fields missing: {field}")

    for procedure_marker in [
        "分差超过 8 分",
        "每周抽取 5-8 份阅读复盘",
        "Course Operations and Improvement Log",
        "External Source Inventory",
        "External Source Verification Guide",
        "脱敏",
    ]:
        if procedure_marker not in text:
            issues.append(f"paper recap TA calibration missing procedure marker: {procedure_marker}")

    for doc_path in [
        "README.md",
        "docs/reading-list.md",
        "docs/participation-feedback-guide.md",
        "docs/course-outcome-map.md",
        "docs/syllabus.md",
    ]:
        if "paper-recap-calibration-pack.md" not in read(doc_path):
            issues.append(f"{doc_path} missing paper recap calibration pack link")

    if issues:
        fail(f"paper recap calibration pack is incomplete: {'; '.join(issues[:10])}")
    ok("paper recap calibration pack covers rubric dimensions, 8 anchor samples, fields, and TA calibration")


def check_reading_discussion_question_bank() -> None:
    text = read("docs/reading-discussion-question-bank.md")
    issues = []

    for marker in [
        "Reading Discussion Question Bank",
        "复核日期：2026-06-05",
        "Question Schema",
        "Core Question Bank",
        "Discussion Formats",
        "Assessment Sampling Rules",
        "Maintenance Workflow",
        "Release Checklist",
        "reading-list.md",
        "paper-recap-calibration-pack.md",
        "paper-to-code-traceability-matrix.md",
        "topic-dependency-map.md",
        "assessment-blueprint-coverage-matrix.md",
        "participation-feedback-guide.md",
        "recitation-worksheet-pack.md",
        "chapter-source-map.md",
        "external-source-verification.md",
        ".venv/bin/python verify_course.py",
        "student site release",
    ]:
        if marker not in text:
            issues.append(f"missing reading discussion question bank marker: {marker}")

    schema_rows = extract_markdown_table_after(text, "## Question Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    for field in ["question_id", "week", "reading_anchor", "question_type", "prompt", "expected_evidence", "course_link"]:
        if field not in schema_fields:
            issues.append(f"reading discussion schema missing field: {field}")

    question_rows = extract_markdown_table_after(text, "## Core Question Bank")
    if len(question_rows) < 23:
        issues.append(f"expected at least 22 reading discussion questions plus header, got {len(question_rows)}")
    question_ids = set()
    weeks = set()
    question_types = set()
    for cells in question_rows[1:]:
        if len(cells) != 7:
            issues.append(f"reading discussion question row expected 7 cells, got {len(cells)}: {cells[:2]}")
            continue
        question_id, week, _anchor, question_type, prompt, expected_evidence, course_link = cells
        question_ids.add(question_id)
        weeks.add(week)
        question_types.add(question_type)
        if not question_id.startswith("RDQ-W"):
            issues.append(f"reading discussion question id must start with RDQ-W: {question_id}")
        if not prompt or not expected_evidence or not course_link:
            issues.append(f"{question_id} missing prompt, expected evidence, or course link")

    for expected_id in [
        "RDQ-W0-CLAIM",
        "RDQ-W1-MECH",
        "RDQ-W2-CODE",
        "RDQ-W3-LIMIT",
        "RDQ-W4-CODE",
        "RDQ-W5-MECH",
        "RDQ-W6-LIMIT",
        "RDQ-W7-SOURCE",
        "RDQ-W8-ETHICS",
        "RDQ-W9-RAG",
        "RDQ-W10-AUDIT",
    ]:
        if expected_id not in question_ids:
            issues.append(f"reading discussion question bank missing question: {expected_id}")

    for week in [f"Week {index}" for index in range(0, 11)]:
        if week not in weeks:
            issues.append(f"reading discussion question bank missing week coverage: {week}")

    for question_type in ["claim", "mechanism", "limitation", "paper_to_code", "metric", "project", "ethics"]:
        if question_type not in question_types:
            issues.append(f"reading discussion question bank missing question_type: {question_type}")

    format_rows = extract_markdown_table_after(text, "## Discussion Formats")
    format_ids = {cells[0] for cells in format_rows[1:] if cells}
    for format_id in ["RDQ-F-PAIR", "RDQ-F-BOARD", "RDQ-F-RECITATION", "RDQ-F-RECAP", "RDQ-F-PROJECT"]:
        if format_id not in format_ids:
            issues.append(f"reading discussion question bank missing discussion format: {format_id}")
    for cells in format_rows[1:]:
        if len(cells) != 4:
            issues.append(f"reading discussion format row expected 4 cells, got {len(cells)}: {cells[:2]}")

    rule_rows = extract_markdown_table_after(text, "## Assessment Sampling Rules")
    rule_ids = {cells[0] for cells in rule_rows[1:] if cells}
    for rule_id in ["RDQ-R1", "RDQ-R2", "RDQ-R3", "RDQ-R4", "RDQ-R5"]:
        if rule_id not in rule_ids:
            issues.append(f"reading discussion question bank missing sampling rule: {rule_id}")
    for cells in rule_rows[1:]:
        if len(cells) != 3:
            issues.append(f"reading discussion sampling rule row expected 3 cells, got {len(cells)}: {cells[:2]}")

    for workflow_marker in [
        "reading-list.md changes",
        "paper recap anchor",
        "chapter source boundary changes",
        "active quiz or exam item",
        ".venv/bin/python verify_course.py",
    ]:
        if workflow_marker not in text:
            issues.append(f"reading discussion maintenance workflow missing marker: {workflow_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/reading-list.md",
        "docs/paper-recap-calibration-pack.md",
        "docs/paper-to-code-traceability-matrix.md",
        "docs/participation-feedback-guide.md",
        "docs/recitation-worksheet-pack.md",
        "docs/assessment-blueprint-coverage-matrix.md",
        "docs/chapter-source-map.md",
    ]
    for doc_path in linked_docs:
        if "reading-discussion-question-bank.md" not in read(doc_path):
            issues.append(f"{doc_path} missing reading discussion question bank link")

    if "reading-discussion-question-bank.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing reading discussion question bank")
    if "docs/reading-discussion-question-bank.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing reading discussion question bank")

    if issues:
        fail(f"reading discussion question bank is incomplete: {'; '.join(issues[:10])}")
    ok("reading discussion question bank covers Week 0-10, question types, evidence fields, discussion formats, sampling rules, and release links")


def check_paper_to_code_traceability_matrix() -> None:
    text = read("docs/paper-to-code-traceability-matrix.md")
    derivation_audit = read("docs/mathematical-derivation-audit.md")
    issues = []

    for marker in [
        "Paper-to-Code Traceability Matrix",
        "复核日期：2026-06-05",
        "Traceability Matrix",
        "Coverage Requirements",
        "Instructor Review Protocol",
        "Release Checklist",
        "reading-list.md",
        "chapter-source-map.md",
        "external-source-inventory.md",
        "mathematical-derivation-audit.md",
        "assignment-handout-pack.md",
        "paper-recap-calibration-pack.md",
    ]:
        if marker not in text:
            issues.append(f"missing paper-to-code marker: {marker}")

    rows = extract_markdown_table_after(text, "## Traceability Matrix")
    if len(rows) < 15:
        issues.append(f"expected 14 paper-to-code rows, got {max(0, len(rows) - 1)}")

    expected_ids = {f"P2C-{index:02d}" for index in range(1, 15)}
    seen_ids = set()
    source_tiers = set()
    row_text = []
    assignment_test_paths = set()
    referenced_derivations = set()
    for cells in rows[1:]:
        if len(cells) != 9:
            issues.append(f"paper-to-code row expected 9 cells, got {len(cells)}: {cells[:2]}")
            continue
        row_id, source, tier, anchor, week, derivation, evidence, deliverable, boundary = cells
        seen_ids.add(row_id)
        row_text.append(" ".join(cells))
        assignment_test_paths.update(re.findall(r"`(assignments/[^`]+/tests\.py)`", evidence))
        referenced_derivations.update(re.findall(r"\bDER-\d{2}\b", derivation))
        for tier_part in [part.strip() for part in tier.split("/")]:
            source_tiers.add(tier_part)
        for field_name, value in [
            ("source", source),
            ("source tier", tier),
            ("course anchor", anchor),
            ("reading week", week),
            ("derivation evidence", derivation),
            ("code evidence", evidence),
            ("student deliverable", deliverable),
            ("boundary", boundary),
        ]:
            if not value:
                issues.append(f"{row_id}: missing {field_name}")
        if "not " not in boundary.lower() and "不能" not in boundary and "不" not in boundary:
            issues.append(f"{row_id}: boundary does not state a limitation")

    for expected_id in sorted(expected_ids):
        if expected_id not in seen_ids:
            issues.append(f"missing paper-to-code row: {expected_id}")

    allowed_tiers = {"A-stable", "A-volatile", "B-implementation", "C-background"}
    unknown_tiers = source_tiers - allowed_tiers
    if unknown_tiers:
        issues.append(f"paper-to-code unknown source tiers: {sorted(unknown_tiers)}")
    for required_tier in ["A-stable", "A-volatile", "B-implementation"]:
        if required_tier not in source_tiers:
            issues.append(f"paper-to-code missing source tier: {required_tier}")

    combined_text = "\n".join(row_text)
    audited_derivations = set(re.findall(r"\|\s*(DER-\d{2})\s*\|", derivation_audit))
    for der_id in sorted(referenced_derivations):
        if der_id not in audited_derivations:
            issues.append(f"paper-to-code references unknown derivation id: {der_id}")
    for der_id in [f"DER-{index:02d}" for index in range(1, 15)]:
        if der_id not in combined_text and der_id not in text:
            issues.append(f"paper-to-code missing derivation coverage: {der_id}")

    for assignment_test_path in sorted(assignment_test_paths):
        if not (ROOT / assignment_test_path).exists():
            issues.append(f"paper-to-code assignment test path does not exist: {assignment_test_path}")

    for assignment_dir in [
        "assignments/ch01_bpe",
        "assignments/ch02_embeddings",
        "assignments/ch03_attention",
        "assignments/ch04_multihead",
        "assignments/ch05_block",
        "assignments/ch06_gpt",
        "assignments/ch07_training",
        "assignments/ch08_generation",
        "assignments/ch09_alignment",
        "assignments/ch10_inference",
        "assignments/ch11_classic_nlp",
    ]:
        if assignment_dir not in combined_text:
            issues.append(f"paper-to-code missing assignment coverage: {assignment_dir}")

    for week in [f"Week {index}" for index in range(1, 10)]:
        if week not in combined_text:
            issues.append(f"paper-to-code missing reading week coverage: {week}")

    for source_marker in [
        "Sennrich",
        "Mikolov",
        "GloVe",
        "Vaswani",
        "RoPE",
        "GQA",
        "DeepSeek-V2",
        "LayerNorm",
        "GPT-2",
        "Switch Transformer",
        "AdamW",
        "Chinchilla",
        "ZeRO",
        "Holtzman",
        "speculative decoding",
        "LoRA",
        "DPO",
        "DeepSeek-R1",
        "PagedAttention",
        "FlashAttention",
        "RAG",
        "QLoRA",
        "BERT",
        "BLEU",
    ]:
        if source_marker not in text:
            issues.append(f"paper-to-code missing source marker: {source_marker}")

    for assessment_marker in [
        "written",
        "Reading recap",
        "capstone",
        "Project report",
        "Paper-to-code drill",
    ]:
        if assessment_marker not in text:
            issues.append(f"paper-to-code missing assessment marker: {assessment_marker}")

    for doc_path in [
        "README.md",
        "docs/reading-list.md",
        "docs/chapter-source-map.md",
        "docs/external-source-inventory.md",
        "docs/course-outcome-map.md",
        "docs/syllabus.md",
    ]:
        if "paper-to-code-traceability-matrix.md" not in read(doc_path):
            issues.append(f"{doc_path} missing paper-to-code traceability matrix link")

    if issues:
        fail(f"paper-to-code traceability matrix is incomplete: {'; '.join(issues[:10])}")
    ok("paper-to-code traceability matrix covers 14 sources, DERs, assignments, reading weeks, and boundaries")


def check_text_and_formula_format() -> None:
    control_hits = []
    malformed_expr_hits = []
    empty_expr_hits = []
    inaccessible_expr_hits = []
    formula_structure_hits = []
    html_markdown_link_hits = []
    visible_tex_hits = []
    expr_count = 0

    for path in text_format_files():
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for lineno, line in enumerate(text.splitlines(keepends=True), start=1):
            for char in line:
                if ord(char) < 32 and char not in ALLOWED_CONTROL_CHARS:
                    control_hits.append((rel, lineno, f"U+{ord(char):04X}"))
                    break

        if path.suffix == ".html":
            for match in HTML_MARKDOWN_DOC_LINK_RE.finditer(text):
                lineno = text.count("\n", 0, match.start()) + 1
                html_markdown_link_hits.append((rel, lineno, match.group(0)))

            for match in MALFORMED_DATA_EXPR_RE.finditer(text):
                lineno = text.count("\n", 0, match.start()) + 1
                malformed_expr_hits.append((rel, lineno))

            parser = KatexExpressionParser()
            parser.feed(text)
            for lineno, tag, expr, aria_label, role in parser.expressions:
                expr_count += 1
                if not expr.strip():
                    empty_expr_hits.append((rel, tag))
                if not aria_label.strip():
                    inaccessible_expr_hits.append((rel, lineno, "missing aria-label", expr[:120]))
                elif aria_label != expr:
                    inaccessible_expr_hits.append((rel, lineno, "aria-label differs from data-expr", expr[:120]))
                if role != "img":
                    inaccessible_expr_hits.append((rel, lineno, "missing role=\"img\"", expr[:120]))
                for reason in validate_formula_structure(expr):
                    formula_structure_hits.append((rel, lineno, reason, expr[:120]))

            if path.parent.name == "chapters":
                visible_parser = VisibleTextTexParser()
                visible_parser.feed(text)
                for lineno, snippet in visible_parser.hits:
                    visible_tex_hits.append((rel, lineno, snippet))

    if control_hits:
        details = "; ".join(f"{path}:{lineno} {code}" for path, lineno, code in control_hits[:10])
        fail(f"unexpected control characters: {details}")
    if malformed_expr_hits:
        details = "; ".join(f"{path}:{lineno}" for path, lineno in malformed_expr_hits[:10])
        fail(f"malformed data-expr attributes: {details}")
    if empty_expr_hits:
        details = "; ".join(f"{path} <{tag} data-expr>" for path, tag in empty_expr_hits[:10])
        fail(f"empty data-expr attributes: {details}")
    if inaccessible_expr_hits:
        details = "; ".join(
            f"{path}:{lineno} {reason} in {expr!r}"
            for path, lineno, reason, expr in inaccessible_expr_hits[:10]
        )
        fail(f"inaccessible formula attributes: {details}")
    if formula_structure_hits:
        details = "; ".join(
            f"{path}:{lineno} {reason} in {expr!r}"
            for path, lineno, reason, expr in formula_structure_hits[:10]
        )
        fail(f"malformed formula structures: {details}")
    if html_markdown_link_hits:
        details = "; ".join(
            f"{path}:{lineno} {target}" for path, lineno, target in html_markdown_link_hits[:10]
        )
        fail(f"markdown link syntax in html chapters: {details}")
    if visible_tex_hits:
        details = "; ".join(
            f"{path}:{lineno} {snippet}" for path, lineno, snippet in visible_tex_hits[:10]
        )
        fail(f"visible raw TeX commands in chapter text: {details}")

    ok(
        "text/control characters, KaTeX data-expr/aria-label attributes, and visible raw TeX checks "
        f"are valid ({expr_count} formula attributes)"
    )


def check_release_placeholders() -> None:
    allowed_contexts = (
        "starter",
        "待实现 API",
        "学生需要实现",
        "编辑 student_solution.py",
    )
    hits = []
    files = [ROOT / "README.md"]
    files.extend(sorted((ROOT / "docs").glob("*.md")))
    files.extend(sorted((ROOT / "assignments").glob("*/README.md")))
    for path in files:
        if not path.exists():
            continue
        rel = path.relative_to(ROOT)
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not UNRESOLVED_RELEASE_PLACEHOLDER_RE.search(line):
                continue
            if any(context in line for context in allowed_contexts):
                continue
            hits.append((rel, lineno, line.strip()[:120]))
    if hits:
        details = "; ".join(f"{path}:{lineno} {line}" for path, lineno, line in hits[:10])
        fail(f"unresolved release placeholders in course docs: {details}")
    ok("course release docs have no unresolved placeholder markers")


def check_command_conventions() -> None:
    files = [ROOT / "README.md"]
    files.extend(sorted((ROOT / "docs").glob("*.md")))
    files.extend(sorted((ROOT / "assignments").glob("*/README.md")))
    files.extend(sorted((ROOT / "assignments").glob("*/starter.py")))
    files.extend(sorted((ROOT / "assignments").glob("*/tests.py")))
    bad_commands = []
    for path in files:
        if not path.exists():
            continue
        rel = path.relative_to(ROOT)
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if BARE_COURSE_COMMAND_RE.search(line):
                bad_commands.append((rel, lineno, line.strip()[:120]))

    missing_assignment_commands = []
    for assignment in EXPECTED_ASSIGNMENTS:
        readme = ROOT / "assignments" / assignment / "README.md"
        if not readme.exists():
            continue
        text = readme.read_text(encoding="utf-8")
        expected = f".venv/bin/python assignments/{assignment}/tests.py"
        if expected not in text:
            missing_assignment_commands.append(f"{assignment}/README.md missing {expected}")

    if bad_commands or missing_assignment_commands:
        details = "; ".join(
            [f"{path}:{lineno} {line}" for path, lineno, line in bad_commands[:10]]
            + missing_assignment_commands[:10]
        )
        fail(f"course command conventions are inconsistent: {details}")
    ok("course command examples consistently use .venv/bin/python")


def check_key_derivation_consistency() -> None:
    ch02 = read("chapters/ch02.html")
    required = [
        'data-expr="R_{\\Theta,m}^\\top R_{\\Theta,n} = R_{\\Theta, n-m}"',
        '&= \\mathbf{q}_m^\\top R_{\\Theta, n-m} \\mathbf{k}_n',
    ]
    for needle in required:
        if needle not in ch02:
            fail(f"Ch02 RoPE derivation missing expected relative-position identity: {needle}")
    if '&= \\mathbf{q}_m^\\top R_{\\Theta, m-n} \\mathbf{k}_n' in ch02:
        fail("Ch02 RoPE derivation has inconsistent R_{Theta,m-n} sign in final line")
    ok("key RoPE derivation sign convention is consistent")


def check_chapter_code_contracts() -> None:
    ch02 = read("chapters/ch02.html")
    ch04 = read("chapters/ch04.html")
    required = [
        (ch02, "if pos_ids is None:", "Ch02 RoPE snippet must handle default sequential positions"),
        (ch02, "self.cos[:, :, pos_ids, :d_head//2]", "Ch02 RoPE snippet must use pos_ids branch"),
        (ch02, "self.sin[:, :, pos_ids, :d_head//2]", "Ch02 RoPE snippet must use pos_ids branch"),
        (
            ch02,
            "torch.allclose(scores[1:, 1:], scores[:-1, :-1], atol=1e-5)",
            "Ch02 RoPE verification must check Toeplitz structure with tensor slicing",
        ),
        (ch04, "repeat_interleave(n_rep, dim=1)", "Ch04 GQA instructions must use PyTorch repeat_interleave signature"),
        (ch04, "k = k.repeat_interleave(self.n_rep, dim=1)", "Ch04 GQA code must repeat K along head dimension"),
        (ch04, "v = v.repeat_interleave(self.n_rep, dim=1)", "Ch04 GQA code must repeat V along head dimension"),
    ]
    for content, needle, reason in required:
        if needle not in content:
            fail(f"chapter code contract missing: {reason}: {needle}")

    forbidden = [
        (ch02, "diag_neg", "Ch02 RoPE verification must not require positive/negative offset symmetry"),
        (ch04, "repeat_interleave(dim=1, factor=n_rep)", "invalid PyTorch repeat_interleave factor keyword"),
    ]
    for content, needle, reason in forbidden:
        if needle in content:
            fail(f"chapter code contract contains forbidden pattern: {reason}: {needle}")

    ok("chapter code snippets match assignment API contracts")


def check_python_code_blocks_compile() -> None:
    compile_hits = []
    unescaped_tag_hits = []
    block_count = 0

    for path in sorted((ROOT / "chapters").glob("ch*.html")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        parser = PythonCodeBlockParser()
        parser.feed(text)
        for start_line, code in parser.blocks:
            block_count += 1
            try:
                compile(code, f"{rel}:{start_line}", "exec")
            except Exception as exc:
                compile_hits.append((rel, start_line, type(exc).__name__, str(exc)))

        for match in re.finditer(r"<div class=\"code-block\" data-lang=\"python\">.*?</div>", text, re.DOTALL):
            block = match.group(0)
            for tag_like in re.finditer(r"(?<!&lt;)<[/]?[A-Za-z][A-Za-z0-9_:-]*[^>]*>", block):
                raw = tag_like.group(0)
                if raw.startswith('<div class="code-block"') or raw == "</div>":
                    continue
                lineno = text.count("\n", 0, match.start() + tag_like.start()) + 1
                unescaped_tag_hits.append((rel, lineno, raw[:80]))

    if unescaped_tag_hits:
        details = "; ".join(
            f"{path}:{lineno} {raw}" for path, lineno, raw in unescaped_tag_hits[:10]
        )
        fail(f"unescaped tag-like text inside python code blocks: {details}")
    if compile_hits:
        details = "; ".join(
            f"{path}:{line} {kind}: {message}" for path, line, kind, message in compile_hits[:10]
        )
        fail(f"python code blocks fail to compile: {details}")

    ok(f"chapter python reference code blocks compile ({block_count} blocks)")


def check_exercise_widgets() -> None:
    malformed_attr_hits = []
    structural_hits = []
    total_exercises = 0

    for path in sorted((ROOT / "chapters").glob("ch*.html")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for match in MALFORMED_EXERCISE_ATTR_RE.finditer(text):
            lineno = text.count("\n", 0, match.start()) + 1
            malformed_attr_hits.append((rel, lineno))

        parser = ExerciseWidgetParser()
        parser.feed(text)
        total_exercises += len(parser.exercises)
        for exercise in parser.exercises:
            line = int(exercise["line"])
            answer = str(exercise["answer"])
            explain = str(exercise["explain"]).strip()
            inputs = list(exercise["inputs"])
            onclicks = list(exercise["onclicks"])
            has_feedback = bool(exercise["has_feedback"])
            names = {name for name, _ in inputs}
            values = [value for _, value in inputs]

            if not answer:
                structural_hits.append((rel, line, "missing data-answer"))
            if len(explain) < 20:
                structural_hits.append((rel, line, "missing or too-short data-explain"))
            if len(inputs) != 4:
                structural_hits.append((rel, line, f"expected 4 radio options, got {len(inputs)}"))
            if len(names) != 1:
                structural_hits.append((rel, line, f"radio options must share one name, got {sorted(names)}"))
            if len(values) != len(set(values)):
                structural_hits.append((rel, line, "duplicate radio option values"))
            if answer and answer not in values:
                structural_hits.append((rel, line, f"data-answer {answer!r} not present in option values {values}"))
            if len(onclicks) != 1:
                structural_hits.append((rel, line, f"expected one LLM.checkMC button, got {len(onclicks)}"))
            elif names:
                expected_group = next(iter(names))
                if f"'{expected_group}'" not in onclicks[0] and f'"{expected_group}"' not in onclicks[0]:
                    structural_hits.append((rel, line, "LLM.checkMC group does not match radio name"))
            if not has_feedback:
                structural_hits.append((rel, line, "missing feedback container"))

    if malformed_attr_hits:
        details = "; ".join(f"{path}:{lineno}" for path, lineno in malformed_attr_hits[:10])
        fail(f"malformed exercise attributes, likely unescaped quotes in data-explain: {details}")
    if total_exercises != EXPECTED_INTERACTIVE_EXERCISES:
        fail(f"expected {EXPECTED_INTERACTIVE_EXERCISES} interactive exercises, got {total_exercises}")
    if structural_hits:
        details = "; ".join(f"{path}:{lineno} {reason}" for path, lineno, reason in structural_hits[:10])
        fail(f"invalid exercise widget structure: {details}")

    ok(f"interactive exercise widgets are valid ({total_exercises} exercises)")


def check_unqualified_claim_phrasing() -> None:
    hits = []
    for path in sorted((ROOT / "chapters").glob("ch*.html")) + [ROOT / "README.md"]:
        if not path.exists():
            continue
        rel = path.relative_to(ROOT)
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for pattern, reason in UNQUALIFIED_CLAIM_PATTERNS:
                if pattern.search(line):
                    hits.append((rel, lineno, reason))

    if hits:
        details = "; ".join(f"{path}:{lineno} ({reason})" for path, lineno, reason in hits[:10])
        fail(f"unqualified strong claims in course text: {details}")

    ok("chapter claim phrasing avoids known unqualified overclaims")


def check_chapter_counts() -> None:
    chapter_files = sorted((ROOT / "chapters").glob("ch*.html"))
    if len(chapter_files) != EXPECTED_CHAPTERS:
        fail(f"expected {EXPECTED_CHAPTERS} chapter files, got {len(chapter_files)}")

    js = read("js/app.js")
    entries = re.findall(r"\{id:(\d+), file:'(ch\d+\.html)'.*?sections:(\d+)\}", js)
    if len(entries) != EXPECTED_CHAPTERS:
        fail(f"expected {EXPECTED_CHAPTERS} CHAPTERS entries in js/app.js, got {len(entries)}")

    total = 0
    for _, file_name, declared in entries:
        html = read(f"chapters/{file_name}")
        ids = re.findall(r'<section class="card" id="([^"]+)"', html)
        unique_ids = set(ids)
        if len(ids) != len(unique_ids):
            fail(f"{file_name} has duplicate section ids")
        if len(ids) != int(declared):
            fail(f"{file_name} declares {declared} sections in js/app.js but has {len(ids)}")
        total += len(ids)

    if total != EXPECTED_SECTIONS:
        fail(f"expected {EXPECTED_SECTIONS} total sections, got {total}")
    ok(f"chapter metadata matches {EXPECTED_CHAPTERS} chapters / {EXPECTED_SECTIONS} sections")


def check_public_stats() -> None:
    readme = read("README.md")
    syllabus = read("docs/syllabus.md")
    index = read("index.html")
    required = [
        (readme, f"sections-{EXPECTED_SECTIONS}-yellow", "README section badge"),
        (readme, f"{EXPECTED_SECTIONS} 小节", "README section total"),
        (readme, f"exercises-{EXPECTED_EXERCISES}", "README exercise badge"),
        (readme, "11 张 SVG 概念示意图 + favicon", "README image inventory total"),
        (readme, "11 张 SVG 图表", "README feature image total"),
        (index, f"{EXPECTED_SECTIONS} 小节", "index section total"),
        (index, f"{EXPECTED_EXERCISES} 道", "index exercise total"),
        (index, "inference-engineer-curriculum.html", "index graduation roadmap link"),
        (index, "training-engineer-curriculum.html", "index training roadmap link"),
        (readme, "projects/inference-engineering-capstone/", "README capstone link"),
        (readme, "projects/training-engineering-capstone/", "README training capstone link"),
        (readme, '.venv/bin/python -c "import sys, torch;', "README .venv torch smoke test"),
        (readme, ".venv/bin/python verify_course.py", "README .venv verify command"),
        (readme, ".venv/bin/python run_assignment_tests.py", "README .venv assignment command"),
        (
            readme,
            ".venv/bin/python verify_course.py --capstone --training",
            "README .venv publish gate command",
        ),
        (
            syllabus,
            ".venv/bin/python verify_course.py --capstone --training",
            "syllabus .venv publish gate command",
        ),
    ]
    for content, needle, label in required:
        if needle not in content:
            fail(f"missing {label}: {needle}")
    ok("public stats and course links are present")


def check_university_course_scaffold() -> None:
    readme = read("README.md")
    required_readme = [
        "高校课程规格",
        "章节编程作业",
        "书面推导与概念题",
        "训练工程 Capstone",
        "推理工程 Capstone",
        "Ch01-Ch10",
        "来源等级",
        "复核日期",
        "2026-06-05",
        "D：monitor-only",
        "docs/syllabus.md",
        "docs/cs224n-benchmark-crosswalk.md",
        "docs/cs224n-current-benchmark-snapshot.md",
        "docs/course-outcome-map.md",
        "docs/course-operations-log.md",
        "docs/lecture-plan.md",
        "docs/lecture-slide-outline.md",
        "docs/lecture-notes-index.md",
        "docs/lecture-notes-quality-review.md",
        "docs/lecture-notes-review-ledger.md",
        "docs/core-concept-glossary.md",
        "docs/topic-dependency-map.md",
        "docs/notation-shape-glossary.md",
        "docs/worked-example-pack.md",
        "docs/board-derivation-pack.md",
        "docs/mathematical-derivation-audit.md",
        "docs/demo-runbook.md",
        "docs/course-materials-index.md",
        "docs/course-calendar-deadline-ledger.md",
        "docs/lecture-media-access-policy.md",
        "docs/material-versioning-archive-policy.md",
        "docs/course-communication-policy.md",
        "docs/course-staff-office-hours-directory.md",
        "docs/enrollment-audit-public-use-policy.md",
        "docs/discussion-office-hours-guide.md",
        "docs/student-faq-troubleshooting.md",
        "docs/environment-reproducibility.md",
        "docs/quiz-checkpoint-guide.md",
        "docs/assessment-administration-policy.md",
        "docs/concept-misconception-map.md",
        "docs/midterm-final-review-pack.md",
        "docs/participation-feedback-guide.md",
        "docs/guest-speaker-seminar-policy.md",
        "docs/staff-runbook.md",
        "docs/course-policies.md",
        "docs/staff-assistance-code-review-policy.md",
        "docs/academic-integrity-case-process.md",
        "docs/accessibility-student-support.md",
        "docs/prerequisite-diagnostic.md",
        "docs/python-pytorch-review-session.md",
        "docs/math-prerequisites.md",
        "docs/ml-foundations-prerequisite-bridge.md",
        "docs/reading-list.md",
        "docs/frontier-seminar-handout.md",
        "docs/chapter-source-map.md",
        "docs/chapter-claim-audit-ledger.md",
        "docs/claim-audit-worksheet.md",
        "docs/external-source-inventory.md",
        "docs/external-source-verification.md",
        "docs/experimental-rigor-evaluation-statistics.md",
        "docs/assignment-handout-pack.md",
        "docs/written-problem-set.md",
        "docs/instructor-solution-guide.md",
        "docs/grading-calibration.md",
        "docs/assignment-submission-guide.md",
        "docs/gradebook-lms-operations.md",
        "docs/autograder-hidden-tests.md",
        "docs/private-autograder-operations.md",
        "docs/capstone-proposal-milestone.md",
        "docs/project-team-mentor-policy.md",
        "docs/default-final-project-guide.md",
        "docs/project-report-template.md",
        "docs/project-report-exemplar-pack.md",
        "docs/experimental-rigor-evaluation-statistics.md",
        "docs/final-project-showcase-archive-policy.md",
        "docs/capstone-project-gallery.md",
        "docs/compute-resource-guide.md",
        "docs/data-ethics-review.md",
        "docs/classic-nlp-handout.md",
        "docs/classic-nlp-deep-dive-module.md",
        "docs/nlp-evaluation-coverage.md",
        "assignments/ch11_classic_nlp/",
        "docs/project-report-rubric.md",
        "docs/presentation-peer-review.md",
        "docs/frontier-source-audit.md",
        "scripts/run_private_autograder.py",
    ]
    for needle in required_readme:
        if needle not in readme:
            fail(f"README missing university course scaffold marker: {needle}")

    for doc_path, markers in COURSE_DOCS.items():
        path = ROOT / doc_path
        if not path.exists():
            fail(f"missing university course document: {doc_path}")
        content = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in content:
                fail(f"{doc_path} missing required marker: {marker}")

    for i in range(1, EXPECTED_CHAPTERS + 1):
        chapter = f"ch{i:02d}.html"
        html = read(f"chapters/{chapter}")
        for marker in CHAPTER_QUALITY_MARKERS:
            if marker not in html:
                fail(f"{chapter} missing learning scaffold marker: {marker}")
        for marker in CHAPTER_SOURCE_GUIDANCE_MARKERS:
            if marker not in html:
                fail(f"{chapter} missing source guidance marker: {marker}")
        assignment = EXPECTED_ASSIGNMENTS[i - 1]
        link = f"../assignments/{assignment}/"
        if link not in html:
            fail(f"{chapter} missing assignment link: {link}")

    ok("university course scaffold and chapter source guidance are present in README, audit doc, and all chapters")


def check_concept_misconception_map() -> None:
    text = read("docs/concept-misconception-map.md")
    issues = []
    for module in EXPECTED_CONCEPT_MODULES:
        if f"| {module} |" not in text:
            issues.append(f"missing module row: {module}")

    required_terms = [
        "必须掌握",
        "常见误区",
        "快速检查",
        "补救材料",
        "评分证据",
        "shape invariant",
        "数学或概率边界",
        "工程失败模式",
        "hidden tests",
        "office hours",
    ]
    for term in required_terms:
        if term not in text:
            issues.append(f"missing concept-map term: {term}")

    high_risk_boundaries = [
        "Shape first",
        "Mask before probability",
        "Norm vs semantics",
        "Metric vs quality",
        "Public tests vs mastery",
        "Frontier claims",
    ]
    for boundary in high_risk_boundaries:
        if f"| {boundary} |" not in text:
            issues.append(f"missing high-risk boundary: {boundary}")

    assignment_refs = re.findall(r"`assignments/([^`]+)`", text)
    if len(set(assignment_refs)) < len(EXPECTED_ASSIGNMENTS):
        issues.append(
            "concept map must reference every assignment or equivalent topic, "
            f"got {len(set(assignment_refs))}/{len(EXPECTED_ASSIGNMENTS)} assignment refs"
        )

    for quick_check_type in (
        "Shape trace",
        "Boundary fix",
        "Claim audit",
        "Metric interpretation",
        "Reproducibility check",
    ):
        if f"| {quick_check_type} |" not in text:
            issues.append(f"missing quick-check template: {quick_check_type}")

    if issues:
        fail(f"concept misconception map is incomplete: {'; '.join(issues[:10])}")
    ok(f"concept misconception map covers {len(EXPECTED_CONCEPT_MODULES)} modules and core high-risk boundaries")


def check_core_concept_glossary() -> None:
    text = read("docs/core-concept-glossary.md")
    issues = []

    for marker in [
        "Core Concept Glossary",
        "复核日期：2026-06-05",
        "Definition Schema",
        "Core Concepts",
        "Cross-Reference Map",
        "Definition Quality Rules",
        "Maintenance Workflow",
        "Release Checklist",
        "concept-misconception-map.md",
        "chapter-source-map.md",
        "notation-shape-glossary.md",
        "worked-example-pack.md",
        "assessment-blueprint-coverage-matrix.md",
        "external-source-verification.md",
        "frontier-source-audit.md",
        ".venv/bin/python verify_course.py",
        "student site release",
    ]:
        if marker not in text:
            issues.append(f"missing core concept glossary marker: {marker}")

    schema_rows = extract_markdown_table_after(text, "## Definition Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    for field in ["concept_id", "term", "course definition", "not this", "evidence anchor", "source boundary"]:
        if field not in schema_fields:
            issues.append(f"core concept schema missing field: {field}")

    concept_rows = extract_markdown_table_after(text, "## Core Concepts")
    if len(concept_rows) < 26:
        issues.append(f"expected at least 25 core concepts plus header, got {len(concept_rows)}")
    concept_ids = {cells[0] for cells in concept_rows[1:] if cells}
    for concept_id in [
        "CG-TOKEN-BPE",
        "CG-EMBED",
        "CG-ROPE",
        "CG-ATTN",
        "CG-CAUSAL-MASK",
        "CG-GQA",
        "CG-MLA",
        "CG-LAYERNORM",
        "CG-RMSNORM",
        "CG-DECODER-LM",
        "CG-MOE",
        "CG-CE-PPL",
        "CG-ADAMW",
        "CG-SAMPLING",
        "CG-SPECDEC",
        "CG-SFT",
        "CG-LORA",
        "CG-DPO",
        "CG-GRPO",
        "CG-KVCACHE",
        "CG-RAG",
        "CG-SLO",
        "CG-EVAL-METRIC",
        "CG-SOURCE-BOUNDARY",
    ]:
        if concept_id not in concept_ids:
            issues.append(f"core concept glossary missing concept: {concept_id}")

    for cells in concept_rows[1:]:
        if len(cells) != 6:
            issues.append(f"core concept row expected 6 cells, got {len(cells)}: {cells[:2]}")
            continue
        concept_id, _term, definition, not_this, evidence, boundary = cells
        if not definition or not not_this or not evidence or not boundary:
            issues.append(f"{concept_id} missing definition, misconception boundary, evidence, or source boundary")
        if not concept_id.startswith("CG-"):
            issues.append(f"concept id must start with CG-: {concept_id}")

    cross_rows = extract_markdown_table_after(text, "## Cross-Reference Map")
    cross_groups = {cells[0] for cells in cross_rows[1:] if cells}
    for group in ["Shape-bearing terms", "Misconception-prone terms", "Formula-heavy terms", "Worked examples", "Source-sensitive terms", "Assessment terms"]:
        if group not in cross_groups:
            issues.append(f"core concept glossary missing cross-reference group: {group}")

    quality_rows = extract_markdown_table_after(text, "## Definition Quality Rules")
    quality_ids = {cells[0] for cells in quality_rows[1:] if cells}
    for rule_id in ["CG-R1", "CG-R2", "CG-R3", "CG-R4", "CG-R5"]:
        if rule_id not in quality_ids:
            issues.append(f"core concept glossary missing definition quality rule: {rule_id}")

    for workflow_marker in ["new term", "office hours", "source boundary", "tensor or unit convention", "linked source/assessment material"]:
        if workflow_marker not in text:
            issues.append(f"core concept maintenance workflow missing marker: {workflow_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/concept-misconception-map.md",
        "docs/chapter-source-map.md",
        "docs/notation-shape-glossary.md",
        "docs/worked-example-pack.md",
        "docs/assessment-blueprint-coverage-matrix.md",
        "docs/university-course-quality-audit.md",
    ]
    for doc_path in linked_docs:
        if "core-concept-glossary.md" not in read(doc_path):
            issues.append(f"{doc_path} missing core concept glossary link")

    if "core-concept-glossary.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing core concept glossary")
    if "docs/core-concept-glossary.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing core concept glossary")

    if issues:
        fail(f"core concept glossary is incomplete: {'; '.join(issues[:10])}")
    ok("core concept glossary covers definitions, misconception boundaries, evidence anchors, source boundaries, cross-references, and quality rules")


def check_topic_dependency_map() -> None:
    text = read("docs/topic-dependency-map.md")
    issues = []

    for marker in [
        "Topic Dependency and Spiral Review Map",
        "复核日期：2026-06-05",
        "Dependency Layers",
        "Chapter Dependency Graph",
        "Spiral Review Schedule",
        "Dependency Failure Signals",
        "Student Navigation Rules",
        "Staff Review Workflow",
        "Release Checklist",
        "core-concept-glossary.md",
        "notation-shape-glossary.md",
        "worked-example-pack.md",
        "concept-misconception-map.md",
        "course-outcome-map.md",
        "assessment-blueprint-coverage-matrix.md",
        "learning-analytics-remediation-plan.md",
        "recitation-worksheet-pack.md",
        "chapter-source-map.md",
        "paper-to-code-traceability-matrix.md",
        ".venv/bin/python verify_course.py",
        "student site release",
    ]:
        if marker not in text:
            issues.append(f"missing topic dependency marker: {marker}")

    layer_rows = extract_markdown_table_after(text, "## Dependency Layers")
    layer_ids = {cells[0] for cells in layer_rows[1:] if cells}
    for layer_id in [
        "TD-L0-PREREQ",
        "TD-L1-TOKEN",
        "TD-L2-ATTN",
        "TD-L3-BLOCK",
        "TD-L4-LM",
        "TD-L5-TRAIN",
        "TD-L6-GEN-ALIGN",
        "TD-L7-EVAL-SERVE",
        "TD-L8-CAPSTONE",
    ]:
        if layer_id not in layer_ids:
            issues.append(f"topic dependency map missing layer: {layer_id}")
    for cells in layer_rows[1:]:
        if len(cells) != 5:
            issues.append(f"dependency layer row expected 5 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[2] or not cells[3] or not cells[4]:
            issues.append(f"{cells[0]} missing depends_on, evidence, or failure signal")

    graph_rows = extract_markdown_table_after(text, "## Chapter Dependency Graph")
    chapter_ids = {cells[0] for cells in graph_rows[1:] if cells}
    for index in range(1, 12):
        graph_id = f"TD-CH{index:02d}"
        if graph_id not in chapter_ids:
            issues.append(f"topic dependency map missing chapter dependency: {graph_id}")
    for cells in graph_rows[1:]:
        if len(cells) != 6:
            issues.append(f"chapter dependency row expected 6 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[2] or not cells[3] or not cells[4] or not cells[5]:
            issues.append(f"{cells[0]} missing depends_on, unlocks, evidence, or remediation")

    spiral_rows = extract_markdown_table_after(text, "## Spiral Review Schedule")
    spiral_ids = {cells[0] for cells in spiral_rows[1:] if cells}
    for index in range(1, 11):
        review_id = f"TD-SR-W{index}"
        if review_id not in spiral_ids:
            issues.append(f"topic dependency map missing spiral review row: {review_id}")
    for cells in spiral_rows[1:]:
        if len(cells) != 6:
            issues.append(f"spiral review row expected 6 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[2] or not cells[3] or not cells[4] or not cells[5]:
            issues.append(f"{cells[0]} missing review focus, new topic, reactivated concept, or evidence")

    failure_rows = extract_markdown_table_after(text, "## Dependency Failure Signals")
    failure_ids = {cells[0] for cells in failure_rows[1:] if cells}
    for failure_id in [
        "TD-F-SHAPE",
        "TD-F-MASK",
        "TD-F-OBJECTIVE",
        "TD-F-METRIC",
        "TD-F-SOURCE",
        "TD-F-SYSTEMS",
    ]:
        if failure_id not in failure_ids:
            issues.append(f"topic dependency map missing failure signal: {failure_id}")
    for cells in failure_rows[1:]:
        if len(cells) != 5:
            issues.append(f"dependency failure row expected 5 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[2] or not cells[3] or not cells[4]:
            issues.append(f"{cells[0]} missing dependency, action, or staff follow-up")

    for navigation_marker in [
        "If RoPE is blocked",
        "If attention mask is blocked",
        "If training loss is blocked",
        "If alignment is blocked",
        "If serving evaluation is blocked",
        "If project evidence is blocked",
    ]:
        if navigation_marker not in text:
            issues.append(f"topic dependency navigation missing marker: {navigation_marker}")

    for workflow_marker in [
        "Before a module starts",
        "During recitation",
        "After grading",
        "chapter, assignment, metric, or paper recap changes",
        "Before release",
    ]:
        if workflow_marker not in text:
            issues.append(f"topic dependency staff workflow missing marker: {workflow_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/core-concept-glossary.md",
        "docs/notation-shape-glossary.md",
        "docs/worked-example-pack.md",
        "docs/concept-misconception-map.md",
        "docs/course-outcome-map.md",
        "docs/assessment-blueprint-coverage-matrix.md",
        "docs/learning-analytics-remediation-plan.md",
        "docs/recitation-worksheet-pack.md",
        "docs/university-course-quality-audit.md",
    ]
    for doc_path in linked_docs:
        if "topic-dependency-map.md" not in read(doc_path):
            issues.append(f"{doc_path} missing topic dependency map link")

    if "topic-dependency-map.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing topic dependency map")
    if "docs/topic-dependency-map.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing topic dependency map")

    if issues:
        fail(f"topic dependency map is incomplete: {'; '.join(issues[:10])}")
    ok("topic dependency map covers prerequisite layers, chapter dependencies, spiral review, failure signals, navigation, and release links")


def check_learning_analytics_remediation_plan() -> None:
    text = read("docs/learning-analytics-remediation-plan.md")
    issues = []

    for marker in [
        "Learning Analytics and Remediation Plan",
        "复核日期：2026-06-05",
        "Data Sources",
        "Trigger Thresholds",
        "Remediation Playbooks",
        "Weekly Review Workflow",
        "Student-Facing Feedback Template",
        "Operations Log Template",
        "Privacy and Fairness Rules",
        "Release Checklist",
        "quiz-checkpoint-guide.md",
        "concept-misconception-map.md",
        "recitation-worksheet-pack.md",
        "gradebook-lms-operations.md",
        "participation-feedback-guide.md",
        "staff-runbook.md",
        "accessibility-student-support.md",
        "course-operations-log.md",
    ]:
        if marker not in text:
            issues.append(f"missing learning analytics marker: {marker}")

    data_rows = extract_markdown_table_after(text, "## Data Sources")
    signal_ids = {cells[0] for cells in data_rows[1:] if cells}
    for signal_id in [
        "LA-QUIZ",
        "LA-ASSIGN",
        "LA-WORKSHEET",
        "LA-OH",
        "LA-READING",
        "LA-PROJECT",
        "LA-GRADEBOOK",
    ]:
        if signal_id not in signal_ids:
            issues.append(f"learning analytics missing data signal: {signal_id}")
    for cells in data_rows[1:]:
        if len(cells) != 5:
            issues.append(f"learning analytics data row expected 5 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[3] or not cells[4]:
            issues.append(f"{cells[0]} missing student-visible use or privacy boundary")

    trigger_rows = extract_markdown_table_after(text, "## Trigger Thresholds")
    if len(trigger_rows) < 9:
        issues.append(f"expected at least 8 trigger rows, got {max(0, len(trigger_rows) - 1)}")
    trigger_ids = {cells[0] for cells in trigger_rows[1:] if cells}
    for trigger_id in [
        "TR-SHAPE-30",
        "TR-MASK-20",
        "TR-SOURCE-30",
        "TR-PROJECT-RISK",
        "TR-REPRO-20",
        "TR-REVIEW-8",
        "TR-OH-3",
        "TR-ACCESS",
    ]:
        if trigger_id not in trigger_ids:
            issues.append(f"learning analytics missing trigger: {trigger_id}")
    for cells in trigger_rows[1:]:
        if len(cells) != 6:
            issues.append(f"learning analytics trigger row expected 6 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not all(cells[1:]):
            issues.append(f"{cells[0]} has empty trigger field")

    playbook_rows = extract_markdown_table_after(text, "## Remediation Playbooks")
    playbook_ids = {cells[0] for cells in playbook_rows[1:] if cells}
    for playbook_id in [
        "RP-SHAPE",
        "RP-MASK",
        "RP-NUMERIC",
        "RP-SOURCE",
        "RP-REPRO",
        "RP-PROJECT-SCOPE",
    ]:
        if playbook_id not in playbook_ids:
            issues.append(f"learning analytics missing playbook: {playbook_id}")
    for cells in playbook_rows[1:]:
        if len(cells) != 5:
            issues.append(f"learning analytics playbook row expected 5 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[2] or not cells[4]:
            issues.append(f"{cells[0]} missing student task or exit criterion")

    workflow_rows = extract_markdown_table_after(text, "## Weekly Review Workflow")
    workflow_steps = [cells[0] for cells in workflow_rows[1:] if cells]
    for expected_step in ["1. collect", "2. classify", "3. choose action", "4. deliver", "5. verify", "6. log"]:
        if expected_step not in workflow_steps:
            issues.append(f"learning analytics workflow missing step: {expected_step}")

    for template_marker in [
        "Observed pattern: aggregate category only",
        "privacy_check:",
        "exit_criterion:",
        "follow_up_result:",
    ]:
        if template_marker not in text:
            issues.append(f"learning analytics template missing marker: {template_marker}")

    for privacy_marker in [
        "聚合类别",
        "个人成绩",
        "late days",
        "accommodation",
        "诚信个案",
        "hidden tests",
        "不得发布隐藏输入",
    ]:
        if privacy_marker not in text:
            issues.append(f"learning analytics privacy rule missing marker: {privacy_marker}")

    for doc_path in [
        "README.md",
        "docs/quiz-checkpoint-guide.md",
        "docs/concept-misconception-map.md",
        "docs/recitation-worksheet-pack.md",
        "docs/gradebook-lms-operations.md",
        "docs/participation-feedback-guide.md",
        "docs/learning-outcome-attainment-report.md",
        "docs/teaching-observation-course-evaluation.md",
        "docs/staff-runbook.md",
        "docs/course-operations-log.md",
    ]:
        if "learning-analytics-remediation-plan.md" not in read(doc_path):
            issues.append(f"{doc_path} missing learning analytics remediation plan link")

    if issues:
        fail(f"learning analytics remediation plan is incomplete: {'; '.join(issues[:10])}")
    ok("learning analytics remediation plan covers signals, triggers, playbooks, workflow, privacy, and linked remediation evidence")


def check_weekly_teaching_reflection_adjustment_log() -> None:
    text = read("docs/weekly-teaching-reflection-adjustment-log.md")
    issues = []

    for marker in [
        "Weekly Teaching Reflection and Adjustment Log",
        "复核日期：2026-06-05",
        "Reflection Schema",
        "Evidence Sources",
        "Adjustment Action Bank",
        "Current Reflection Records",
        "Next-Lecture Patch Template",
        "Staff Workflow",
        "Release Checklist",
        "lecture-plan.md",
        "discussion-office-hours-guide.md",
        "course-operations-log.md",
        "learning-analytics-remediation-plan.md",
        "teaching-observation-course-evaluation.md",
        "course-materials-index.md",
        "lecture-notes-quality-review.md",
        "lecture-notes-review-ledger.md",
        "lecture-slide-sample-pack.md",
        "recitation-worksheet-pack.md",
        "quiz-checkpoint-guide.md",
        "assessment-item-analysis-psychometrics.md",
        "participation-feedback-guide.md",
        "course-communication-policy.md",
        "course-errata-correction-ledger.md",
        "student-faq-troubleshooting.md",
        "accessibility-student-support.md",
    ]:
        if marker not in text:
            issues.append(f"missing weekly teaching reflection marker: {marker}")

    schema_rows = extract_markdown_table_after(text, "## Reflection Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    for field in [
        "reflection_id",
        "lecture_or_week",
        "evidence_sources",
        "observed_pattern",
        "interpretation",
        "next_adjustment",
        "student_message",
        "verification_signal",
        "owner",
        "status",
    ]:
        if field not in schema_fields:
            issues.append(f"weekly reflection schema missing field: {field}")
    for cells in schema_rows[1:]:
        if len(cells) != 3:
            issues.append(f"weekly reflection schema row expected 3 cells, got {len(cells)}: {cells[:2]}")

    evidence_rows = extract_markdown_table_after(text, "## Evidence Sources")
    evidence_ids = {cells[0] for cells in evidence_rows[1:] if cells}
    for source_id in [
        "WTR-QUICK",
        "WTR-EXIT",
        "WTR-OH",
        "WTR-ASSIGN",
        "WTR-READING",
        "WTR-PROJECT",
        "WTR-PEER",
        "WTR-ACCESS",
    ]:
        if source_id not in evidence_ids:
            issues.append(f"weekly reflection missing evidence source: {source_id}")
    for cells in evidence_rows[1:]:
        if len(cells) != 5:
            issues.append(f"weekly reflection evidence row expected 5 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[3] or not cells[4]:
            issues.append(f"{cells[0]} missing privacy boundary or linked doc")

    action_rows = extract_markdown_table_after(text, "## Adjustment Action Bank")
    action_ids = {cells[0] for cells in action_rows[1:] if cells}
    for action_id in [
        "WTR-A-RECAP",
        "WTR-A-WORKSHEET",
        "WTR-A-DEMO",
        "WTR-A-FAQ",
        "WTR-A-HANDOUT",
        "WTR-A-RUBRIC",
        "WTR-A-PACING",
        "WTR-A-PROJECT",
        "WTR-A-SOURCE",
        "WTR-A-ACCESS",
    ]:
        if action_id not in action_ids:
            issues.append(f"weekly reflection missing action: {action_id}")
    for cells in action_rows[1:]:
        if len(cells) != 5:
            issues.append(f"weekly reflection action row expected 5 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[2] or not cells[4]:
            issues.append(f"{cells[0]} missing visible change or verification signal")

    record_rows = extract_markdown_table_after(text, "## Current Reflection Records")
    record_ids = {cells[0] for cells in record_rows[1:] if cells}
    for record_id in [
        "WTR-2026-L02-ROPE",
        "WTR-2026-L03-MASK",
        "WTR-2026-L05-GQA",
        "WTR-2026-L09-TRAIN",
        "WTR-2026-L15-EVAL",
        "WTR-2026-L18-SLO",
    ]:
        if record_id not in record_ids:
            issues.append(f"weekly reflection missing current record: {record_id}")
    statuses = {cells[6] for cells in record_rows[1:] if len(cells) == 7}
    for status in ["planned", "in_progress", "verified", "deferred"]:
        if status not in statuses:
            issues.append(f"weekly reflection missing status: {status}")
    for cells in record_rows[1:]:
        if len(cells) != 7:
            issues.append(f"weekly reflection record row expected 7 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[3] or not cells[4] or not cells[5]:
            issues.append(f"{cells[0]} missing pattern, adjustment, or verification signal")

    for template_marker in [
        "reflection_id:",
        "lecture_or_week:",
        "evidence_sources:",
        "observed_pattern:",
        "interpretation:",
        "next_adjustment:",
        "student_message:",
        "verification_signal:",
        "owner:",
        "status:",
    ]:
        if template_marker not in text:
            issues.append(f"weekly reflection template missing marker: {template_marker}")

    for workflow_marker in [
        "within 24 hours",
        "Concept Mastery and Misconception Map",
        "Topic Dependency and Spiral Review Map",
        "Course Errata and Correction Ledger",
        "External Source Verification Guide",
        "Gradebook and LMS Operations Guide",
        "regrade",
        "next quick check",
    ]:
        if workflow_marker not in text:
            issues.append(f"weekly reflection workflow missing marker: {workflow_marker}")

    for privacy_marker in [
        "student identifiers",
        "raw survey comments",
        "personal grades",
        "accommodation details",
        "integrity cases",
        "hidden tests",
        "reference_solution.py",
        "private grading samples",
        "real student submissions",
        "student site release",
    ]:
        if privacy_marker not in text:
            issues.append(f"weekly reflection privacy/release boundary missing marker: {privacy_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/course-operations-log.md",
        "docs/learning-analytics-remediation-plan.md",
        "docs/teaching-observation-course-evaluation.md",
        "docs/lecture-plan.md",
        "docs/discussion-office-hours-guide.md",
        "docs/course-materials-index.md",
        "docs/lecture-notes-quality-review.md",
        "docs/participation-feedback-guide.md",
        "docs/student-faq-troubleshooting.md",
        "docs/university-course-quality-audit.md",
    ]
    for doc_path in linked_docs:
        if "weekly-teaching-reflection-adjustment-log.md" not in read(doc_path):
            issues.append(f"{doc_path} missing weekly teaching reflection log link")

    if "weekly-teaching-reflection-adjustment-log.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing weekly teaching reflection log")
    if "docs/weekly-teaching-reflection-adjustment-log.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing weekly teaching reflection log")

    if issues:
        fail(f"weekly teaching reflection adjustment log is incomplete: {'; '.join(issues[:10])}")
    ok("weekly teaching reflection adjustment log covers schema, evidence sources, action bank, records, workflow, privacy, and release links")


def check_course_operations_log_records() -> None:
    text = read("docs/course-operations-log.md")
    issues = []

    for placeholder in ["待填", "YYYY-MM-DD"]:
        if placeholder in text:
            issues.append(f"course operations log still contains placeholder marker: {placeholder}")

    for marker in [
        "dry-run baseline",
        "live offering",
        "Weekly Teaching Reflection and Adjustment Log",
        "Learning Analytics and Remediation Plan",
        "Teaching Observation and Course Evaluation Dossier",
        "Pre-Semester Readiness Audit",
        "Course Errata and Correction Ledger",
        "scripts/generate_course_evidence_manifest.py",
        ".venv/bin/python verify_course.py",
        "ASSIGNMENT TESTS: PASS (11 suite(s))",
        "source governance ready",
        "private autograder manifest",
        "student release",
    ]:
        if marker not in text:
            issues.append(f"course operations log missing marker: {marker}")

    section_expectations = {
        "## 每周运行记录": ["Week 1", "Week 2", "Ch01-Ch02", "Ch03", "WTR-2026-L02-ROPE", "WTR-2026-L03-MASK"],
        "## Quiz 与阶段 Checkpoint 记录": ["Week 5", "Week 9", "Midterm checkpoint dry run", "Capstone checkpoint dry run"],
        "## Demo Dry Run 记录": ["L1", "L3", "L18", "PASS in course verifier"],
        "## 作业复盘记录": ["ch01_bpe", "ch02_embeddings", "reference solution public suite"],
        "## 隐藏测试统计": ["ch02_embeddings", "ch03_attention", "private-run required before live grading"],
        "## 讨论课与 Office Hours 记录": ["Week 2", "Week 5", "causal mask", "training-loop debugging"],
        "## 学生 FAQ 更新记录": ["2026-06-05", ".venv/bin/python", "hidden-test boundaries"],
        "## 项目复现记录": ["training capstone", "inference capstone", "PASS through full verifier evidence"],
        "## 算力额度与成本记录": ["training capstone readiness", "inference capstone readiness", "local dry-run cost not billed"],
        "## 阅读复盘与来源审计记录": ["Week 1", "Week 8", "metric-card mini case"],
        "## 课堂参与与反馈调查记录": ["Week 5", "Week 10", "live participation pending"],
        "## 复核与评分争议记录": ["ch02_embeddings dry-run", "capstone dry-run", "rubric note"],
        "## 前沿来源更新记录": ["CS224N current benchmark snapshot", "Course readiness evidence", "Course operations evidence"],
        "## 期末课程复盘": ["design_ready", "real student attainment", "source governance ready"],
    }
    for heading, markers in section_expectations.items():
        rows = extract_markdown_table_after(text, heading)
        if len(rows) < 2:
            issues.append(f"course operations section has no records: {heading}")
            continue
        section_text = "\n".join("|".join(row) for row in rows)
        for marker in markers:
            if marker not in section_text:
                issues.append(f"{heading} missing concrete record marker: {marker}")

    for boundary_marker in [
        "不记录隐藏输入原文",
        "不公开个人账号",
        "只记录聚合反馈",
        "live projects must add dataset cards",
        "hidden-run manifest in private storage",
        "真实开课后应追加 `live offering` 行",
    ]:
        if boundary_marker not in text:
            issues.append(f"course operations privacy/live boundary missing marker: {boundary_marker}")

    if issues:
        fail(f"course operations log records are incomplete: {'; '.join(issues[:10])}")
    ok("course operations log has concrete dry-run baseline records, privacy boundaries, live-offering follow-ups, and no placeholder rows")


def check_learning_outcome_attainment_report() -> None:
    text = read("docs/learning-outcome-attainment-report.md")
    issues = []

    for marker in [
        "Learning Outcome Attainment Report",
        "复核日期：2026-06-05",
        "Attainment Evidence Taxonomy",
        "Outcome Attainment Targets",
        "Current Dry-Run Attainment Matrix",
        "Direct Evidence Collection Plan",
        "Indirect Evidence and Triangulation",
        "Attainment Status Codes",
        "Closing the Loop Actions",
        "Release Checklist",
        "course-outcome-map.md",
        "assessment-blueprint-coverage-matrix.md",
        "assessment-item-analysis-psychometrics.md",
        "gradebook-lms-operations.md",
        "learning-analytics-remediation-plan.md",
        "teaching-observation-course-evaluation.md",
        "project-submission-dossier.md",
        "course-operations-log.md",
    ]:
        if marker not in text:
            issues.append(f"missing attainment report marker: {marker}")

    taxonomy_rows = extract_markdown_table_after(text, "## Attainment Evidence Taxonomy")
    taxonomy_ids = {cells[0] for cells in taxonomy_rows[1:] if cells}
    for evidence_type in ["direct_auto", "direct_manual", "indirect_student", "indirect_staff", "readiness_proxy"]:
        if evidence_type not in taxonomy_ids:
            issues.append(f"attainment report missing evidence type: {evidence_type}")

    target_rows = extract_markdown_table_after(text, "## Outcome Attainment Targets")
    if len(target_rows) != 7:
        issues.append(f"expected 6 attainment target rows plus header, got {len(target_rows)}")
    target_outcomes = {cells[0] for cells in target_rows[1:] if cells}
    for outcome_id in ["CO1", "CO2", "CO3", "CO4", "CO5", "CO6"]:
        if outcome_id not in target_outcomes:
            issues.append(f"attainment report missing target row: {outcome_id}")
    for cells in target_rows[1:]:
        if len(cells) != 5:
            issues.append(f"attainment target row expected 5 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[1] or not cells[2] or not cells[3] or not cells[4]:
            issues.append(f"{cells[0]} missing target or action threshold")

    dry_rows = extract_markdown_table_after(text, "## Current Dry-Run Attainment Matrix")
    if len(dry_rows) != 7:
        issues.append(f"expected 6 dry-run attainment rows plus header, got {len(dry_rows)}")
    dry_outcomes = {cells[0] for cells in dry_rows[1:] if cells}
    for outcome_id in ["CO1", "CO2", "CO3", "CO4", "CO5", "CO6"]:
        if outcome_id not in dry_outcomes:
            issues.append(f"attainment report missing dry-run row: {outcome_id}")
    for cells in dry_rows[1:]:
        if len(cells) != 6:
            issues.append(f"dry-run attainment row expected 6 cells, got {len(cells)}: {cells[:2]}")
            continue
        if cells[4] != "design_ready":
            issues.append(f"{cells[0]} dry-run status must be design_ready, got {cells[4]}")
        if "needs real" not in cells[5]:
            issues.append(f"{cells[0]} gap must explicitly require real offering data")

    collection_rows = extract_markdown_table_after(text, "## Direct Evidence Collection Plan")
    collection_ids = {cells[0] for cells in collection_rows[1:] if cells}
    for collection_id in ["LOA-AUTO-ASSIGN", "LOA-WRITTEN", "LOA-QUIZ", "LOA-CAPSTONE", "LOA-READING", "LOA-EVAL"]:
        if collection_id not in collection_ids:
            issues.append(f"attainment report missing collection plan: {collection_id}")

    status_rows = extract_markdown_table_after(text, "## Attainment Status Codes")
    status_ids = {cells[0] for cells in status_rows[1:] if cells}
    for status in ["design_ready", "partially_attained", "attained", "over_assessed", "under_supported", "inconclusive"]:
        if status not in status_ids:
            issues.append(f"attainment report missing status code: {status}")

    action_rows = extract_markdown_table_after(text, "## Closing the Loop Actions")
    action_ids = {cells[0] for cells in action_rows[1:] if cells}
    for action_id in [
        "LOA-RECAP",
        "LOA-ASSIGN-REVISION",
        "LOA-RUBRIC-CAL",
        "LOA-PROJECT-CLINIC",
        "LOA-SOURCE-CASE",
        "LOA-EVAL-RECITATION",
    ]:
        if action_id not in action_ids:
            issues.append(f"attainment report missing loop action: {action_id}")

    for boundary_marker in [
        "不得把 `COURSE VERIFY: PASS` 解释为真实学生学习结果已经达成",
        "dry-run evidence does not prove real student attainment",
        "must be replaced or supplemented with real offering data",
    ]:
        if boundary_marker not in text:
            issues.append(f"attainment report missing boundary marker: {boundary_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/course-outcome-map.md",
        "docs/assessment-blueprint-coverage-matrix.md",
        "docs/learning-analytics-remediation-plan.md",
        "docs/teaching-observation-course-evaluation.md",
        "docs/course-operations-log.md",
    ]
    for doc_path in linked_docs:
        if "learning-outcome-attainment-report.md" not in read(doc_path):
            issues.append(f"{doc_path} missing learning outcome attainment report link")

    if "learning-outcome-attainment-report.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing learning outcome attainment report")
    if "docs/learning-outcome-attainment-report.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing learning outcome attainment report")

    if issues:
        fail(f"learning outcome attainment report is incomplete: {'; '.join(issues[:10])}")
    ok("learning outcome attainment report covers CO targets, dry-run gaps, evidence collection, status codes, loop actions, and release links")


def check_teaching_observation_course_evaluation() -> None:
    text = read("docs/teaching-observation-course-evaluation.md")
    issues = []

    for marker in [
        "Teaching Observation and Course Evaluation Dossier",
        "复核日期：2026-06-05",
        "Evaluation Sources",
        "Peer Observation Rubric",
        "Midterm Feedback Response Protocol",
        "End-of-Term Course Review",
        "Current Evaluation Ledger",
        "Student-Visible Response Memo Template",
        "Staff Observation Note Template",
        "Release Checklist",
        "participation-feedback-guide.md",
        "course-operations-log.md",
        "learning-analytics-remediation-plan.md",
        "lecture-notes-quality-review.md",
        "lecture-slide-sample-pack.md",
        "staff-runbook.md",
        "accessibility-student-support.md",
    ]:
        if marker not in text:
            issues.append(f"missing teaching evaluation marker: {marker}")

    source_rows = extract_markdown_table_after(text, "## Evaluation Sources")
    source_ids = {cells[0] for cells in source_rows[1:] if cells}
    for source_id in ["CE-PEER-OBS", "CE-MID-SURVEY", "CE-END-SURVEY", "CE-ANALYTICS", "CE-GRADING", "CE-CAPSTONE"]:
        if source_id not in source_ids:
            issues.append(f"teaching evaluation missing source: {source_id}")
    for cells in source_rows[1:]:
        if len(cells) != 5:
            issues.append(f"teaching evaluation source row expected 5 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[3] or not cells[4]:
            issues.append(f"{cells[0]} missing evidence or privacy boundary")

    rubric_rows = extract_markdown_table_after(text, "## Peer Observation Rubric")
    rubric_dimensions = {cells[0] for cells in rubric_rows[1:] if cells}
    for dimension in [
        "learning_goal_alignment",
        "technical_accuracy",
        "board_and_slide_clarity",
        "active_learning",
        "pacing_and_workload",
        "inclusion_accessibility",
        "assessment_alignment",
    ]:
        if dimension not in rubric_dimensions:
            issues.append(f"teaching evaluation missing peer rubric dimension: {dimension}")

    protocol_rows = extract_markdown_table_after(text, "## Midterm Feedback Response Protocol")
    protocol_steps = [cells[0] for cells in protocol_rows[1:] if cells]
    for step in ["1. collect", "2. code themes", "3. triangulate", "4. publish response memo", "5. update artifacts", "6. verify impact"]:
        if step not in protocol_steps:
            issues.append(f"teaching evaluation missing midterm response step: {step}")

    review_rows = extract_markdown_table_after(text, "## End-of-Term Course Review")
    review_areas = {cells[0] for cells in review_rows[1:] if cells}
    for area in [
        "outcome attainment",
        "content accuracy",
        "workload and pacing",
        "assessment quality",
        "project quality",
        "support and accessibility",
    ]:
        if area not in review_areas:
            issues.append(f"teaching evaluation missing end-term review area: {area}")

    ledger_rows = extract_markdown_table_after(text, "## Current Evaluation Ledger")
    if len(ledger_rows) < 6:
        issues.append(f"expected at least 5 current evaluation records, got {max(0, len(ledger_rows) - 1)}")
    ledger_ids = {cells[0] for cells in ledger_rows[1:] if cells}
    for record_id in ["CE-2026-OBS-L3", "CE-2026-MID-WORKLOAD", "CE-2026-ITEM-W5", "CE-2026-CAP-REPRO", "CE-2026-SOURCE"]:
        if record_id not in ledger_ids:
            issues.append(f"teaching evaluation missing ledger record: {record_id}")
    for cells in ledger_rows[1:]:
        if len(cells) != 7:
            issues.append(f"teaching evaluation ledger row expected 7 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[4] or not cells[5] or not cells[6]:
            issues.append(f"{cells[0]} missing action, owner, or status")

    for template_marker in [
        "What we heard:",
        "What we will change by date:",
        "What evidence we will watch next:",
        "observer_role:",
        "learning_goal_alignment:",
        "private_follow_up:",
    ]:
        if template_marker not in text:
            issues.append(f"teaching evaluation missing template marker: {template_marker}")

    for privacy_marker in [
        "不得公开学生个人反馈",
        "raw comments",
        "accommodation details",
        "staff personnel evaluation",
        "no student identifiers",
    ]:
        if privacy_marker not in text:
            issues.append(f"teaching evaluation privacy boundary missing marker: {privacy_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/participation-feedback-guide.md",
        "docs/course-operations-log.md",
        "docs/learning-analytics-remediation-plan.md",
        "docs/lecture-notes-quality-review.md",
        "docs/staff-runbook.md",
    ]
    for doc_path in linked_docs:
        if "teaching-observation-course-evaluation.md" not in read(doc_path):
            issues.append(f"{doc_path} missing teaching evaluation dossier link")

    if "teaching-observation-course-evaluation.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing teaching evaluation dossier")
    if "docs/teaching-observation-course-evaluation.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing teaching evaluation dossier")

    if issues:
        fail(f"teaching observation/course evaluation dossier is incomplete: {'; '.join(issues[:10])}")
    ok("teaching observation/course evaluation dossier covers sources, peer rubric, response protocol, end-term review, ledger, privacy, and release links")


def check_external_expert_review_dossier() -> None:
    text = read("docs/external-expert-review-dossier.md")
    issues = []

    for marker in [
        "External Expert Review Dossier",
        "复核日期：2026-06-05",
        "Review Scope",
        "Reviewer Independence Rules",
        "Review Rubric",
        "Current External Review Ledger",
        "Response and Closure Workflow",
        "Evidence Packet Template",
        "Severity and Required Response",
        "Release Checklist",
        "university-course-quality-audit.md",
        "chapter-claim-audit-ledger.md",
        "chapter-source-map.md",
        "mathematical-derivation-audit.md",
        "external-source-verification.md",
        "frontier-source-audit.md",
        "course-errata-correction-ledger.md",
        "teaching-observation-course-evaluation.md",
        "course-operations-log.md",
        "student site release",
        "no direct grading authority",
        "conflict_check",
        "reviewer_role",
        "source expertise",
        "confidentiality",
    ]:
        if marker not in text:
            issues.append(f"missing external expert review marker: {marker}")

    scope_rows = extract_markdown_table_after(text, "## Review Scope")
    scope_ids = {cells[0] for cells in scope_rows[1:] if cells}
    for scope_id in [
        "ER-CONTENT",
        "ER-MATH",
        "ER-SOURCES",
        "ER-ASSIGNMENTS",
        "ER-ASSESSMENT",
        "ER-PROJECTS",
        "ER-ACCESSIBILITY",
        "ER-RELEASE",
    ]:
        if scope_id not in scope_ids:
            issues.append(f"external expert review missing scope: {scope_id}")
    for cells in scope_rows[1:]:
        if len(cells) != 4:
            issues.append(f"external expert review scope row expected 4 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[2] or not cells[3]:
            issues.append(f"{cells[0]} missing expert task or evidence")

    independence_rows = extract_markdown_table_after(text, "## Reviewer Independence Rules")
    independence_ids = {cells[0] for cells in independence_rows[1:] if cells}
    for rule_id in ["ER-IND-ROLE", "ER-IND-CONFLICT", "ER-IND-EXPERTISE", "ER-IND-SEPARATION", "ER-IND-CONFIDENTIALITY"]:
        if rule_id not in independence_ids:
            issues.append(f"external expert review missing independence rule: {rule_id}")

    rubric_rows = extract_markdown_table_after(text, "## Review Rubric")
    rubric_dimensions = {cells[0] for cells in rubric_rows[1:] if cells}
    for dimension in [
        "technical_accuracy",
        "mathematical_rigor",
        "source_traceability",
        "assessment_alignment",
        "implementation_reproducibility",
        "project_rigor",
        "accessibility_inclusion",
        "release_safety",
    ]:
        if dimension not in rubric_dimensions:
            issues.append(f"external expert review missing rubric dimension: {dimension}")

    ledger_rows = extract_markdown_table_after(text, "## Current External Review Ledger")
    if len(ledger_rows) < 7:
        issues.append(f"expected at least 6 external review records, got {max(0, len(ledger_rows) - 1)}")
    ledger_ids = {cells[0] for cells in ledger_rows[1:] if cells}
    for review_id in [
        "ER-2026-MATH-ROPE",
        "ER-2026-SOURCE-FRONTIER",
        "ER-2026-ASSIGN-ATTN",
        "ER-2026-PROJECT-CAPSTONE",
        "ER-2026-ACCESS-MEDIA",
        "ER-2026-RELEASE-SAFETY",
    ]:
        if review_id not in ledger_ids:
            issues.append(f"external expert review missing ledger record: {review_id}")
    for cells in ledger_rows[1:]:
        if len(cells) != 7:
            issues.append(f"external expert review ledger row expected 7 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[4].startswith("ER-S") or not cells[5] or not cells[6]:
            issues.append(f"{cells[0]} missing severity, required response, or status")

    workflow_rows = extract_markdown_table_after(text, "## Response and Closure Workflow")
    workflow_steps = [cells[0] for cells in workflow_rows[1:] if cells]
    for step in ["1. intake", "2. triage", "3. response", "4. patch", "5. verify", "6. close"]:
        if step not in workflow_steps:
            issues.append(f"external expert review missing workflow step: {step}")

    severity_rows = extract_markdown_table_after(text, "## Severity and Required Response")
    severity_ids = {cells[0] for cells in severity_rows[1:] if cells}
    for severity in ["ER-S0", "ER-S1", "ER-S2", "ER-S3"]:
        if severity not in severity_ids:
            issues.append(f"external expert review missing severity code: {severity}")

    for template_marker in [
        "review_id:",
        "reviewer_role:",
        "conflict_check:",
        "materials_reviewed:",
        "verification_command:",
        "closure_status:",
    ]:
        if template_marker not in text:
            issues.append(f"external expert review missing evidence packet marker: {template_marker}")

    linked_docs = [
        "README.md",
        "docs/university-course-quality-audit.md",
        "docs/course-errata-correction-ledger.md",
        "docs/chapter-claim-audit-ledger.md",
        "docs/mathematical-derivation-audit.md",
        "docs/external-source-verification.md",
        "docs/frontier-source-audit.md",
        "docs/teaching-observation-course-evaluation.md",
        "docs/course-operations-log.md",
    ]
    for doc_path in linked_docs:
        if "external-expert-review-dossier.md" not in read(doc_path):
            issues.append(f"{doc_path} missing external expert review dossier link")

    if "external-expert-review-dossier.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing external expert review dossier")
    if "docs/external-expert-review-dossier.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing external expert review dossier")

    if issues:
        fail(f"external expert review dossier is incomplete: {'; '.join(issues[:10])}")
    ok("external expert review dossier covers independent scope, reviewer rules, rubric, ledger, workflow, severity, evidence template, and release links")


def check_workload_pacing_calibration() -> None:
    text = read("docs/workload-pacing-calibration.md")
    issues = []

    for marker in [
        "Workload and Pacing Calibration",
        "复核日期：2026-06-05",
        "Calibration Assumptions",
        "Weekly Workload Budget",
        "Difficulty Ladder",
        "Assignment Load Guardrails",
        "Overload Signals and Pacing Actions",
        "10-to-12 Week Expansion Map",
        "Student Time-Planning Template",
        "Staff Review Protocol",
        "Release Checklist",
        "syllabus.md",
        "course-calendar-deadline-ledger.md",
        "assignment-handout-pack.md",
        "recitation-worksheet-pack.md",
        "reading-list.md",
        "learning-analytics-remediation-plan.md",
        "compute-resource-guide.md",
        "course-operations-log.md",
    ]:
        if marker not in text:
            issues.append(f"missing workload pacing marker: {marker}")

    assumption_rows = extract_markdown_table_after(text, "## Calibration Assumptions")
    assumptions = {cells[0] for cells in assumption_rows[1:] if cells}
    for assumption in [
        "Offering length",
        "Contact time",
        "Student preparation",
        "Assignment cadence",
        "Expected weekly effort",
        "Overload boundary",
    ]:
        if assumption not in assumptions:
            issues.append(f"workload assumptions missing: {assumption}")

    weekly_rows = extract_markdown_table_after(text, "## Weekly Workload Budget")
    seen_weeks = set()
    for cells in weekly_rows[1:]:
        if len(cells) != 9:
            issues.append(f"weekly workload row expected 9 cells, got {len(cells)}: {cells[:2]}")
            continue
        week, topic, lecture_hours, reading_hours, assignment_hours, recitation_hours, project_hours, total_target, pacing_note = cells
        seen_weeks.add(week)
        if not topic or not pacing_note:
            issues.append(f"{week}: missing topic or pacing note")
        numeric_parts = [lecture_hours, reading_hours, assignment_hours, recitation_hours, project_hours, total_target]
        try:
            parsed = [float(part) for part in numeric_parts]
        except ValueError:
            issues.append(f"{week}: workload hours are not numeric: {numeric_parts}")
            continue
        computed_total = sum(parsed[:5])
        if abs(computed_total - parsed[5]) > 0.05:
            issues.append(f"{week}: total target {parsed[5]} does not match components {computed_total}")
        if not (8.0 <= parsed[5] <= 13.0):
            issues.append(f"{week}: total target outside 8-13 hour range: {parsed[5]}")
    for index in range(1, 11):
        if f"Week {index}" not in seen_weeks:
            issues.append(f"workload budget missing Week {index}")

    ladder_rows = extract_markdown_table_after(text, "## Difficulty Ladder")
    ladder_levels = {cells[0] for cells in ladder_rows[1:] if cells}
    for level in ["D1 Foundations", "D2 Architecture", "D3 Optimization and generation", "D4 Evaluation and systems", "D5 Synthesis"]:
        if level not in ladder_levels:
            issues.append(f"workload difficulty ladder missing level: {level}")
    for cells in ladder_rows[1:]:
        if len(cells) != 4:
            issues.append(f"difficulty ladder row expected 4 cells, got {len(cells)}: {cells[:2]}")
            continue
        if "tests" not in cells[3] and "capstone" not in cells[3]:
            issues.append(f"{cells[0]} evidence should reference tests or capstone")

    guardrail_rows = extract_markdown_table_after(text, "## Assignment Load Guardrails")
    guardrails = {cells[0] for cells in guardrail_rows[1:] if cells}
    for guardrail in [
        "Public test runtime",
        "Starter scope",
        "Written questions",
        "Hidden test category count",
        "Capstone overlap",
        "Reading density",
    ]:
        if guardrail not in guardrails:
            issues.append(f"workload guardrails missing: {guardrail}")

    overload_rows = extract_markdown_table_after(text, "## Overload Signals and Pacing Actions")
    overload_signals = {cells[0] for cells in overload_rows[1:] if cells}
    for signal in [
        "workload_over_13h",
        "public_test_blocker",
        "written_low_cluster",
        "project_scope_risk",
        "reading_recap_gap",
        "regrade_spike",
    ]:
        if signal not in overload_signals:
            issues.append(f"workload overload signals missing: {signal}")
    for cells in overload_rows[1:]:
        if len(cells) != 4:
            issues.append(f"overload signal row expected 4 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not all(cells[1:]):
            issues.append(f"{cells[0]} has empty overload action field")

    expansion_rows = extract_markdown_table_after(text, "## 10-to-12 Week Expansion Map")
    if len(expansion_rows) < 5:
        issues.append(f"expected at least 4 expansion rows, got {max(0, len(expansion_rows) - 1)}")
    for pressure_marker in ["Week 3", "Week 7", "Week 8", "Week 10"]:
        if pressure_marker not in text:
            issues.append(f"workload expansion map missing pressure point: {pressure_marker}")

    for template_marker in [
        "Lecture preparation hours:",
        "Programming hours:",
        "First blocker:",
        "What I will move to office hours:",
    ]:
        if template_marker not in text:
            issues.append(f"workload student planning template missing: {template_marker}")

    for doc_path in [
        "README.md",
        "docs/syllabus.md",
        "docs/course-calendar-deadline-ledger.md",
        "docs/assignment-handout-pack.md",
        "docs/reading-list.md",
        "docs/recitation-worksheet-pack.md",
        "docs/learning-analytics-remediation-plan.md",
        "docs/course-operations-log.md",
    ]:
        if "workload-pacing-calibration.md" not in read(doc_path):
            issues.append(f"{doc_path} missing workload pacing calibration link")

    if issues:
        fail(f"workload and pacing calibration is incomplete: {'; '.join(issues[:10])}")
    ok("workload and pacing calibration covers weekly budgets, difficulty ladder, guardrails, overload actions, and expansion path")


def check_material_versioning_archive_policy() -> None:
    text = read("docs/material-versioning-archive-policy.md")
    issues = []

    for status in ("current", "release-candidate", "archived", "retired", "instructor-only"):
        if f"| {status} |" not in text:
            issues.append(f"missing material status row: {status}")

    for material_type in (
        "HTML 章节",
        "作业包",
        "Slides / notes",
        "Demo / notebook",
        "项目报告样例",
        "外部链接与论文",
    ):
        if f"| {material_type} |" not in text:
            issues.append(f"missing material type rule: {material_type}")

    required_fields = (
        "material_id",
        "status",
        "release_date",
        "audience",
        "source_files",
        "validation",
        "change_summary",
        "replacement",
    )
    for field in required_fields:
        if f"| {field} |" not in text and f"| {field} " not in text:
            issues.append(f"missing version record field: {field}")

    for required_phrase in (
        "不作为本轮课程评分依据",
        "不得作为本轮作业、quiz、项目或评分依据",
        "scripts/build_course_site_release.py",
        "SITE_RELEASE_MANIFEST.json",
        "RELEASE_MANIFEST.json",
        "reference_solution.py",
        "隐藏测试",
        ".venv/bin/python verify_course.py --capstone --training",
    ):
        if required_phrase not in text:
            issues.append(f"missing archive policy phrase: {required_phrase}")

    if issues:
        fail(f"material versioning/archive policy is incomplete: {'; '.join(issues[:10])}")
    ok("material versioning/archive policy covers current, archived, retired, release, and instructor-only boundaries")


def check_lecture_notes_quality_review() -> None:
    text = read("docs/lecture-notes-quality-review.md")
    issues = []

    for material_type in (
        "HTML chapter used as notes",
        "Markdown handout",
        "slide outline",
        "board derivation script",
        "external lecture notes",
        "recording transcript / summary",
    ):
        if f"| {material_type} |" not in text:
            issues.append(f"missing lecture-notes material row: {material_type}")

    for rubric_dimension in (
        "Learning goals",
        "Notation ledger",
        "Derivation completeness",
        "Shape and units",
        "Code binding",
        "Source boundary",
        "Misconception coverage",
        "Accessibility",
        "Correction path",
    ):
        if f"| {rubric_dimension} |" not in text:
            issues.append(f"missing lecture-notes quality rubric row: {rubric_dimension}")

    for check_id in (
        "notation_consistency",
        "derivation_steps",
        "shape_invariants",
        "code_binding",
        "source_boundary",
        "misconception_link",
        "accessibility_asset",
        "release_status",
        "correction_path",
    ):
        if f"| {check_id} |" not in text:
            issues.append(f"missing per-lecture review check: {check_id}")

    for record_field in (
        "lecture_id",
        "material_id",
        "reviewer",
        "review_date",
        "status",
        "notation_checked",
        "derivation_checked",
        "code_binding_checked",
        "source_boundary_checked",
        "accessibility_checked",
        "affected_materials",
        "change_summary",
        "verification_command",
    ):
        if f"| {record_field} |" not in text:
            issues.append(f"missing lecture-notes review record field: {record_field}")

    for trigger in (
        "公式符号错误",
        "shape 或代码绑定错误",
        "来源事实变化",
        "可访问性缺口",
        "录播或课堂口误",
        "作业解释歧义",
    ):
        if f"| {trigger} |" not in text:
            issues.append(f"missing correction workflow trigger: {trigger}")

    for lecture_range in (
        "L1-L2",
        "L3-L6",
        "L7-L10",
        "L11-L14",
        "L15-L16",
        "L17-L18",
        "L19-L20",
    ):
        if f"| {lecture_range} |" not in text:
            issues.append(f"missing evidence matrix lecture range: {lecture_range}")

    for required_phrase in (
        "可审稿、可修订、可追溯",
        "前沿模型和 benchmark claim 不写成未复核事实",
        "instructor-only notes、隐藏测试、评分校准和 reference solution 不进入学生站点发布包",
        ".venv/bin/python verify_course.py --capstone --training",
        "review_record",
    ):
        if required_phrase not in text:
            issues.append(f"missing lecture-notes quality phrase: {required_phrase}")

    for linked_doc in (
        "lecture-notes-index.md",
        "lecture-slide-outline.md",
        "board-derivation-pack.md",
        "demo-runbook.md",
        "course-materials-index.md",
        "chapter-source-map.md",
        "external-source-verification.md",
        "concept-misconception-map.md",
        "material-versioning-archive-policy.md",
    ):
        if linked_doc not in text:
            issues.append(f"lecture-notes quality review missing linked doc: {linked_doc}")

    notes_index = read("docs/lecture-notes-index.md")
    for notes_marker in (
        "Lecture Notes Quality and Review Standard",
        "review_record",
        "notation_checked",
        "source_boundary_checked",
    ):
        if notes_marker not in notes_index:
            issues.append(f"lecture notes index missing quality-review marker: {notes_marker}")

    slide_outline = read("docs/lecture-slide-outline.md")
    for slide_marker in (
        "Lecture Notes Quality and Review Standard",
        "reviewed notes",
        "review_record",
    ):
        if slide_marker not in slide_outline:
            issues.append(f"lecture slide outline missing quality-review marker: {slide_marker}")

    materials_index = read("docs/course-materials-index.md")
    for materials_marker in (
        "Lecture Notes Quality and Review Standard",
        "lecture notes quality review",
        "review record",
        "2026-06-05 | lecture notes quality review",
    ):
        if materials_marker not in materials_index:
            issues.append(f"course materials index missing lecture-notes quality marker: {materials_marker}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for snapshot_marker in (
        "| Lecture notes / slides |",
        "Lecture Notes Quality and Review Standard",
        "review_record",
        "source_boundary",
        "correction workflow",
    ):
        if snapshot_marker not in snapshot:
            issues.append(f"CS224N snapshot missing lecture-notes quality marker: {snapshot_marker}")

    crosswalk = read("docs/cs224n-benchmark-crosswalk.md")
    for crosswalk_marker in (
        "Schedule and lecture slides / notes",
        "Lecture Notes Quality and Review Standard",
        "review record",
        "correction workflow",
    ):
        if crosswalk_marker not in crosswalk:
            issues.append(f"CS224N crosswalk missing lecture-notes quality marker: {crosswalk_marker}")

    if issues:
        fail(f"lecture notes quality review is incomplete: {'; '.join(issues[:10])}")
    ok("lecture notes quality review covers reviewed notes, notation, derivations, source boundaries, corrections, and evidence")


def check_lecture_notes_review_ledger() -> None:
    ledger = read("docs/lecture-notes-review-ledger.md")
    issues = []

    for heading in [
        "Review Ledger",
        "Review Exceptions and Follow-Up",
        "Evidence Requirements",
        "发布前 Checklist",
    ]:
        markdown_section(ledger, heading)

    rows = extract_markdown_table_after(ledger, "## Review Ledger")
    if len(rows) != 21:
        issues.append(f"expected review ledger header plus 20 lecture rows, got {len(rows)}")

    expected_lectures = {f"L{index}" for index in range(1, 21)}
    seen_lectures: set[str] = set()
    check_columns = {
        "notation_checked": 5,
        "derivation_checked": 6,
        "code_binding_checked": 7,
        "source_boundary_checked": 8,
        "accessibility_checked": 9,
    }
    capstone_lectures = {"L10", "L18", "L19", "L20"}

    for cells in rows[1:]:
        if len(cells) != 13:
            issues.append(f"lecture review row expected 13 cells, got {len(cells)}: {cells[:2]}")
            continue
        lecture_id = cells[0]
        material_id = cells[1]
        status = cells[4]
        command = cells[12]
        if lecture_id not in expected_lectures:
            issues.append(f"unexpected lecture id in review ledger: {lecture_id}")
            continue
        if lecture_id in seen_lectures:
            issues.append(f"duplicate lecture id in review ledger: {lecture_id}")
        seen_lectures.add(lecture_id)
        if not material_id:
            issues.append(f"{lecture_id}: missing material_id")
        if status != "ready":
            issues.append(f"{lecture_id}: expected ready status, got {status!r}")
        for field, index in check_columns.items():
            if cells[index] != "Yes":
                issues.append(f"{lecture_id}: {field} must be Yes, got {cells[index]!r}")
        if ".venv/bin/python verify_course.py" not in command:
            issues.append(f"{lecture_id}: verification command must use .venv verify_course.py")
        if lecture_id in capstone_lectures and "--capstone --training" not in command:
            issues.append(f"{lecture_id}: capstone lecture must use --capstone --training verification")

    missing_lectures = expected_lectures - seen_lectures
    if missing_lectures:
        issues.append(f"missing lecture review rows: {', '.join(sorted(missing_lectures))}")

    exception_rows = extract_markdown_table_after(ledger, "## Review Exceptions and Follow-Up")
    if not any(cells and cells[0] == "none-current" for cells in exception_rows[1:]):
        issues.append("review exceptions table must include none-current row")

    for check_id in (
        "notation_checked",
        "derivation_checked",
        "code_binding_checked",
        "source_boundary_checked",
        "accessibility_checked",
    ):
        if f"| {check_id} |" not in ledger:
            issues.append(f"evidence requirements missing check id: {check_id}")

    for doc_path in [
        "README.md",
        "docs/lecture-notes-index.md",
        "docs/lecture-notes-quality-review.md",
    ]:
        if "lecture-notes-review-ledger.md" not in read(doc_path):
            issues.append(f"{doc_path} missing lecture notes review ledger link")

    if issues:
        fail(f"lecture notes review ledger is incomplete: {'; '.join(issues[:10])}")
    ok("lecture notes review ledger covers L1-L20 ready records, review checks, evidence, and verification commands")


def check_lecture_note_sample_pack() -> None:
    text = read("docs/lecture-note-sample-pack.md")
    issues = []

    for marker in [
        "Lecture Note Sample Pack",
        "复核日期：2026-06-05",
        "Sample Packet Rubric",
        "TA Review Checklist",
        "Release Checklist",
        "lecture-notes-index.md",
        "lecture-notes-quality-review.md",
        "lecture-notes-review-ledger.md",
        "mathematical-derivation-audit.md",
        "paper-recap-calibration-pack.md",
    ]:
        if marker not in text:
            issues.append(f"missing lecture note sample marker: {marker}")

    required_fields = [
        "Learning goals",
        "Notation ledger",
        "Core derivation",
        "Shape checks",
        "Code binding",
        "Common misconceptions",
        "Source boundary",
        "Accessibility notes",
        "Quick check",
        "Post-lecture evidence",
    ]
    rubric_rows = extract_markdown_table_after(text, "## Sample Packet Rubric")
    rubric_fields = {cells[0] for cells in rubric_rows[1:] if cells}
    for field in required_fields:
        if field not in rubric_fields:
            issues.append(f"lecture note sample rubric missing field: {field}")

    sample_specs = [
        ("Sample L1: Tokenization and BPE", "DER-01", "assignments/ch01_bpe/tests.py"),
        ("Sample L3: Scaled Dot-Product Attention", "DER-04", "assignments/ch03_attention/tests.py"),
        ("Sample L9: Cross Entropy and AdamW", "DER-09", "assignments/ch07_training/tests.py"),
        ("Sample L18: Serving SLO and Capacity", "DER-13", "assignments/ch10_inference/tests.py"),
    ]
    for heading, derivation_id, test_path in sample_specs:
        section = markdown_section(text, heading)
        for field in required_fields:
            if f"{field}:" not in section:
                issues.append(f"{heading} missing field: {field}")
        if derivation_id not in section:
            issues.append(f"{heading} missing derivation link: {derivation_id}")
        if test_path not in section:
            issues.append(f"{heading} missing assignment test binding: {test_path}")
        for boundary_marker in ("does not", "不", "not"):
            if boundary_marker in section:
                break
        else:
            issues.append(f"{heading} missing explicit boundary language")
        if ".venv/bin/python" not in section and "capstone acceptance" not in section:
            issues.append(f"{heading} missing executable command or capstone acceptance evidence")

    checklist = markdown_section(text, "TA Review Checklist")
    for checklist_marker in [
        "Four representative notes",
        "Field completeness",
        "Course binding",
        "Boundary control",
        "Student usability",
    ]:
        if checklist_marker not in checklist:
            issues.append(f"lecture note TA checklist missing marker: {checklist_marker}")

    for doc_path in [
        "README.md",
        "docs/lecture-notes-index.md",
        "docs/lecture-notes-quality-review.md",
    ]:
        if "lecture-note-sample-pack.md" not in read(doc_path):
            issues.append(f"{doc_path} missing lecture note sample pack link")

    if issues:
        fail(f"lecture note sample pack is incomplete: {'; '.join(issues[:10])}")
    ok("lecture note sample pack covers 4 representative notes with fields, evidence, and boundaries")


def check_lecture_note_core_pack() -> None:
    text = read("docs/lecture-note-core-pack.md")
    issues = []

    for marker in [
        "Lecture Note Core Pack",
        "复核日期：2026-06-05",
        "Coverage Contract",
        "TA Review Checklist",
        "Release Checklist",
        "lecture-notes-index.md",
        "lecture-note-sample-pack.md",
        "lecture-notes-quality-review.md",
        "lecture-notes-review-ledger.md",
        "mathematical-derivation-audit.md",
        "paper-to-code-traceability-matrix.md",
    ]:
        if marker not in text:
            issues.append(f"missing lecture note core marker: {marker}")

    required_fields = [
        "Learning goals",
        "Notation ledger",
        "Core derivation",
        "Shape checks",
        "Code binding",
        "Common misconceptions",
        "Source boundary",
        "Accessibility notes",
        "Quick check",
        "Post-lecture evidence",
    ]
    core_specs = [
        (
            "Core L2: Embedding, Analogy, and RoPE",
            ["assignments/ch02_embeddings/tests.py", "DER-02", "DER-03", "analogy", "RoPE"],
        ),
        (
            "Core L4: Causal Mask and Cross-Entropy Gradient",
            ["assignments/ch03_attention/tests.py", "assignments/ch07_training/tests.py", "DER-05", "DER-09"],
        ),
        (
            "Core L6: MHA, GQA, MLA, Norm, and Block Boundaries",
            ["assignments/ch04_multihead/tests.py", "assignments/ch05_block/tests.py", "GQA", "MLA", "Pre-Norm"],
        ),
        (
            "Core L12: Speculative Decoding, Constraints, and Frontier Source Boundaries",
            ["assignments/ch08_generation/tests.py", "scripts/verify_frontier_sources.py", "D-level", "monitor-only"],
        ),
        (
            "Core L15: Classic NLP, Encoder-Decoder, BERT, and Evaluation",
            ["assignments/ch11_classic_nlp/tests.py", "dependency parsing", "seq2seq", "BERT", "BLEU"],
        ),
    ]
    for heading, expected_markers in core_specs:
        section = markdown_section(text, heading)
        if not section:
            issues.append(f"missing lecture note core section: {heading}")
            continue
        for field in required_fields:
            if f"{field}:" not in section:
                issues.append(f"{heading} missing field: {field}")
        section_lower = section.lower()
        for expected_marker in expected_markers:
            if expected_marker.lower() not in section_lower:
                issues.append(f"{heading} missing expected marker: {expected_marker}")
        boundary_hits = sum(section.count(marker) for marker in ["does not", "not ", "不能", "不等于", "不是", "false"])
        if boundary_hits < 2:
            issues.append(f"{heading} missing enough explicit boundary language")
        if ".venv/bin/python" not in section:
            issues.append(f"{heading} missing executable verification command")

    coverage_rows = extract_markdown_table_after(text, "## Coverage Contract")
    covered_lectures = {cells[0] for cells in coverage_rows[1:] if cells}
    for lecture in ["L2", "L4", "L6", "L12", "L15"]:
        if lecture not in covered_lectures:
            issues.append(f"coverage contract missing lecture: {lecture}")

    checklist = markdown_section(text, "TA Review Checklist")
    for checklist_marker in [
        "Field completeness",
        "Executable binding",
        "Boundary control",
        "CS224N alignment",
        "Source safety",
        "Student usability",
    ]:
        if checklist_marker not in checklist:
            issues.append(f"lecture note core TA checklist missing marker: {checklist_marker}")

    for doc_path in [
        "README.md",
        "docs/lecture-notes-index.md",
        "docs/course-materials-index.md",
        "docs/university-course-quality-audit.md",
    ]:
        if "lecture-note-core-pack.md" not in read(doc_path):
            issues.append(f"{doc_path} missing lecture note core pack link")

    if issues:
        fail(f"lecture note core pack is incomplete: {'; '.join(issues[:10])}")
    ok("lecture note core pack covers high-risk L2/L4/L6/L12/L15 notes with tests, boundaries, and source controls")


def check_notation_shape_glossary() -> None:
    text = read("docs/notation-shape-glossary.md")
    issues = []

    for marker in [
        "Notation and Shape Glossary",
        "复核日期：2026-06-05",
        "Global Symbols",
        "Module Shape Contracts",
        "Mask and Broadcast Rules",
        "Loss, Objective, and Optimizer Symbols",
        "Serving and Evaluation Units",
        "Disambiguation Rules",
        "Assessment Use",
        "Maintenance Workflow",
        "Release Checklist",
        "mathematical-derivation-audit.md",
        "worked-example-pack.md",
        "lecture-note-sample-pack.md",
        "recitation-worksheet-pack.md",
        "assessment-blueprint-coverage-matrix.md",
        "chapter-source-map.md",
        "assignment-handout-pack.md",
        ".venv/bin/python verify_course.py",
        "student site release",
    ]:
        if marker not in text:
            issues.append(f"missing notation/shape glossary marker: {marker}")

    global_rows = extract_markdown_table_after(text, "## Global Symbols")
    global_symbols = {cells[0] for cells in global_rows[1:] if cells}
    for symbol in ["B", "T", "S", "V", "D", "H", "H_kv", "D_h", "L", "K", "E", "logits", "labels", "mask", "dtype_bytes"]:
        if symbol not in global_symbols:
            issues.append(f"notation glossary missing global symbol: {symbol}")
    for cells in global_rows[1:]:
        if len(cells) != 4:
            issues.append(f"global symbol row expected 4 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[1] or not cells[2]:
            issues.append(f"{cells[0]} missing meaning or shape/unit")

    contract_rows = extract_markdown_table_after(text, "## Module Shape Contracts")
    contract_ids = {cells[0] for cells in contract_rows[1:] if cells}
    for contract_id in [f"NS-{index:02d}" for index in range(1, 16)]:
        if contract_id not in contract_ids:
            issues.append(f"notation glossary missing shape contract: {contract_id}")
    for cells in contract_rows[1:]:
        if len(cells) != 5:
            issues.append(f"shape contract row expected 5 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[2] or not cells[3] or not cells[4]:
            issues.append(f"{cells[0]} missing input shape, output shape, or invariant")

    mask_rows = extract_markdown_table_after(text, "## Mask and Broadcast Rules")
    mask_ids = {cells[0] for cells in mask_rows[1:] if cells}
    for rule_id in ["MASK-CAUSAL", "MASK-ADDITIVE", "MASK-BOOLEAN", "MASK-BROADCAST", "MASK-PADDING", "MASK-LABEL"]:
        if rule_id not in mask_ids:
            issues.append(f"notation glossary missing mask rule: {rule_id}")

    loss_rows = extract_markdown_table_after(text, "## Loss, Objective, and Optimizer Symbols")
    loss_symbols = {cells[0] for cells in loss_rows[1:] if cells}
    for symbol in ["y", "log p_theta", "CE", "ppl", "lr", "beta_1, beta_2", "weight_decay", "beta_dpo", "A_lora, B_lora", "advantage"]:
        if symbol not in loss_symbols:
            issues.append(f"notation glossary missing loss/objective symbol: {symbol}")

    unit_rows = extract_markdown_table_after(text, "## Serving and Evaluation Units")
    unit_symbols = {cells[0] for cells in unit_rows[1:] if cells}
    for symbol in ["TTFT", "TPOT", "TPS", "P50/P95/P99", "error_rate", "memory", "cost", "UAS", "LAS", "BLEU / ROUGE-L", "EM / F1"]:
        if symbol not in unit_symbols:
            issues.append(f"notation glossary missing serving/evaluation unit: {symbol}")

    disambiguation_rows = extract_markdown_table_after(text, "## Disambiguation Rules")
    if len(disambiguation_rows) < 8:
        issues.append(f"expected at least 7 disambiguation rules plus header, got {len(disambiguation_rows)}")
    for ambiguity in ["`L` could mean layers or loss.", "`K` could mean keys or top-k.", "`beta` could mean Adam beta or DPO beta.", "metric values can be percent or ratio."]:
        if ambiguity not in text:
            issues.append(f"notation glossary missing ambiguity rule: {ambiguity}")

    assessment_rows = extract_markdown_table_after(text, "## Assessment Use")
    assessment_uses = {cells[0] for cells in assessment_rows[1:] if cells}
    for use_case in ["written derivation", "programming assignment", "recitation worksheet", "paper recap", "capstone report", "regrade request"]:
        if use_case not in assessment_uses:
            issues.append(f"notation glossary missing assessment use case: {use_case}")

    for workflow_marker in ["new symbol", "shape contract", "mask bug", "metric or SLO", "unit", "boundary"]:
        if workflow_marker not in text:
            issues.append(f"notation glossary maintenance workflow missing marker: {workflow_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/mathematical-derivation-audit.md",
        "docs/worked-example-pack.md",
        "docs/lecture-note-sample-pack.md",
        "docs/recitation-worksheet-pack.md",
        "docs/assessment-blueprint-coverage-matrix.md",
        "docs/assignment-handout-pack.md",
        "docs/chapter-source-map.md",
        "docs/university-course-quality-audit.md",
    ]
    for doc_path in linked_docs:
        if "notation-shape-glossary.md" not in read(doc_path):
            issues.append(f"{doc_path} missing notation/shape glossary link")

    if "notation-shape-glossary.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing notation/shape glossary")
    if "docs/notation-shape-glossary.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing notation/shape glossary")

    if issues:
        fail(f"notation/shape glossary is incomplete: {'; '.join(issues[:10])}")
    ok("notation/shape glossary covers global symbols, shape contracts, masks, objectives, units, disambiguation, assessment use, and release links")


def check_worked_example_pack() -> None:
    text = read("docs/worked-example-pack.md")
    derivation_audit = read("docs/mathematical-derivation-audit.md")
    issues = []

    for marker in [
        "Worked Example Pack",
        "复核日期：2026-06-05",
        "Example Schema",
        "Core Worked Examples",
        "Recitation Use",
        "Assessment Coverage",
        "Maintenance Workflow",
        "Release Checklist",
        "lecture-note-sample-pack.md",
        "recitation-worksheet-pack.md",
        "notation-shape-glossary.md",
        "mathematical-derivation-audit.md",
        "chapter-claim-audit-ledger.md",
        "assignment-handout-pack.md",
        "written-problem-set.md",
        "paper-to-code-traceability-matrix.md",
        "external-source-verification.md",
        "frontier-source-audit.md",
        ".venv/bin/python verify_course.py",
        "student site release",
    ]:
        if marker not in text:
            issues.append(f"missing worked example marker: {marker}")

    schema_rows = extract_markdown_table_after(text, "## Example Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    for field in [
        "example_id",
        "chapter",
        "learning target",
        "inputs and shapes",
        "worked trace",
        "common failure",
        "assessment link",
        "source boundary",
    ]:
        if field not in schema_fields:
            issues.append(f"worked example schema missing field: {field}")

    core_rows = extract_markdown_table_after(text, "## Core Worked Examples")
    if len(core_rows) != 12:
        issues.append(f"expected 11 core worked example rows plus header, got {len(core_rows)}")
    core_ids = {cells[0] for cells in core_rows[1:] if cells}
    for example_id in [
        "WE-CH01-BPE",
        "WE-CH02-ROPE",
        "WE-CH03-ATTN",
        "WE-CH04-GQA",
        "WE-CH05-NORM",
        "WE-CH06-PARAMS",
        "WE-CH07-ADAMW",
        "WE-CH08-TOPP",
        "WE-CH09-DPO",
        "WE-CH10-KVCACHE",
        "WE-CH11-METRICS",
    ]:
        if example_id not in core_ids:
            issues.append(f"worked example pack missing core example: {example_id}")
    for cells in core_rows[1:]:
        if len(cells) != 8:
            issues.append(f"worked example row expected 8 cells, got {len(cells)}: {cells[:2]}")
            continue
        example_id = cells[0]
        assessment_link = cells[6]
        if not cells[4] or not cells[5] or not cells[6] or not cells[7]:
            issues.append(f"{cells[0]} missing worked trace, common failure, assessment link, or source boundary")
        if "assignments/" not in cells[6] and "capstone" not in cells[6] and "handout" not in cells[6]:
            issues.append(f"{cells[0]} assessment link does not bind to assignment/capstone/handout evidence")
        for assignment_dir in re.findall(r"`(assignments/[^`]+/)`", assessment_link):
            if not (ROOT / assignment_dir).is_dir():
                issues.append(f"{example_id} assignment directory does not exist: {assignment_dir}")
        for der_id in re.findall(r"\bDER-\d{2}\b", assessment_link):
            if not re.search(rf"\|\s*{re.escape(der_id)}\s*\|", derivation_audit):
                issues.append(f"{example_id} references unknown derivation id: {der_id}")

    expected_example_derivations = {
        "WE-CH02-ROPE": "DER-03",
        "WE-CH03-ATTN": "DER-04",
        "WE-CH05-NORM": "DER-07",
        "WE-CH07-ADAMW": "DER-10",
        "WE-CH09-DPO": "DER-12",
    }
    example_links = {cells[0]: cells[6] for cells in core_rows[1:] if len(cells) == 8}
    for example_id, der_id in expected_example_derivations.items():
        if der_id not in example_links.get(example_id, ""):
            issues.append(f"{example_id} must link to {der_id}")

    recitation_rows = extract_markdown_table_after(text, "## Recitation Use")
    recitation_ids = {cells[0] for cells in recitation_rows[1:] if cells}
    for recitation_id in ["WE-R1-SHAPE", "WE-R2-SYSTEMS", "WE-R3-OBJECTIVES", "WE-R4-EVAL"]:
        if recitation_id not in recitation_ids:
            issues.append(f"worked example pack missing recitation use row: {recitation_id}")

    coverage_rows = extract_markdown_table_after(text, "## Assessment Coverage")
    coverage_channels = {cells[0] for cells in coverage_rows[1:] if cells}
    for channel in ["programming assignments", "written assessment", "recitation", "quiz/checkpoint", "paper recap"]:
        if channel not in coverage_channels:
            issues.append(f"worked example pack missing assessment coverage channel: {channel}")

    for workflow_marker in [
        "chapter formula",
        "starter API",
        "assignment test",
        "source boundary",
        "source audit",
    ]:
        if workflow_marker not in text:
            issues.append(f"worked example maintenance workflow missing marker: {workflow_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/lecture-note-sample-pack.md",
        "docs/recitation-worksheet-pack.md",
        "docs/assignment-handout-pack.md",
        "docs/written-problem-set.md",
        "docs/paper-to-code-traceability-matrix.md",
        "docs/mathematical-derivation-audit.md",
        "docs/chapter-claim-audit-ledger.md",
        "docs/university-course-quality-audit.md",
    ]
    for doc_path in linked_docs:
        if "worked-example-pack.md" not in read(doc_path):
            issues.append(f"{doc_path} missing worked example pack link")

    if "worked-example-pack.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing worked example pack")
    if "docs/worked-example-pack.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing worked example pack")

    if issues:
        fail(f"worked example pack is incomplete: {'; '.join(issues[:10])}")
    ok("worked example pack covers 11 core examples, schema, recitation use, assessment coverage, workflow, and release links")


def check_lecture_slide_sample_pack() -> None:
    text = read("docs/lecture-slide-sample-pack.md")
    issues = []

    for marker in [
        "Lecture Slide Sample Pack",
        "复核日期：2026-06-05",
        "Slide Sample Rubric",
        "Deck Accessibility Checklist",
        "Release Checklist",
        "lecture-slide-outline.md",
        "lecture-note-sample-pack.md",
        "lecture-notes-quality-review.md",
        "course-materials-index.md",
        "demo-runbook.md",
        "recitation-worksheet-pack.md",
        "paper-to-code-traceability-matrix.md",
    ]:
        if marker not in text:
            issues.append(f"missing lecture slide sample marker: {marker}")

    required_fields = [
        "Deck metadata",
        "Learning goals",
        "Slide sequence",
        "Visual plan",
        "Speaker note",
        "Accessibility text",
        "Source boundary",
        "Quick check",
        "Post-lecture evidence",
    ]
    rubric_rows = extract_markdown_table_after(text, "## Slide Sample Rubric")
    rubric_fields = {cells[0] for cells in rubric_rows[1:] if cells}
    for field in required_fields:
        if field not in rubric_fields:
            issues.append(f"lecture slide sample rubric missing field: {field}")

    deck_specs = [
        ("Sample Deck S1: L2 Embeddings, Word Vectors, RoPE", "assignments/ch02_embeddings", ["DER-02", "DER-03"]),
        ("Sample Deck S2: L5 Multi-Head Attention and GQA", "assignments/ch04_multihead", ["DER-06", "P2C-05"]),
        ("Sample Deck S3: L10 Training Loop, Checkpoint, Scaling", "assignments/ch07_training", ["DER-10", "training capstone"]),
        ("Sample Deck S4: L18 Serving, Benchmark, SLO, Capacity", "assignments/ch10_inference", ["DER-13", "inference capstone"]),
    ]
    for heading, assignment_marker, evidence_markers in deck_specs:
        section = markdown_section(text, heading)
        for required_marker in [
            "Deck metadata:",
            "Learning goals:",
            "Slide sequence:",
            "Source boundary:",
            "Post-lecture evidence:",
        ]:
            if required_marker not in section:
                issues.append(f"{heading} missing required marker: {required_marker}")
        if assignment_marker not in section:
            issues.append(f"{heading} missing assignment marker: {assignment_marker}")
        for evidence_marker in evidence_markers:
            if evidence_marker not in section:
                issues.append(f"{heading} missing evidence marker: {evidence_marker}")

        slide_rows = extract_markdown_table_after(section, "Slide sequence:")
        slide_count = max(0, len(slide_rows) - 1)
        if not (8 <= slide_count <= 12):
            issues.append(f"{heading} expected 8-12 slide rows, got {slide_count}")
        for cells in slide_rows[1:]:
            if len(cells) != 5:
                issues.append(f"{heading} slide row expected 5 cells, got {len(cells)}: {cells[:2]}")
                continue
            if not all(cells):
                issues.append(f"{heading} has empty slide row field: {cells[:2]}")
        if "does not" not in section and "do not" not in section and "不" not in section:
            issues.append(f"{heading} missing explicit source boundary language")
        if "Quick check" not in section:
            issues.append(f"{heading} missing quick check slide or field")

    accessibility_rows = extract_markdown_table_after(text, "## Deck Accessibility Checklist")
    accessibility_checks = {cells[0] for cells in accessibility_rows[1:] if cells}
    for check in [
        "Text alternative",
        "Formula readability",
        "Color independence",
        "Demo fallback",
        "Source boundary",
        "Student evidence",
    ]:
        if check not in accessibility_checks:
            issues.append(f"lecture slide accessibility checklist missing: {check}")

    for unsafe_marker in [
        "hidden-test input",
        "hidden test input",
        "private grading key",
        "reference implementation appears",
    ]:
        if unsafe_marker in text:
            issues.append(f"lecture slide sample pack contains unsafe marker: {unsafe_marker}")

    for doc_path in [
        "README.md",
        "docs/lecture-slide-outline.md",
        "docs/course-materials-index.md",
        "docs/lecture-notes-quality-review.md",
        "docs/lecture-note-sample-pack.md",
    ]:
        if "lecture-slide-sample-pack.md" not in read(doc_path):
            issues.append(f"{doc_path} missing lecture slide sample pack link")

    if issues:
        fail(f"lecture slide sample pack is incomplete: {'; '.join(issues[:10])}")
    ok("lecture slide sample pack covers 4 representative decks with slide sequence, accessibility, evidence, and boundaries")


def check_recitation_worksheet_pack() -> None:
    text = read("docs/recitation-worksheet-pack.md")
    issues = []

    for marker in [
        "Recitation Worksheet Pack",
        "复核日期：2026-06-05",
        "Worksheet Schema",
        "Staff Feedback Rubric",
        "Release Checklist",
        "discussion-office-hours-guide.md",
        "concept-misconception-map.md",
        "paper-to-code-traceability-matrix.md",
        "mathematical-derivation-audit.md",
        "assignment-handout-pack.md",
        "participation-feedback-guide.md",
    ]:
        if marker not in text:
            issues.append(f"missing recitation worksheet marker: {marker}")

    schema_rows = extract_markdown_table_after(text, "## Worksheet Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    for field in [
        "learning_goal",
        "shape_table",
        "failure_hypothesis",
        "paper_to_code_link",
        "source_boundary",
        "exit_ticket",
    ]:
        if field not in schema_fields:
            issues.append(f"recitation worksheet schema missing field: {field}")

    worksheet_specs = [
        ("Worksheet W1: BPE, Embedding, RoPE", ["assignments/ch01_bpe", "assignments/ch02_embeddings"], ["DER-01", "DER-02", "DER-03"]),
        ("Worksheet W2: Attention and Masking", ["assignments/ch03_attention"], ["DER-04", "DER-05"]),
        ("Worksheet W3: MHA, GQA, Norm, FFN", ["assignments/ch04_multihead", "assignments/ch05_block"], ["DER-06", "DER-07"]),
        ("Worksheet W4: GPT, Training, Decoding, Alignment", ["assignments/ch06_gpt", "assignments/ch07_training", "assignments/ch08_generation", "assignments/ch09_alignment"], ["DER-08", "DER-09", "DER-10", "DER-11", "DER-12", "DER-14"]),
        ("Worksheet W5: Inference, RAG, Evaluation", ["assignments/ch10_inference", "assignments/ch11_classic_nlp"], ["DER-13", "DER-14"]),
        ("Worksheet W6: Capstone Rehearsal and Source Audit", ["training capstone", "inference capstone"], ["Project Report Template", "Experimental Rigor"]),
    ]
    for heading, assignment_markers, evidence_markers in worksheet_specs:
        section = markdown_section(text, heading)
        if not section:
            issues.append(f"missing recitation worksheet section: {heading}")
            continue
        for required_marker in [
            "Learning goal:",
            "Shape table:",
            "Activity:",
            "Failure drill:",
            "Paper-to-code link:",
            "Exit ticket:",
        ]:
            if required_marker not in section:
                issues.append(f"{heading} missing required marker: {required_marker}")
        for assignment_marker in assignment_markers:
            if assignment_marker not in section:
                issues.append(f"{heading} missing assignment/capstone marker: {assignment_marker}")
        for evidence_marker in evidence_markers:
            if evidence_marker not in section:
                issues.append(f"{heading} missing evidence marker: {evidence_marker}")
        if "does not" not in section and "do not" not in section and "不" not in section:
            issues.append(f"{heading} missing explicit source boundary")

        shape_rows = extract_markdown_table_after(section, "Shape table:")
        if len(shape_rows) < 3:
            issues.append(f"{heading} shape table has too few rows")
        failure_rows = extract_markdown_table_after(section, "Failure drill:")
        if len(failure_rows) < 3:
            issues.append(f"{heading} failure drill has too few rows")

    for marker in [
        "assignments/ch01_bpe",
        "assignments/ch02_embeddings",
        "assignments/ch03_attention",
        "assignments/ch04_multihead",
        "assignments/ch05_block",
        "assignments/ch07_training",
        "assignments/ch08_generation",
        "assignments/ch09_alignment",
        "assignments/ch10_inference",
        "assignments/ch11_classic_nlp",
    ]:
        if marker not in text:
            issues.append(f"recitation worksheet pack missing assignment coverage: {marker}")
    if "assignments/ch06_gpt" not in text:
        issues.append("recitation worksheet pack missing Ch06/GPT assignment coverage")

    for der_id in [f"DER-{index:02d}" for index in range(1, 15)]:
        if der_id not in text:
            issues.append(f"recitation worksheet pack missing DER coverage: {der_id}")

    for unsafe_marker in [
        "reference_solution.py",
        "hidden test input",
        "hidden-test input",
        "private grading key",
    ]:
        if unsafe_marker in text:
            issues.append(f"recitation worksheet pack contains unsafe student-facing marker: {unsafe_marker}")

    for doc_path in [
        "README.md",
        "docs/syllabus.md",
        "docs/participation-feedback-guide.md",
        "docs/course-materials-index.md",
        "docs/discussion-office-hours-guide.md",
    ]:
        if "recitation-worksheet-pack.md" not in read(doc_path):
            issues.append(f"{doc_path} missing recitation worksheet pack link")

    if issues:
        fail(f"recitation worksheet pack is incomplete: {'; '.join(issues[:10])}")
    ok("recitation worksheet pack covers 6 worksheets with shape, failure, paper-to-code, exit-ticket, and boundary evidence")


def check_assessment_item_bank_ledger() -> None:
    text = read("docs/assessment-item-bank-ledger.md")
    issues = []

    for marker in [
        "Assessment Item Bank Ledger",
        "复核日期：2026-06-05",
        "Exposure Levels",
        "Item Metadata Schema",
        "Public-Safe Item Bank",
        "Rotation Procedure",
        "Equivalence and Makeup Rules",
        "Release Checklist",
        "quiz-checkpoint-guide.md",
        "midterm-final-review-pack.md",
        "assessment-administration-policy.md",
        "course-calendar-deadline-ledger.md",
        "gradebook-lms-operations.md",
        "course-operations-log.md",
    ]:
        if marker not in text:
            issues.append(f"missing assessment item bank marker: {marker}")

    exposure_rows = extract_markdown_table_after(text, "## Exposure Levels")
    exposure_levels = {cells[0] for cells in exposure_rows[1:] if cells}
    for level in ["public_sample", "practice_variant", "active_assessment", "retired"]:
        if level not in exposure_levels:
            issues.append(f"assessment item bank missing exposure level: {level}")

    schema_rows = extract_markdown_table_after(text, "## Item Metadata Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    for field in [
        "item_bank_id",
        "assessment_type",
        "learning_objective",
        "source_material",
        "exposure_level",
        "variant_policy",
        "evidence_required",
        "remediation_link",
        "retirement_trigger",
    ]:
        if field not in schema_fields:
            issues.append(f"assessment item bank schema missing field: {field}")

    rows = extract_markdown_table_after(text, "## Public-Safe Item Bank")
    if len(rows) < 11:
        issues.append(f"expected 10 item bank rows plus header, got {len(rows)}")
    seen_ids = set()
    seen_weeks = set()
    seen_types = set()
    seen_levels = set()
    for cells in rows[1:]:
        if len(cells) != 9:
            issues.append(f"assessment item row expected 9 cells, got {len(cells)}: {cells[:2]}")
            continue
        (
            item_id,
            assessment_type,
            learning_objective,
            source_material,
            exposure_level,
            variant_policy,
            evidence_required,
            remediation_link,
            retirement_trigger,
        ) = cells
        seen_ids.add(item_id)
        seen_types.add(assessment_type)
        seen_levels.add(exposure_level)
        week_match = re.search(r"QC-W(\d+)-", item_id)
        if week_match:
            seen_weeks.add(int(week_match.group(1)))
        for field_name, value in {
            "learning_objective": learning_objective,
            "source_material": source_material,
            "variant_policy": variant_policy,
            "evidence_required": evidence_required,
            "remediation_link": remediation_link,
            "retirement_trigger": retirement_trigger,
        }.items():
            if not value or value in {"-", "N/A"}:
                issues.append(f"{item_id} missing {field_name}")
        if exposure_level not in exposure_levels:
            issues.append(f"{item_id} has invalid exposure level: {exposure_level}")

    for expected_id in [
        "QC-W1-BPE-01",
        "QC-W2-MASK-01",
        "QC-W3-CACHE-01",
        "QC-W5-TRAIN-01",
        "QC-W6-SAMPLING-01",
        "QC-W7-DPO-01",
        "QC-W8-EVAL-01",
        "QC-W9-SLO-01",
        "QC-W10-SOURCE-01",
        "QC-MAKEUP-EQUIV-01",
    ]:
        if expected_id not in seen_ids:
            issues.append(f"missing assessment item bank id: {expected_id}")
    for week in [1, 2, 3, 5, 6, 7, 8, 9, 10]:
        if week not in seen_weeks:
            issues.append(f"assessment item bank missing week coverage: Week {week}")
    for assessment_type in ["lecture_quick_check", "recap_quiz", "midterm_checkpoint", "final_review_quiz", "capstone_readiness_check", "makeup_assessment"]:
        if assessment_type not in seen_types:
            issues.append(f"assessment item bank missing assessment type: {assessment_type}")
    for level in ["public_sample", "practice_variant", "active_assessment"]:
        if level not in seen_levels:
            issues.append(f"assessment item bank missing used exposure level: {level}")

    equivalence = markdown_section(text, "Equivalence and Makeup Rules")
    for scenario in ["illness / emergency makeup", "accommodation alternative", "remote oral check", "LMS outage", "integrity retake"]:
        if scenario not in equivalence:
            issues.append(f"assessment item bank missing equivalence scenario: {scenario}")

    for doc_path in [
        "README.md",
        "docs/syllabus.md",
        "docs/quiz-checkpoint-guide.md",
        "docs/assessment-administration-policy.md",
    ]:
        if "assessment-item-bank-ledger.md" not in read(doc_path):
            issues.append(f"{doc_path} missing assessment item bank ledger link")

    if issues:
        fail(f"assessment item bank ledger is incomplete: {'; '.join(issues[:10])}")
    ok("assessment item bank ledger covers exposure levels, 10 items, rotation, and makeup equivalence")


def check_assessment_blueprint_coverage_matrix() -> None:
    text = read("docs/assessment-blueprint-coverage-matrix.md")
    issues = []

    for marker in [
        "Assessment Blueprint and Coverage Matrix",
        "复核日期：2026-06-05",
        "Blueprint Dimensions",
        "Outcome Coverage Matrix",
        "Assessment Channel Balance",
        "Cognitive Level Ladder",
        "Sampling and Rotation Rules",
        "Evidence and Grading Gates",
        "Gap Audit",
        "Release Checklist",
        "course-outcome-map.md",
        "assignment-handout-pack.md",
        "written-problem-set.md",
        "quiz-checkpoint-guide.md",
        "assessment-item-bank-ledger.md",
        "project-submission-dossier.md",
        "gradebook-lms-operations.md",
    ]:
        if marker not in text:
            issues.append(f"missing assessment blueprint marker: {marker}")

    outcome_rows = extract_markdown_table_after(text, "## Outcome Coverage Matrix")
    if len(outcome_rows) != 7:
        issues.append(f"expected 6 outcome rows plus header, got {len(outcome_rows)}")
    outcome_ids = {cells[0] for cells in outcome_rows[1:] if cells}
    for outcome_id in ["CO1", "CO2", "CO3", "CO4", "CO5", "CO6"]:
        if outcome_id not in outcome_ids:
            issues.append(f"assessment blueprint missing outcome row: {outcome_id}")

    required_channels = [
        "programming assignment",
        "written derivation",
        "quiz/checkpoint",
        "capstone artifact",
        "reading/source audit",
        "presentation/peer review",
    ]
    for channel in required_channels:
        if channel not in text:
            issues.append(f"assessment blueprint missing channel: {channel}")

    cognitive_rows = extract_markdown_table_after(text, "## Cognitive Level Ladder")
    cognitive_levels = {cells[0] for cells in cognitive_rows[1:] if cells}
    for level in ["remember", "understand", "apply", "analyze", "evaluate", "create"]:
        if level not in cognitive_levels:
            issues.append(f"assessment blueprint missing cognitive level: {level}")

    balance_rows = extract_markdown_table_after(text, "## Assessment Channel Balance")
    weight_by_channel = {cells[0]: cells[1] for cells in balance_rows[1:] if len(cells) >= 2}
    expected_weights = {
        "programming assignments": "35%",
        "written derivations": "20%",
        "training capstone": "15%",
        "inference capstone": "20%",
        "reading/participation/peer review": "10%",
    }
    for channel, weight in expected_weights.items():
        if weight_by_channel.get(channel) != weight:
            issues.append(f"assessment blueprint channel weight mismatch: {channel} -> {weight_by_channel.get(channel)}")

    gate_rows = extract_markdown_table_after(text, "## Evidence and Grading Gates")
    gates = {cells[0] for cells in gate_rows[1:] if cells}
    for gate in [
        "auto_gate",
        "written_gate",
        "checkpoint_gate",
        "capstone_gate",
        "source_gate",
        "rubric_calibration_gate",
        "accessibility_integrity_gate",
    ]:
        if gate not in gates:
            issues.append(f"assessment blueprint missing gate: {gate}")

    gap_rows = extract_markdown_table_after(text, "## Gap Audit")
    if len(gap_rows) < 8:
        issues.append(f"assessment blueprint gap audit too short: {len(gap_rows)} rows")
    for cells in gap_rows[1:]:
        if len(cells) >= 2 and cells[1] != "covered":
            issues.append(f"assessment blueprint gap audit not covered: {cells[:2]}")

    for item_id in [
        "QC-W1-BPE-01",
        "QC-W2-MASK-01",
        "QC-W8-EVAL-01",
        "QC-W9-SLO-01",
        "QC-W10-SOURCE-01",
        "QC-MAKEUP-EQUIV-01",
    ]:
        if item_id not in text:
            issues.append(f"assessment blueprint missing item-bank link: {item_id}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/course-outcome-map.md",
        "docs/assignment-handout-pack.md",
        "docs/written-problem-set.md",
        "docs/quiz-checkpoint-guide.md",
        "docs/assessment-item-bank-ledger.md",
        "docs/assessment-administration-policy.md",
    ]
    for doc_path in linked_docs:
        if "assessment-blueprint-coverage-matrix.md" not in read(doc_path):
            issues.append(f"{doc_path} missing assessment blueprint link")

    if "assessment-blueprint-coverage-matrix.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing assessment blueprint")
    if "docs/assessment-blueprint-coverage-matrix.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing assessment blueprint")

    if issues:
        fail(f"assessment blueprint coverage matrix is incomplete: {'; '.join(issues[:10])}")
    ok("assessment blueprint coverage matrix covers CO1-CO6, channels, cognitive levels, gates, and release links")


def check_assessment_item_analysis_psychometrics() -> None:
    text = read("docs/assessment-item-analysis-psychometrics.md")
    issues = []

    for marker in [
        "Assessment Item Analysis and Psychometrics Guide",
        "复核日期：2026-06-05",
        "Item Analysis Scope",
        "Metric Definitions",
        "Decision Thresholds",
        "Analysis Record Schema",
        "Current Dry-Run Analysis Records",
        "Post-Assessment Workflow",
        "Fairness and Privacy Rules",
        "Release Checklist",
        "assessment-blueprint-coverage-matrix.md",
        "assessment-item-bank-ledger.md",
        "assessment-administration-policy.md",
        "learning-analytics-remediation-plan.md",
        "concept-misconception-map.md",
        "gradebook-lms-operations.md",
        "grading-drift-audit-ledger.md",
        "course-operations-log.md",
    ]:
        if marker not in text:
            issues.append(f"missing item-analysis marker: {marker}")

    scope_rows = extract_markdown_table_after(text, "## Item Analysis Scope")
    scope_ids = {cells[0] for cells in scope_rows[1:] if cells}
    for scope_id in ["IA-QUICK", "IA-RECAP", "IA-MIDTERM", "IA-FINAL", "IA-CAPSTONE", "IA-MAKEUP"]:
        if scope_id not in scope_ids:
            issues.append(f"item analysis missing scope: {scope_id}")
    for item_id in [
        "QC-W1-BPE-01",
        "QC-W2-MASK-01",
        "QC-W3-CACHE-01",
        "QC-W5-TRAIN-01",
        "QC-W6-SAMPLING-01",
        "QC-W7-DPO-01",
        "QC-W8-EVAL-01",
        "QC-W9-SLO-01",
        "QC-W10-SOURCE-01",
        "QC-MAKEUP-EQUIV-01",
    ]:
        if item_id not in text:
            issues.append(f"item analysis missing item bank reference: {item_id}")

    metric_rows = extract_markdown_table_after(text, "## Metric Definitions")
    metric_ids = {cells[0] for cells in metric_rows[1:] if cells}
    for metric_id in [
        "item_difficulty_p",
        "item_discrimination_d",
        "distractor_efficiency",
        "short_answer_rubric_fit",
        "completion_time_median",
        "subgroup_review_flag",
        "retake_equivalence_delta",
    ]:
        if metric_id not in metric_ids:
            issues.append(f"item analysis missing metric: {metric_id}")
    for cells in metric_rows[1:]:
        if len(cells) != 4:
            issues.append(f"item analysis metric row expected 4 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not all(cells[1:]):
            issues.append(f"{cells[0]} has empty metric definition field")

    threshold_rows = extract_markdown_table_after(text, "## Decision Thresholds")
    decision_ids = {cells[0] for cells in threshold_rows[1:] if cells}
    for decision_id in [
        "IA-DIFF-HARD",
        "IA-DIFF-EASY",
        "IA-DISC-LOW",
        "IA-DISTRACTOR-DEAD",
        "IA-RUBRIC-DRIFT",
        "IA-TIME-OVER",
        "IA-FAIRNESS-FLAG",
        "IA-EQUIV-FAIL",
    ]:
        if decision_id not in decision_ids:
            issues.append(f"item analysis missing decision threshold: {decision_id}")
    for cells in threshold_rows[1:]:
        if len(cells) != 4:
            issues.append(f"item analysis threshold row expected 4 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[1] or not cells[2] or not cells[3]:
            issues.append(f"{cells[0]} missing threshold action or linked record")

    schema_rows = extract_markdown_table_after(text, "## Analysis Record Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    for field in [
        "analysis_id",
        "assessment_id",
        "item_bank_id",
        "outcome_id",
        "cognitive_level",
        "sample_size",
        "item_difficulty_p",
        "item_discrimination_d",
        "distractor_efficiency",
        "short_answer_rubric_fit",
        "completion_time_median",
        "subgroup_review_flag",
        "decision_id",
        "action_taken",
        "public_summary",
        "private_record_location",
    ]:
        if field not in schema_fields:
            issues.append(f"item analysis schema missing field: {field}")

    record_rows = extract_markdown_table_after(text, "## Current Dry-Run Analysis Records")
    if len(record_rows) < 7:
        issues.append(f"expected at least 6 dry-run item analysis records, got {max(0, len(record_rows) - 1)}")
    record_ids = {cells[0] for cells in record_rows[1:] if cells}
    for record_id in [
        "IA-2026-W1-BPE",
        "IA-2026-W2-MASK",
        "IA-2026-W5-TRAIN",
        "IA-2026-W8-EVAL",
        "IA-2026-W10-SOURCE",
        "IA-2026-CAP-SLO",
    ]:
        if record_id not in record_ids:
            issues.append(f"item analysis missing dry-run record: {record_id}")
    record_outcomes = {cells[3] for cells in record_rows[1:] if len(cells) > 3}
    for outcome_id in ["CO1", "CO2", "CO4", "CO5", "CO6"]:
        if outcome_id not in record_outcomes:
            issues.append(f"item analysis dry-run records missing outcome: {outcome_id}")
    for cells in record_rows[1:]:
        if len(cells) != 14:
            issues.append(f"item analysis dry-run row expected 14 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[12] or not cells[13]:
            issues.append(f"{cells[0]} missing decision_id or action_taken")

    workflow_rows = extract_markdown_table_after(text, "## Post-Assessment Workflow")
    workflow_steps = [cells[0] for cells in workflow_rows[1:] if cells]
    for expected_step in [
        "1. collect aggregate",
        "2. compute metrics",
        "3. classify decisions",
        "4. update records",
        "5. publish safe summary",
        "6. archive private evidence",
    ]:
        if expected_step not in workflow_steps:
            issues.append(f"item analysis workflow missing step: {expected_step}")

    for privacy_marker in [
        "suppress small-n subgroup",
        "individual students",
        "accommodation",
        "Active item statistics",
        "Hidden-test",
        "objective and cognitive_level equivalence",
    ]:
        if privacy_marker not in text:
            issues.append(f"item analysis privacy rule missing marker: {privacy_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/assessment-item-bank-ledger.md",
        "docs/assessment-blueprint-coverage-matrix.md",
        "docs/assessment-administration-policy.md",
        "docs/learning-analytics-remediation-plan.md",
    ]
    for doc_path in linked_docs:
        if "assessment-item-analysis-psychometrics.md" not in read(doc_path):
            issues.append(f"{doc_path} missing item-analysis guide link")

    if "assessment-item-analysis-psychometrics.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing item-analysis guide")
    if "docs/assessment-item-analysis-psychometrics.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing item-analysis guide")

    if issues:
        fail(f"assessment item analysis guide is incomplete: {'; '.join(issues[:10])}")
    ok("assessment item analysis guide covers psychometric metrics, thresholds, dry-run records, workflow, privacy, and release links")


def check_ml_foundations_prerequisite_bridge() -> None:
    text = read("docs/ml-foundations-prerequisite-bridge.md")
    issues = []

    for topic in (
        "Calculus / gradients",
        "Probability",
        "Statistics",
        "ML objectives",
        "Generalization",
        "Optimization",
        "Evaluation",
    ):
        if f"| {topic} |" not in text:
            issues.append(f"missing prerequisite coverage row: {topic}")

    for diagnostic_module in (
        "calculus",
        "probability",
        "statistics",
        "ML objective",
        "generalization",
        "evaluation",
    ):
        if f"| {diagnostic_module} |" not in text:
            issues.append(f"missing diagnostic module row: {diagnostic_module}")

    for mini_lecture in (
        "Mini-Lecture: Calculus to Backprop",
        "Mini-Lecture: Probability and Language Models",
        "Mini-Lecture: Statistics for Experiments",
        "Mini-Lecture: ML Objectives and Generalization",
    ):
        if mini_lecture not in text:
            issues.append(f"missing mini-lecture: {mini_lecture}")

    for evidence_id in (
        "objective_mapping",
        "baseline_result",
        "split_statement",
        "leakage_check",
        "variance_note",
        "ablation_plan",
        "metric_limit",
        "generalization_boundary",
    ):
        if f"| {evidence_id} |" not in text:
            issues.append(f"missing project evidence field: {evidence_id}")

    for required_phrase in (
        "college calculus",
        "probability/statistics",
        "foundations of machine learning",
        "train/validation split",
        "overfitting",
        "data leakage",
        "benchmark contamination",
        ".venv/bin/python verify_course.py",
    ):
        if required_phrase not in text:
            issues.append(f"missing ML foundations bridge phrase: {required_phrase}")

    for linked_doc in (
        "prerequisite-diagnostic.md",
        "math-prerequisites.md",
        "python-pytorch-review-session.md",
        "reading-list.md",
        "course-outcome-map.md",
        "project-report-template.md",
    ):
        if linked_doc not in text:
            issues.append(f"ML foundations bridge missing linked doc: {linked_doc}")

    prerequisite_diagnostic = read("docs/prerequisite-diagnostic.md")
    for marker in (
        "ML Foundations Prerequisite Bridge",
        "ML Foundations 得分",
        "benchmark variance",
        "generalization boundary",
    ):
        if marker not in prerequisite_diagnostic:
            issues.append(f"prerequisite diagnostic missing ML foundations marker: {marker}")

    math_prerequisites = read("docs/math-prerequisites.md")
    for marker in (
        "统计与 ML Foundations 入口",
        "ML Foundations Prerequisite Bridge",
        "train / validation / test split",
    ):
        if marker not in math_prerequisites:
            issues.append(f"math prerequisites missing ML foundations marker: {marker}")

    reading_list = read("docs/reading-list.md")
    for marker in (
        "Week 0: 先修与 ML Foundations Bridge",
        "Stanford CS224N",
        "ML Foundations Prerequisite Bridge",
    ):
        if marker not in reading_list:
            issues.append(f"reading list missing ML foundations marker: {marker}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for marker in (
        "college calculus",
        "probability/statistics",
        "ML Foundations Prerequisite Bridge",
        "ML objectives",
        "generalization",
        "evaluation",
    ):
        if marker not in snapshot:
            issues.append(f"CS224N snapshot missing ML foundations marker: {marker}")

    crosswalk = read("docs/cs224n-benchmark-crosswalk.md")
    for marker in (
        "ML Foundations Prerequisite Bridge",
        "college calculus",
        "probability/statistics",
        "ML foundations",
    ):
        if marker not in crosswalk:
            issues.append(f"CS224N crosswalk missing ML foundations marker: {marker}")

    if issues:
        fail(f"ML foundations prerequisite bridge is incomplete: {'; '.join(issues[:10])}")
    ok("ML foundations prerequisite bridge covers calculus, probability/statistics, objectives, generalization, evaluation, and project evidence")


def check_gradebook_lms_operations() -> None:
    text = read("docs/gradebook-lms-operations.md")
    issues = []

    for column_id in (
        "student_id",
        "student_display_name",
        "enrollment_status",
        "assignment_id",
        "grade_category",
        "raw_score",
        "max_score",
        "normalized_score",
        "weight_percent",
        "weighted_points",
        "submission_timestamp",
        "due_timestamp",
        "late_days_used",
        "late_penalty",
        "extension_reason_code",
        "grader_id",
        "rubric_version",
        "release_batch",
        "regrade_status",
        "regrade_decision_id",
        "integrity_hold",
        "student_visible_feedback",
    ):
        if f"| {column_id} |" not in text:
            issues.append(f"missing gradebook schema column: {column_id}")

    for reconciliation_check in (
        "category sum",
        "item mapping",
        "max score",
        "weighted total",
        "late-day application",
        "missing submission",
        "hold visibility",
    ):
        if f"| {reconciliation_check} |" not in text:
            issues.append(f"missing weight reconciliation check: {reconciliation_check}")

    for ledger_field in (
        "late_days_initial",
        "late_days_used_total",
        "late_days_remaining",
        "assignment_id",
        "days_charged",
        "pooled_team_days",
        "exception_code",
        "audit_note",
    ):
        if f"| {ledger_field} |" not in text:
            issues.append(f"missing late-day ledger field: {ledger_field}")

    for release_field in (
        "release_batch",
        "covered_items",
        "grading_basis",
        "common_issues",
        "late_day_policy",
        "regrade_open_at",
        "regrade_close_at",
        "contact_path",
    ):
        if f"| {release_field} |" not in text:
            issues.append(f"missing grade release field: {release_field}")

    for status in ("requested", "in_review", "resolved", "escalated", "closed_late"):
        if f"| {status} |" not in text:
            issues.append(f"missing regrade workflow status: {status}")

    for access_role in (
        "Instructor",
        "Course Manager",
        "Head TA",
        "Grader / Discussion TA",
        "Project Mentor",
    ):
        if f"| {access_role} |" not in text:
            issues.append(f"missing access-control role: {access_role}")

    for linked_doc in (
        "syllabus.md",
        "course-calendar-deadline-ledger.md",
        "assignment-submission-guide.md",
        "grading-calibration.md",
        "course-policies.md",
        "course-staff-office-hours-directory.md",
        "academic-integrity-case-process.md",
        "course-operations-log.md",
    ):
        if linked_doc not in text:
            issues.append(f"gradebook/LMS guide missing linked doc: {linked_doc}")

    for phrase in (
        "Canvas",
        "Moodle",
        "Blackboard",
        "Gradescope",
        "weighted gradebook",
        "late-day ledger",
        "team pooling",
        "integrity hold",
        "minimum privileges",
        "hidden-test category feedback",
        ".venv/bin/python verify_course.py",
    ):
        if phrase not in text:
            issues.append(f"missing gradebook/LMS phrase: {phrase}")

    syllabus = read("docs/syllabus.md")
    for marker in (
        "Gradebook and LMS Operations Guide",
        "late-day 账本",
        "regrade request",
        "决定 ID",
    ):
        if marker not in syllabus:
            issues.append(f"syllabus missing gradebook/LMS marker: {marker}")

    assignment_guide = read("docs/assignment-submission-guide.md")
    for marker in (
        "Gradebook and LMS Operations Guide",
        "release_batch",
        "rubric_version",
        "weighted gradebook",
        "regrade_decision_id",
    ):
        if marker not in assignment_guide:
            issues.append(f"assignment submission guide missing gradebook/LMS marker: {marker}")

    for doc_path in ("docs/course-policies.md", "docs/grading-calibration.md", "docs/course-staff-office-hours-directory.md"):
        doc_text = read(doc_path)
        if "Gradebook and LMS Operations Guide" not in doc_text:
            issues.append(f"{doc_path} missing gradebook/LMS link")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for marker in (
        "gradebook schema",
        "late-day ledger",
        "release batch",
        "regrade workflow",
    ):
        if marker not in snapshot:
            issues.append(f"CS224N snapshot missing gradebook/LMS marker: {marker}")

    crosswalk = read("docs/cs224n-benchmark-crosswalk.md")
    for marker in (
        "Gradebook and LMS Operations Guide",
        "gradebook column",
        "late-day ledger",
        "regrade decision",
    ):
        if marker not in crosswalk:
            issues.append(f"CS224N crosswalk missing gradebook/LMS marker: {marker}")

    if issues:
        fail(f"gradebook/LMS operations guide is incomplete: {'; '.join(issues[:10])}")
    ok("gradebook/LMS operations guide covers schema, weights, late days, release, regrade, privacy, and audit hooks")


def check_comprehensive_review_study_guide() -> None:
    text = read("docs/comprehensive-review-study-guide.md")
    issues = []

    for marker in [
        "Comprehensive Review Study Guide",
        "复核日期：2026-06-05",
        "Review Outcomes",
        "Two-Pass Review Schedule",
        "Self-Diagnostic Checklist",
        "Error Log Template",
        "Practice Set Sequence",
        "Staff Use",
        "Release Checklist",
        "midterm-final-review-pack.md",
        "quiz-checkpoint-guide.md",
        "written-problem-set.md",
        "worked-example-pack.md",
        "topic-dependency-map.md",
        "reading-discussion-question-bank.md",
        "assessment-blueprint-coverage-matrix.md",
        "concept-misconception-map.md",
        "notation-shape-glossary.md",
        "learning-analytics-remediation-plan.md",
        "student site release",
    ]:
        if marker not in text:
            issues.append(f"missing comprehensive review marker: {marker}")

    outcome_rows = extract_markdown_table_after(text, "## Review Outcomes")
    outcome_ids = {cells[0] for cells in outcome_rows[1:] if cells}
    for outcome_id in ["CR-O1", "CR-O2", "CR-O3", "CR-O4", "CR-O5"]:
        if outcome_id not in outcome_ids:
            issues.append(f"comprehensive review missing outcome: {outcome_id}")
    for cells in outcome_rows[1:]:
        if len(cells) != 4:
            issues.append(f"review outcome row expected 4 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[1] or not cells[2] or not cells[3]:
            issues.append(f"{cells[0]} missing student ability, evidence, or source")

    schedule_rows = extract_markdown_table_after(text, "## Two-Pass Review Schedule")
    schedule_ids = {cells[0] for cells in schedule_rows[1:] if cells}
    for schedule_id in [f"CR-S{index}" for index in range(1, 7)]:
        if schedule_id not in schedule_ids:
            issues.append(f"comprehensive review missing schedule row: {schedule_id}")
    for cells in schedule_rows[1:]:
        if len(cells) != 5:
            issues.append(f"review schedule row expected 5 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[1] or not cells[2] or not cells[3] or not cells[4]:
            issues.append(f"{cells[0]} missing timing, goal, tasks, or exit check")

    diagnostic_rows = extract_markdown_table_after(text, "## Self-Diagnostic Checklist")
    diagnostic_ids = {cells[0] for cells in diagnostic_rows[1:] if cells}
    for diagnostic_id in [
        "CR-D-SHAPE",
        "CR-D-MASK",
        "CR-D-FORMULA",
        "CR-D-OBJECTIVE",
        "CR-D-METRIC",
        "CR-D-SOURCE",
        "CR-D-CAPSTONE",
    ]:
        if diagnostic_id not in diagnostic_ids:
            issues.append(f"comprehensive review missing diagnostic: {diagnostic_id}")
    for cells in diagnostic_rows[1:]:
        if len(cells) != 4:
            issues.append(f"diagnostic row expected 4 cells, got {len(cells)}: {cells[:2]}")

    error_rows = extract_markdown_table_after(text, "## Error Log Template")
    error_fields = {cells[0] for cells in error_rows[1:] if cells}
    for field in ["error_id", "source", "category", "first_wrong_step", "corrected_rule", "evidence_to_redo", "cleared_when"]:
        if field not in error_fields:
            issues.append(f"comprehensive review error log missing field: {field}")

    practice_rows = extract_markdown_table_after(text, "## Practice Set Sequence")
    practice_ids = {cells[0] for cells in practice_rows[1:] if cells}
    for practice_id in ["CR-P-MIDTERM", "CR-P-FINAL", "CR-P-SHAPE", "CR-P-SOURCE", "CR-P-PROJECT"]:
        if practice_id not in practice_ids:
            issues.append(f"comprehensive review missing practice sequence: {practice_id}")
    for cells in practice_rows[1:]:
        if len(cells) != 4:
            issues.append(f"practice sequence row expected 4 cells, got {len(cells)}: {cells[:2]}")

    staff_rows = extract_markdown_table_after(text, "## Staff Use")
    staff_actions = {cells[0] for cells in staff_rows[1:] if cells}
    for staff_action in ["CR-STAFF-RECAP", "CR-STAFF-OH", "CR-STAFF-CALIBRATE", "CR-STAFF-SCOPE"]:
        if staff_action not in staff_actions:
            issues.append(f"comprehensive review missing staff action: {staff_action}")
    for cells in staff_rows[1:]:
        if len(cells) != 3:
            issues.append(f"staff use row expected 3 cells, got {len(cells)}: {cells[:2]}")

    for release_marker in [
        "hidden tests",
        "reference_solution.py",
        "private grading samples",
        "real student submissions",
        "instructor-only answer keys",
    ]:
        if release_marker not in text:
            issues.append(f"comprehensive review release checklist missing marker: {release_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/midterm-final-review-pack.md",
        "docs/quiz-checkpoint-guide.md",
        "docs/written-problem-set.md",
        "docs/topic-dependency-map.md",
        "docs/assessment-blueprint-coverage-matrix.md",
    ]
    for doc_path in linked_docs:
        if "comprehensive-review-study-guide.md" not in read(doc_path):
            issues.append(f"{doc_path} missing comprehensive review study guide link")

    if "comprehensive-review-study-guide.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing comprehensive review study guide")
    if "docs/comprehensive-review-study-guide.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing comprehensive review study guide")

    if issues:
        fail(f"comprehensive review study guide is incomplete: {'; '.join(issues[:10])}")
    ok("comprehensive review study guide covers outcomes, two-pass schedule, diagnostics, error log, practice sequence, staff use, and release links")


def check_assessment_administration_policy() -> None:
    text = read("docs/assessment-administration-policy.md")
    issues = []

    for assessment_type in (
        "lecture_quick_check",
        "recap_quiz",
        "prerequisite_diagnostic",
        "midterm_checkpoint",
        "capstone_readiness_check",
        "final_review_quiz",
        "makeup_assessment",
    ):
        if f"| {assessment_type} |" not in text:
            issues.append(f"missing assessment type row: {assessment_type}")

    for announcement_field in (
        "assessment_id",
        "coverage",
        "weight_percent",
        "release_at / start_at / due_at",
        "duration_minutes",
        "allowed_materials",
        "delivery_mode",
        "submission_format",
        "regrade_window",
        "accommodation_path",
    ):
        if f"| {announcement_field} |" not in text:
            issues.append(f"missing assessment announcement field: {announcement_field}")

    for material_mode in (
        "closed-book",
        "one-page notes",
        "open-book local",
        "coding check",
        "oral check",
    ):
        if f"| {material_mode} |" not in text:
            issues.append(f"missing allowed-materials mode: {material_mode}")

    for security_field in (
        "item_bank_id",
        "learning_objective",
        "variant_policy",
        "source_boundary",
        "exposure_level",
        "retirement_trigger",
    ):
        if f"| {security_field} |" not in text:
            issues.append(f"missing item-security field: {security_field}")

    for delivery_mode in (
        "in-class paper",
        "LMS timed quiz",
        "take-home",
        "remote oral check",
        "accessibility alternative",
    ):
        if f"| {delivery_mode} |" not in text:
            issues.append(f"missing delivery/proctoring mode: {delivery_mode}")

    for accommodation_case in (
        "documented accommodation",
        "illness / emergency",
        "LMS outage",
        "timezone conflict",
        "team project conflict",
    ):
        if f"| {accommodation_case} |" not in text:
            issues.append(f"missing accommodation/makeup case: {accommodation_case}")

    for integrity_stage in (
        "signal_triage",
        "private_notice",
        "manual_review",
        "grade_hold",
        "resolution",
    ):
        if f"| {integrity_stage} |" not in text:
            issues.append(f"missing integrity incident stage: {integrity_stage}")

    for release_field in (
        "score_breakdown",
        "common_misconceptions",
        "rubric_version",
        "regrade_open_at / regrade_close_at",
        "makeup_status",
        "integrity_hold",
        "remediation_path",
    ):
        if f"| {release_field} |" not in text:
            issues.append(f"missing assessment release field: {release_field}")

    for metric in (
        "participation_count",
        "score_distribution",
        "low_item_clusters",
        "accommodation_count",
        "makeup_count",
        "regrade_count",
        "integrity_signal_count",
        "item_retirement_decision",
    ):
        if f"| {metric} |" not in text:
            issues.append(f"missing post-assessment metric: {metric}")

    for linked_doc in (
        "syllabus.md",
        "quiz-checkpoint-guide.md",
        "midterm-final-review-pack.md",
        "course-calendar-deadline-ledger.md",
        "gradebook-lms-operations.md",
        "accessibility-student-support.md",
        "academic-integrity-case-process.md",
        "course-communication-policy.md",
        "course-operations-log.md",
        "claim-audit-worksheet.md",
        "external-source-verification.md",
    ):
        if linked_doc not in text:
            issues.append(f"assessment administration policy missing linked doc: {linked_doc}")

    for phrase in (
        "hidden assignment tests",
        "reference_solution.py",
        "active item bank",
        "remote proctored",
        "intrusive proctoring",
        "honor statement",
        "makeup assessment",
        "allowed materials",
        "accommodation path",
        ".venv/bin/python verify_course.py",
    ):
        if phrase not in text:
            issues.append(f"missing assessment-administration phrase: {phrase}")

    syllabus = read("docs/syllabus.md")
    for marker in (
        "Assessment Administration and Exam Integrity Policy",
        "allowed materials",
        "makeup",
        "评估诚信流程",
    ):
        if marker not in syllabus:
            issues.append(f"syllabus missing assessment-administration marker: {marker}")

    quiz_guide = read("docs/quiz-checkpoint-guide.md")
    for marker in (
        "Assessment Administration and Exam Integrity Policy",
        "allowed materials",
        "makeup assessment",
        "assessment_id",
    ):
        if marker not in quiz_guide:
            issues.append(f"quiz/checkpoint guide missing assessment-administration marker: {marker}")

    review_pack = read("docs/midterm-final-review-pack.md")
    for marker in (
        "Assessment Administration and Exam Integrity Policy",
        "assessment_id",
        "allowed materials",
        "makeup",
        "regrade window",
    ):
        if marker not in review_pack:
            issues.append(f"midterm/final review pack missing assessment-administration marker: {marker}")

    deadline_ledger = read("docs/course-calendar-deadline-ledger.md")
    for marker in (
        "Assessment Administration and Exam Integrity Policy",
        "assessment window",
        "allowed materials",
        "makeup",
        "accommodation path",
    ):
        if marker not in deadline_ledger:
            issues.append(f"deadline ledger missing assessment-administration marker: {marker}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for marker in (
        "Quiz / checkpoint administration",
        "Assessment Administration and Exam Integrity Policy",
        "allowed materials",
        "makeup assessment",
        "item security",
    ):
        if marker not in snapshot:
            issues.append(f"CS224N snapshot missing assessment-administration marker: {marker}")

    crosswalk = read("docs/cs224n-benchmark-crosswalk.md")
    for marker in (
        "Quiz / checkpoint administration",
        "Assessment Administration and Exam Integrity Policy",
        "allowed materials",
        "makeup assessment",
        "item security",
    ):
        if marker not in crosswalk:
            issues.append(f"CS224N crosswalk missing assessment-administration marker: {marker}")

    if issues:
        fail(f"assessment administration policy is incomplete: {'; '.join(issues[:10])}")
    ok("assessment administration policy covers assessment types, allowed materials, item security, makeup, integrity, release, and review")


def check_staff_assistance_code_review_policy() -> None:
    text = read("docs/staff-assistance-code-review-policy.md")
    issues = []

    for assistance_level in (
        "concept_hint",
        "debug_trace",
        "limited_code_view",
        "pseudocode_review",
        "artifact_review",
        "rubric_explanation",
    ):
        if f"| {assistance_level} |" not in text:
            issues.append(f"missing assistance level row: {assistance_level}")

    for course_item in (
        "Ch01 BPE",
        "Ch02 Embeddings / RoPE",
        "Ch03 Attention",
        "Ch04 MHA / GQA / MLA",
        "Ch05 Transformer Block",
        "Ch06 GPT / MoE",
        "Ch07 Training Loop",
        "Ch08 Generation",
        "Ch09 Alignment",
        "Ch10 Inference / RAG",
        "Ch11 Classic NLP",
    ):
        if f"| {course_item} |" not in text:
            issues.append(f"missing assignment assistance row: {course_item}")

    for stage in ("proposal", "milestone", "mentor meeting", "final report draft", "presentation rehearsal"):
        if f"| {stage} |" not in text:
            issues.append(f"missing capstone boundary stage: {stage}")

    for office_hour_field in (
        "course_item",
        "command",
        "first_failure",
        "expected_shape_or_behavior",
        "minimal_reproduction",
        "attempted_fix",
    ):
        if f"| {office_hour_field} |" not in text:
            issues.append(f"missing office-hours interaction field: {office_hour_field}")

    for channel in ("public forum", "private message", "office hours queue", "LMS regrade"):
        if f"| {channel} |" not in text:
            issues.append(f"missing public/private channel row: {channel}")

    for regrade_case in (
        "rubric explanation",
        "environment dispute",
        "manual review",
        "integrity concern",
        "staff mistake",
    ):
        if f"| {regrade_case} |" not in text:
            issues.append(f"missing regrade/integrity boundary row: {regrade_case}")

    for log_field in (
        "date",
        "staff_role",
        "course_item",
        "assistance_level",
        "public_or_private",
        "issue_category",
        "action_taken",
        "fairness_followup",
    ):
        if f"| {log_field} |" not in text:
            issues.append(f"missing staff assistance log field: {log_field}")

    for linked_doc in (
        "syllabus.md",
        "course-staff-office-hours-directory.md",
        "discussion-office-hours-guide.md",
        "assignment-submission-guide.md",
        "project-team-mentor-policy.md",
        "academic-integrity-case-process.md",
        "gradebook-lms-operations.md",
        "course-operations-log.md",
    ):
        if linked_doc not in text:
            issues.append(f"staff assistance policy missing linked doc: {linked_doc}")

    for phrase in (
        "Ch01-Ch02",
        "Ch03-Ch11",
        "final project / capstone",
        "hidden tests",
        "reference solution",
        "完整可提交实现",
        "不能把 staff 的修复代码作为学生核心贡献",
        ".venv/bin/python verify_course.py",
    ):
        if phrase not in text:
            issues.append(f"missing staff assistance phrase: {phrase}")

    syllabus = read("docs/syllabus.md")
    for marker in (
        "Staff Assistance and Code Review Boundary Policy",
        "staff 对学生代码",
        "伪代码",
        "artifact",
    ):
        if marker not in syllabus:
            issues.append(f"syllabus missing staff-assistance marker: {marker}")

    staff_directory = read("docs/course-staff-office-hours-directory.md")
    for marker in (
        "Staff Assistance and Code Review Boundary Policy",
        "limited_code_view",
        "pseudocode",
        "fairness_followup",
    ):
        if marker not in staff_directory:
            issues.append(f"staff directory missing staff-assistance marker: {marker}")

    discussion_guide = read("docs/discussion-office-hours-guide.md")
    for marker in (
        "Staff Assistance and Code Review Boundary Policy",
        "limited_code_view",
        "pseudocode_review",
        "rubric_explanation",
    ):
        if marker not in discussion_guide:
            issues.append(f"discussion guide missing staff-assistance marker: {marker}")

    assignment_guide = read("docs/assignment-submission-guide.md")
    for marker in (
        "Staff Assistance and Code Review Boundary Policy",
        "minimal reproduction",
        "attempted fix",
        "Ch03-Ch11",
    ):
        if marker not in assignment_guide:
            issues.append(f"assignment guide missing staff-assistance marker: {marker}")

    project_policy = read("docs/project-team-mentor-policy.md")
    for marker in (
        "Staff Assistance and Code Review Boundary Policy",
        "artifact_review",
        "完整项目实现",
        "report outline",
    ):
        if marker not in project_policy:
            issues.append(f"project-team policy missing staff-assistance marker: {marker}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for marker in (
        "Staff help boundary",
        "Staff Assistance and Code Review Boundary Policy",
        "limited_code_view",
        "pseudocode_review",
        "artifact_review",
    ):
        if marker not in snapshot:
            issues.append(f"CS224N snapshot missing staff-assistance marker: {marker}")

    crosswalk = read("docs/cs224n-benchmark-crosswalk.md")
    for marker in (
        "Staff assistance and code review boundaries",
        "Staff Assistance and Code Review Boundary Policy",
        "limited_code_view",
        "pseudocode_review",
        "fairness_followup",
    ):
        if marker not in crosswalk:
            issues.append(f"CS224N crosswalk missing staff-assistance marker: {marker}")

    if issues:
        fail(f"staff assistance/code review policy is incomplete: {'; '.join(issues[:10])}")
    ok("staff assistance/code review policy covers assistance levels, assignment matrix, capstone boundaries, office hours, regrade, and fairness follow-up")


def check_project_team_mentor_policy() -> None:
    text = read("docs/project-team-mentor-policy.md")
    issues = []

    for team_size in ("1 人", "2 人", "3 人"):
        if f"| {team_size} |" not in text:
            issues.append(f"missing team-size row: {team_size}")

    for mentor_type in (
        "训练工程",
        "推理工程",
        "经典 NLP / evaluation",
        "alignment / safety",
        "高风险数据或应用",
    ):
        if f"| {mentor_type} |" not in text:
            issues.append(f"missing mentor matching row: {mentor_type}")

    for required_phrase in (
        "external collaborators",
        "shared project",
        "Mentor 可以做",
        "Mentor 不可以做",
        "不均衡贡献处理",
        "自评贡献比例",
        "downgrade_trigger",
        "多人项目没有未经说明地按人数线性扩大 GPU/API 额度",
        "每名学生只能参与一个本课程 final project",
        "外部协作者不能代替学生完成本课程要求",
    ):
        if required_phrase not in text:
            issues.append(f"missing project-team policy phrase: {required_phrase}")

    for linked_doc in (
        "capstone-proposal-milestone.md",
        "capstone-project-gallery.md",
        "default-final-project-guide.md",
        "project-report-template.md",
        "project-report-rubric.md",
        "data-ethics-review.md",
        "compute-resource-guide.md",
        "course-policies.md",
    ):
        if linked_doc not in text:
            issues.append(f"project-team policy missing linked doc: {linked_doc}")

    if issues:
        fail(f"project team and mentor policy is incomplete: {'; '.join(issues[:10])}")
    ok("project team and mentor policy covers teams, mentors, external collaborators, shared projects, and contribution disputes")


def check_capstone_proposal_milestone_rigor() -> None:
    text = read("docs/capstone-proposal-milestone.md")
    issues = []

    def subsection(heading: str) -> str:
        pattern = re.compile(rf"^###\s+{re.escape(heading)}\s*$", re.MULTILINE)
        match = pattern.search(text)
        if not match:
            issues.append(f"missing markdown subsection: {heading}")
            return ""
        next_match = re.search(r"^###\s+", text[match.end() :], re.MULTILINE)
        end = match.end() + next_match.start() if next_match else len(text)
        return text[match.end() : end]

    for heading in [
        "交付时间线",
        "项目提案模板",
        "Milestone 模板",
        "Milestone 评分",
        "导师反馈记录",
        "最终提交包",
    ]:
        markdown_section(text, heading)

    for marker in [
        "Experimental Rigor and Evaluation Statistics Guide",
        "split_card",
        "metric_card",
        "uncertainty_plan",
        "uncertainty_record",
        "claim_audit",
        "significance claim gate",
        "leakage_check",
        "prompt leakage",
        "retrieval contamination",
        "benchmark contamination",
        "single_seed_limit",
        "bootstrap_ci",
        "seed_sensitivity",
        "paired_comparison",
        "load-test variance",
        "statistics_gate",
        "downgrade_decision",
    ]:
        if marker not in text:
            issues.append(f"capstone proposal/milestone guide missing marker: {marker}")

    proposal_metrics = subsection("评测指标")
    for marker in ("split_card", "metric_card", "uncertainty_plan", "claim_audit"):
        if marker not in proposal_metrics:
            issues.append(f"proposal metric section missing marker: {marker}")

    risk_table = subsection("风险登记表")
    for risk in ("contamination/leakage", "uncertainty too high"):
        if f"| {risk} |" not in risk_table:
            issues.append(f"risk register missing row: {risk}")

    milestone_required = subsection("必交内容")
    for marker in ("split_card", "leakage_check", "metric_card", "uncertainty_record", "claim_audit"):
        if marker not in milestone_required:
            issues.append(f"milestone required-content section missing marker: {marker}")

    training_milestone = subsection("训练 milestone 检查表")
    inference_milestone = subsection("推理 milestone 检查表")
    if "统计严谨性" not in training_milestone:
        issues.append("training milestone checklist missing statistical rigor row")
    if "统计严谨性" not in inference_milestone:
        issues.append("inference milestone checklist missing statistical rigor row")

    mentor_feedback = markdown_section(text, "导师反馈记录")
    for marker in ("statistics_gate", "downgrade_decision"):
        if marker not in mentor_feedback:
            issues.append(f"mentor feedback record missing marker: {marker}")

    project_policy = read("docs/project-team-mentor-policy.md")
    for marker in ("statistics_gate", "split_card", "metric_card", "uncertainty_record", "claim_audit", "leakage_check"):
        if marker not in project_policy:
            issues.append(f"project-team mentor policy missing capstone rigor marker: {marker}")

    crosswalk = read("docs/cs224n-benchmark-crosswalk.md")
    for marker in ("proposal/milestone/final report", "split_card", "uncertainty_record", "contamination/leakage gate"):
        if marker not in crosswalk:
            issues.append(f"CS224N crosswalk missing capstone proposal/milestone rigor marker: {marker}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for marker in ("proposal、milestone、poster 和 report", "Capstone Proposal and Milestone Guide", "split_card", "contamination/leakage gate"):
        if marker not in snapshot:
            issues.append(f"CS224N snapshot missing capstone proposal/milestone rigor marker: {marker}")

    if issues:
        fail(f"capstone proposal/milestone rigor guide is incomplete: {'; '.join(issues[:10])}")
    ok("capstone proposal/milestone guide front-loads split, metric, uncertainty, claim, leakage, mentor, and downgrade gates")


def check_project_submission_dossier() -> None:
    text = read("docs/project-submission-dossier.md")
    issues: list[str] = []

    for heading in [
        "Dossier Stages",
        "Required File Map",
        "Structured Templates",
        "Stage Acceptance Matrix",
        "TA Review Procedure",
        "Common Downgrade Decisions",
        "Student Final Checklist",
        "Release Checklist",
    ]:
        markdown_section(text, heading)

    stage_rows = extract_markdown_table_after(text, "## Dossier Stages")
    stage_ids = {cells[0] for cells in stage_rows[1:] if cells}
    required_stage_ids = {"DSR-PROPOSAL", "DSR-MILESTONE", "DSR-FINAL", "DSR-PRESENTATION", "DSR-ARCHIVE"}
    missing_stages = sorted(required_stage_ids - stage_ids)
    if missing_stages:
        issues.append(f"submission dossier missing stages: {', '.join(missing_stages)}")
    for cells in stage_rows[1:]:
        if len(cells) != 5:
            issues.append(f"dossier stage row expected 5 cells, got {len(cells)}: {cells[:2]}")

    file_rows = extract_markdown_table_after(text, "## Required File Map")
    required_files = {
        "`proposal.md`",
        "`artifact_manifest.md`",
        "`split_card.md`",
        "`metric_card.md`",
        "`uncertainty_record.md`",
        "`claim_audit.md`",
        "`leakage_check.md`",
        "`run_log.txt`",
        "`metrics.jsonl` or `benchmark_report.json`",
        "`data_ethics_review.md`",
        "`contributions.md`",
        "`poster_or_slides.*`",
        "`archive_record.md`",
    }
    file_names = {cells[0] for cells in file_rows[1:] if cells}
    missing_files = sorted(required_files - file_names)
    if missing_files:
        issues.append(f"submission dossier missing required file rows: {', '.join(missing_files)}")
    for cells in file_rows[1:]:
        if len(cells) != 6:
            issues.append(f"required file row expected 6 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not any(stage in cells[1] for stage in required_stage_ids):
            issues.append(f"required file row has unknown stage marker: {cells[0]} -> {cells[1]}")

    required_template_fields = [
        "artifact_id:",
        "artifact_type:",
        "license_or_access:",
        "pii_risk:",
        "contamination_risk:",
        "retention_scope:",
        "split_id:",
        "train_source:",
        "dev_policy:",
        "test_policy:",
        "freeze_date:",
        "leakage_check:",
        "metric:",
        "aggregation:",
        "known_limit:",
        "method: bootstrap_ci / seed_sensitivity / paired_comparison / load_test_variance / single_seed_limit",
        "claim_id:",
        "downgrade_decision:",
    ]
    for field in required_template_fields:
        if field not in text:
            issues.append(f"structured templates missing field: {field}")

    acceptance_rows = extract_markdown_table_after(text, "## Stage Acceptance Matrix")
    acceptance_criteria = {cells[0] for cells in acceptance_rows[1:] if cells}
    required_criteria = {
        "scope",
        "reproducibility",
        "data provenance",
        "experiment design",
        "engineering evidence",
        "communication",
    }
    missing_criteria = sorted(required_criteria - acceptance_criteria)
    if missing_criteria:
        issues.append(f"stage acceptance matrix missing criteria: {', '.join(missing_criteria)}")
    for cells in acceptance_rows[1:]:
        if len(cells) != 4:
            issues.append(f"acceptance matrix row expected 4 cells, got {len(cells)}: {cells[:2]}")

    review_rows = extract_markdown_table_after(text, "## TA Review Procedure")
    review_steps = {cells[0] for cells in review_rows[1:] if cells}
    required_review_steps = {"R1 completeness", "R2 reproducibility", "R3 provenance", "R4 experiment rigor", "R5 report alignment", "R6 integrity and archive"}
    missing_review_steps = sorted(required_review_steps - review_steps)
    if missing_review_steps:
        issues.append(f"TA review procedure missing steps: {', '.join(missing_review_steps)}")
    for cells in review_rows[1:]:
        if len(cells) != 4:
            issues.append(f"TA review row expected 4 cells, got {len(cells)}: {cells[:2]}")

    downgrade_rows = extract_markdown_table_after(text, "## Common Downgrade Decisions")
    if len(downgrade_rows) < 7:
        issues.append("common downgrade decisions expected at least 6 rows")
    for trigger in ("single seed only", "public benchmark may be contaminated", "toy corpus only", "missing model card", "no P95/P99 latency", "no artifact_manifest"):
        if f"| {trigger} |" not in text:
            issues.append(f"common downgrade decisions missing trigger: {trigger}")

    final_rows = extract_markdown_table_after(text, "## Student Final Checklist")
    final_items = {cells[0] for cells in final_rows[1:] if cells}
    required_final_items = {
        "primary command",
        "environment",
        "artifact_manifest",
        "split_card",
        "metric_card",
        "uncertainty_record",
        "claim_audit",
        "leakage_check",
        "data_ethics_review",
        "contributions",
        "presentation",
        "archive boundary",
    }
    missing_final_items = sorted(required_final_items - final_items)
    if missing_final_items:
        issues.append(f"student final checklist missing items: {', '.join(missing_final_items)}")

    linked_files = {
        "README.md": "Project Submission Dossier",
        "docs/capstone-proposal-milestone.md": "project-submission-dossier.md",
        "docs/project-report-template.md": "project-submission-dossier.md",
        "docs/project-report-rubric.md": "project-submission-dossier.md",
        "docs/final-project-showcase-archive-policy.md": "project-submission-dossier.md",
        "docs/dataset-model-artifact-registry.md": "project-submission-dossier.md",
        "docs/academic-integrity-case-process.md": "project-submission-dossier.md",
        "docs/experimental-rigor-evaluation-statistics.md": "project-submission-dossier.md",
        "scripts/build_course_site_release.py": "project-submission-dossier.md",
        "scripts/generate_course_evidence_manifest.py": "docs/project-submission-dossier.md",
    }
    for path, marker in linked_files.items():
        if marker not in read(path):
            issues.append(f"{path} missing project submission dossier marker: {marker}")

    if issues:
        fail(f"project submission dossier incomplete: {'; '.join(issues[:12])}")
    ok(
        "project submission dossier covers stages, required files, templates, acceptance matrix, "
        f"TA workflow, downgrade rules, and release links ({len(file_names)} required records)"
    )


def check_final_project_showcase_archive_policy() -> None:
    text = read("docs/final-project-showcase-archive-policy.md")
    issues = []

    for showcase_type in (
        "in-class poster session",
        "recorded presentation",
        "public project abstract",
        "archived final report",
        "staff-only evaluation packet",
    ):
        if f"| {showcase_type} |" not in text:
            issues.append(f"missing showcase/archive row: {showcase_type}")

    for archive_requirement in (
        "consent",
        "redaction",
        "data license",
        "model/API boundary",
        "reproducibility summary",
        "safety review",
        "archived label",
    ):
        if f"| {archive_requirement} |" not in text:
            issues.append(f"missing public archive requirement: {archive_requirement}")

    for artifact in (
        "final report",
        "poster/slides",
        "code snapshot",
        "logs/metrics",
        "peer reviews",
        "grading notes",
    ):
        if f"| {artifact} |" not in text:
            issues.append(f"missing artifact retention row: {artifact}")

    for record_field in (
        "project_id",
        "title",
        "track",
        "visibility",
        "consent_status",
        "redaction_status",
        "artifact_manifest",
        "source_boundary",
        "reproduction_summary",
        "archived_label",
    ):
        if f"| {record_field} |" not in text:
            issues.append(f"missing archive record field: {record_field}")

    for required_phrase in (
        "CS224N Winter 2026",
        "proposal、milestone、poster 和 report",
        "archived public reports",
        "consent、redaction、source boundary 和 reproducibility artifact",
        "staff-only grading packet",
        "公开与否不影响正式成绩",
        "公开样例不是可复制答案",
        "hidden tests",
        "reference_solution.py",
        "private LMS / Ed post",
        ".venv/bin/python verify_course.py --capstone --training",
    ):
        if required_phrase not in text:
            issues.append(f"missing showcase/archive phrase: {required_phrase}")

    for linked_doc in (
        "capstone-project-gallery.md",
        "presentation-peer-review.md",
        "project-report-template.md",
        "project-report-rubric.md",
        "project-team-mentor-policy.md",
        "data-ethics-review.md",
        "material-versioning-archive-policy.md",
        "enrollment-audit-public-use-policy.md",
        "course-communication-policy.md",
    ):
        if linked_doc not in text:
            issues.append(f"showcase/archive policy missing linked doc: {linked_doc}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for snapshot_marker in (
        "| Archived project reports |",
        "Final Project Showcase and Archive Policy",
        "archived project reports",
        "staff-only grading packet",
    ):
        if snapshot_marker not in snapshot:
            issues.append(f"CS224N snapshot missing showcase/archive marker: {snapshot_marker}")

    if issues:
        fail(f"final project showcase/archive policy is incomplete: {'; '.join(issues[:10])}")
    ok("final project showcase/archive policy covers poster session, public reports, consent, redaction, and artifact retention")


def check_academic_integrity_case_process() -> None:
    text = read("docs/academic-integrity-case-process.md")
    issues = []

    for scope in (
        "编程作业",
        "书面题",
        "Capstone / final project",
        "讨论区 / peer review",
    ):
        if f"| {scope} |" not in text:
            issues.append(f"missing integrity scope row: {scope}")

    for signal in (
        "similarity cluster",
        "identical nontrivial bug",
        "reference_solution.py access",
        "hidden test leakage",
        "AI disclosure mismatch",
        "project contribution mismatch",
    ):
        if f"| {signal} |" not in text:
            issues.append(f"missing integrity triage signal: {signal}")

    for check in (
        "`reference_solution.py`",
        "tests.py modification",
        "network access",
        "public input hardcoding",
        "module rename / shape / seed",
        "similarity report",
    ):
        if f"| {check} |" not in text:
            issues.append(f"missing automated integrity check: {check}")

    for flow_marker in (
        "freeze original submission",
        "student_response",
        "policy_mapping",
        "grade_action",
        "privacy_scope",
        "follow_up",
    ):
        if flow_marker not in text:
            issues.append(f"missing manual review/case field: {flow_marker}")

    for linked_doc in (
        "course-policies.md",
        "assignment-submission-guide.md",
        "autograder-hidden-tests.md",
        "grading-calibration.md",
        "course-communication-policy.md",
        "project-team-mentor-policy.md",
        "data-ethics-review.md",
        "enrollment-audit-public-use-policy.md",
        "course-operations-log.md",
    ):
        if linked_doc not in text:
            issues.append(f"academic integrity process missing linked doc: {linked_doc}")

    for required_phrase in (
        "similarity report 的作用是排序复核优先级",
        "不能单独证明违规",
        "不在公开讨论区",
        "其他学生代码",
        "学校正式 honor code",
        "AI 工具争议按 Manual Review Flow 处理",
        "scripts/build_course_site_release.py",
        ".venv/bin/python verify_course.py --capstone --training",
    ):
        if required_phrase not in text:
            issues.append(f"missing academic integrity phrase: {required_phrase}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for snapshot_marker in (
        "| Honor code / academic integrity |",
        "Academic Integrity Case Process",
        "student_response",
        "grade_action",
    ):
        if snapshot_marker not in snapshot:
            issues.append(f"CS224N snapshot missing integrity marker: {snapshot_marker}")

    crosswalk = read("docs/cs224n-benchmark-crosswalk.md")
    for crosswalk_marker in (
        "Honor code and AI policy",
        "Academic Integrity Case Process",
        "相似性检测解释",
        "个案取证",
    ):
        if crosswalk_marker not in crosswalk:
            issues.append(f"CS224N crosswalk missing integrity marker: {crosswalk_marker}")

    if issues:
        fail(f"academic integrity case process is incomplete: {'; '.join(issues[:10])}")
    ok("academic integrity case process covers honor-code, AI, similarity, privacy, and review workflows")


def check_guest_speaker_seminar_policy() -> None:
    text = read("docs/guest-speaker-seminar-policy.md")
    issues = []

    for activity_type in (
        "guest lecture",
        "external seminar",
        "project clinic",
        "student-led paper report",
    ):
        if f"| {activity_type} |" not in text:
            issues.append(f"missing guest/seminar activity row: {activity_type}")

    for admission_check in (
        "course fit",
        "source boundary",
        "no private solution leakage",
        "accessibility",
        "privacy and consent",
        "conflict boundary",
    ):
        if f"| {admission_check} |" not in text:
            issues.append(f"missing guest/seminar admission check: {admission_check}")

    for evidence in (
        "attendance",
        "technical reflection",
        "Q&A note",
        "source audit",
        "project transfer",
    ):
        if f"| {evidence} |" not in text:
            issues.append(f"missing guest/seminar participation evidence: {evidence}")

    for alternative in (
        "时区或课程冲突",
        "学术便利安排",
        "录播不可发布",
        "讲者取消",
    ):
        if f"| {alternative} |" not in text:
            issues.append(f"missing guest/seminar alternative row: {alternative}")

    for record_field in (
        "event_id",
        "event_type",
        "speaker_or_source",
        "recording_status",
        "accessibility_support",
        "participation_credit",
        "source_boundary",
        "privacy_review",
        "follow_up_actions",
    ):
        if f"| {record_field} |" not in text:
            issues.append(f"missing guest/seminar record field: {record_field}")

    for required_phrase in (
        "不得把“人在现场”作为唯一评分依据",
        "live、recording、summary 或 approved alternative",
        "hidden tests",
        "reference_solution.py",
        "private LMS / Ed post",
        "caption / transcript",
        "External Source Verification Guide",
        "Data and Ethics Review",
        "Course Calendar and Deadline Ledger",
        ".venv/bin/python verify_course.py",
    ):
        if required_phrase not in text:
            issues.append(f"missing guest/seminar phrase: {required_phrase}")

    for linked_doc in (
        "participation-feedback-guide.md",
        "frontier-seminar-handout.md",
        "lecture-media-access-policy.md",
        "course-communication-policy.md",
        "course-operations-log.md",
        "accessibility-student-support.md",
        "external-source-verification.md",
        "external-source-inventory.md",
        "data-ethics-review.md",
    ):
        if linked_doc not in text:
            issues.append(f"guest/seminar policy missing linked doc: {linked_doc}")

    participation = read("docs/participation-feedback-guide.md")
    for participation_marker in (
        "Guest Speaker and External Seminar Policy",
        "guest lecture / external seminar",
        "technical reflection",
        "Q&A/source audit",
    ):
        if participation_marker not in participation:
            issues.append(f"participation guide missing guest/seminar marker: {participation_marker}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for snapshot_marker in (
        "guest lecture",
        "feedback surveys",
        "Ed participation",
        "karma point",
        "Guest Speaker and External Seminar Policy",
        "Q&A/source audit",
    ):
        if snapshot_marker not in snapshot:
            issues.append(f"CS224N snapshot missing guest/seminar marker: {snapshot_marker}")

    crosswalk = read("docs/cs224n-benchmark-crosswalk.md")
    for crosswalk_marker in (
        "Participation credit",
        "Guest Speaker and External Seminar Policy",
        "guest lecture reflection",
        "karma-style",
    ):
        if crosswalk_marker not in crosswalk:
            issues.append(f"CS224N crosswalk missing guest/seminar marker: {crosswalk_marker}")

    calendar = read("docs/course-calendar-deadline-ledger.md")
    for calendar_marker in (
        "guest lecture / external seminar option",
        "Guest speaker reflection",
        "guest speaker reflection window",
    ):
        if calendar_marker not in calendar:
            issues.append(f"calendar ledger missing guest/seminar marker: {calendar_marker}")

    if issues:
        fail(f"guest speaker/seminar policy is incomplete: {'; '.join(issues[:10])}")
    ok("guest speaker/seminar policy covers participation credit, alternatives, recording/privacy, source audit, and follow-up")


def check_course_staff_office_hours_directory() -> None:
    text = read("docs/course-staff-office-hours-directory.md")
    issues = []

    for role in (
        "Instructor",
        "Course Manager",
        "Head TA",
        "Discussion TA",
        "Project Mentor",
        "Autograder Contact",
    ):
        if f"| {role} |" not in text:
            issues.append(f"missing student-visible staff role: {role}")

    for channel in (
        "Public forum",
        "Private message",
        "Course email",
        "Office Hours queue",
        "LMS / Gradescope",
    ):
        if f"| {channel} |" not in text:
            issues.append(f"missing contact channel row: {channel}")

    for office_hour_type in (
        "Concept / math hours",
        "Coding / debugging hours",
        "Project mentor hours",
        "Regrade support hours",
        "Accessibility / private support",
    ):
        if f"| {office_hour_type} |" not in text:
            issues.append(f"missing office-hours type row: {office_hour_type}")

    for queue_field in (
        "course_item",
        "question_type",
        "command_or_context",
        "first_failure",
        "minimal_reproduction",
        "requested_help",
    ):
        if f"| {queue_field} |" not in text:
            issues.append(f"missing office-hours queue field: {queue_field}")

    for escalation in (
        "公开测试或环境大面积失败",
        "rubric 或成绩复核争议",
        "hidden test leakage 或诚信疑似",
        "项目 scope 或 mentor 分歧",
        "学术便利或个人困难",
        "内容事实错误",
    ):
        if f"| {escalation} |" not in text:
            issues.append(f"missing escalation matrix row: {escalation}")

    for handoff_field in (
        "staff_name",
        "role",
        "contact_scope",
        "office_hours_type",
        "timezone",
        "coverage_weeks",
        "backup_contact",
        "escalation_owner",
        "privacy_notes",
    ):
        if f"| {handoff_field} |" not in text:
            issues.append(f"missing staff handoff field: {handoff_field}")

    for required_phrase in (
        "学生可见",
        "公开目录只展示学生需要的信息",
        "staff-only 权限",
        "不能写核心实现、查看隐藏测试、共享参考解",
        "至少 1 次 concept / math hours 和 1 次 coding / debugging hours",
        "队列只记录问题摘要",
        "影响评分、deadline、policy 或测试口径的答复同步为公告或文档更新",
        "学生站点发布包包含本文件",
        ".venv/bin/python verify_course.py",
    ):
        if required_phrase not in text:
            issues.append(f"missing staff directory phrase: {required_phrase}")

    for linked_doc in (
        "syllabus.md",
        "course-communication-policy.md",
        "discussion-office-hours-guide.md",
        "participation-feedback-guide.md",
        "project-team-mentor-policy.md",
        "staff-runbook.md",
        "python-pytorch-review-session.md",
        "guest-speaker-seminar-policy.md",
        "academic-integrity-case-process.md",
        "course-operations-log.md",
    ):
        if linked_doc not in text:
            issues.append(f"staff/office-hours directory missing linked doc: {linked_doc}")

    communication = read("docs/course-communication-policy.md")
    for communication_marker in (
        "Course Staff and Office Hours Directory",
        "queue policy",
        "escalation matrix",
    ):
        if communication_marker not in communication:
            issues.append(f"communication policy missing staff directory marker: {communication_marker}")

    discussion = read("docs/discussion-office-hours-guide.md")
    for discussion_marker in (
        "Course Staff and Office Hours Directory",
        "students",
    ):
        if discussion_marker == "students":
            continue
        if discussion_marker not in discussion:
            issues.append(f"discussion guide missing staff directory marker: {discussion_marker}")

    project_policy = read("docs/project-team-mentor-policy.md")
    for project_marker in (
        "Course Staff and Office Hours Directory",
        "project mentor hours",
        "queue policy",
        "escalation matrix",
    ):
        if project_marker not in project_policy:
            issues.append(f"project mentor policy missing staff directory marker: {project_marker}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for snapshot_marker in (
        "Instructors / course staff / TAs",
        "Course Staff and Office Hours Directory",
        "Office Hours queue",
        "private routing",
        "escalation matrix",
    ):
        if snapshot_marker not in snapshot:
            issues.append(f"CS224N snapshot missing staff directory marker: {snapshot_marker}")

    crosswalk = read("docs/cs224n-benchmark-crosswalk.md")
    for crosswalk_marker in (
        "Course Staff and Office Hours Directory",
        "staff 角色",
        "Office Hours 类型",
        "queue policy",
        "escalation matrix",
    ):
        if crosswalk_marker not in crosswalk:
            issues.append(f"CS224N crosswalk missing staff directory marker: {crosswalk_marker}")

    if issues:
        fail(f"course staff/office-hours directory is incomplete: {'; '.join(issues[:10])}")
    ok("course staff/office-hours directory covers public staff roles, contact channels, queue policy, and escalation")


def check_course_communication_policy() -> None:
    text = read("docs/course-communication-policy.md")
    issues = []

    for channel in (
        "课程公告",
        "公开讨论区",
        "私密消息或课程邮箱",
        "Office Hours",
        "LMS / Gradescope 等平台",
        "学校正式支持渠道",
    ):
        if f"| {channel} |" not in text:
            issues.append(f"missing communication channel row: {channel}")

    for section in (
        "公告规则",
        "公开讨论区规则",
        "私密渠道规则",
        "Office Hours 规则",
        "评分和复核沟通",
        "课程勘误和内容更正",
        "Staff 使用规范",
    ):
        if f"## {section}" not in text:
            issues.append(f"missing communication section: {section}")

    for required_phrase in (
        "影响评分、截止时间、提交入口、测试口径、项目要求或课程政策",
        "隐藏测试输入、隐藏测试输出或评分脚本细节",
        "个人健康、身份、安全、家庭、便利安排或成绩争议细节",
        "课程组处理私密问题时只共享必要信息",
        "复核可能提高或降低成绩",
        ".venv/bin/python verify_course.py",
        ".venv/bin/python verify_course.py --capstone --training",
        "External Source Verification Guide",
        "不在公开仓库、公开讨论区或公告中记录学生个人敏感信息",
    ):
        if required_phrase not in text:
            issues.append(f"missing communication policy phrase: {required_phrase}")

    for linked_doc in (
        "syllabus.md",
        "discussion-office-hours-guide.md",
        "student-faq-troubleshooting.md",
        "staff-runbook.md",
        "participation-feedback-guide.md",
        "accessibility-student-support.md",
        "course-operations-log.md",
    ):
        if linked_doc not in text:
            issues.append(f"communication policy missing linked doc: {linked_doc}")

    if issues:
        fail(f"course communication policy is incomplete: {'; '.join(issues[:10])}")
    ok("course communication policy covers announcements, public/private channels, office hours, corrections, and privacy boundaries")


def check_course_errata_correction_ledger() -> None:
    text = read("docs/course-errata-correction-ledger.md")
    issues: list[str] = []

    for heading in [
        "Severity Levels",
        "Ledger Schema",
        "Current Errata Ledger",
        "Intake and Triage Workflow",
        "Announcement Template",
        "SLA and Escalation",
        "Cross-Update Rules",
        "Student-Facing Report Form",
        "Release Checklist",
    ]:
        markdown_section(text, heading)

    severity_rows = extract_markdown_table_after(text, "## Severity Levels")
    severities = {cells[0] for cells in severity_rows[1:] if cells}
    required_severities = {"S0 blocker", "S1 grading-impacting", "S2 conceptual", "S3 presentation", "S4 source-drift"}
    missing_severities = sorted(required_severities - severities)
    if missing_severities:
        issues.append(f"errata ledger missing severities: {', '.join(missing_severities)}")
    for cells in severity_rows[1:]:
        if len(cells) != 3:
            issues.append(f"severity row expected 3 cells, got {len(cells)}: {cells[:2]}")

    schema_rows = extract_markdown_table_after(text, "## Ledger Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    required_schema_fields = {
        "errata_id",
        "reported_at",
        "reporter_channel",
        "affected_material",
        "severity",
        "issue_summary",
        "impact_scope",
        "correction_action",
        "verification_evidence",
        "announcement_status",
        "owner",
        "status",
    }
    missing_schema = sorted(required_schema_fields - schema_fields)
    if missing_schema:
        issues.append(f"errata schema missing fields: {', '.join(missing_schema)}")

    ledger_rows = extract_markdown_table_after(text, "## Current Errata Ledger")
    required_errata_ids = {
        "ERR-2026-06-05-CH02-01",
        "ERR-2026-06-05-WORDING-01",
        "ERR-2026-06-05-ARTIFACT-REGISTRY-01",
        "ERR-2026-06-05-PROJECT-DOSSIER-01",
    }
    ledger_ids: set[str] = set()
    valid_announcement_status = {"not_needed", "draft", "posted", "posted_with_regrade", "posted_with_workaround"}
    valid_status = {"open", "fixed_pending_verify", "fixed_announced", "closed"}
    valid_actions = {"keep", "clarify", "patch", "replace", "retire", "regrade", "announce"}
    for cells in ledger_rows[1:]:
        if len(cells) != 12:
            issues.append(f"current errata row expected 12 cells, got {len(cells)}: {cells[:2]}")
            continue
        errata_id, _, _, _, severity, _, impact, action, evidence, announcement, owner, status = cells
        ledger_ids.add(errata_id)
        if severity not in {"S0 blocker", "S1 grading-impacting", "S2 conceptual", "S3 presentation", "S4 source-drift"}:
            issues.append(f"{errata_id}: invalid severity {severity!r}")
        if action not in valid_actions:
            issues.append(f"{errata_id}: invalid correction_action {action!r}")
        if announcement not in valid_announcement_status:
            issues.append(f"{errata_id}: invalid announcement_status {announcement!r}")
        if status not in valid_status:
            issues.append(f"{errata_id}: invalid status {status!r}")
        if not impact or not evidence or not owner:
            issues.append(f"{errata_id}: missing impact/evidence/owner")
    missing_errata_ids = sorted(required_errata_ids - ledger_ids)
    if missing_errata_ids:
        issues.append(f"current errata ledger missing IDs: {', '.join(missing_errata_ids)}")

    workflow_rows = extract_markdown_table_after(text, "## Intake and Triage Workflow")
    required_workflow = {"T1 intake", "T2 classify", "T3 owner", "T4 patch plan", "T5 verify", "T6 announce", "T7 close"}
    workflow_steps = {cells[0] for cells in workflow_rows[1:] if cells}
    missing_workflow = sorted(required_workflow - workflow_steps)
    if missing_workflow:
        issues.append(f"errata workflow missing steps: {', '.join(missing_workflow)}")

    for template_field in (
        "Subject:",
        "Errata ID:",
        "Affected material:",
        "What changed:",
        "Who is affected:",
        "Student action:",
        "Grading or deadline impact:",
        "Verification command or evidence:",
        "Updated documents:",
        "Regrade or support path:",
    ):
        if template_field not in text:
            issues.append(f"announcement template missing field: {template_field}")

    sla_rows = extract_markdown_table_after(text, "## SLA and Escalation")
    sla_severities = {cells[0] for cells in sla_rows[1:] if cells}
    if not required_severities <= sla_severities:
        issues.append("SLA table must cover S0-S4 severities")

    for error_type in (
        "formula / derivation error",
        "source or frontier claim drift",
        "assignment API or test bug",
        "project rubric or dossier ambiguity",
        "site release or rendering bug",
        "grading-impacting issue",
    ):
        if f"| {error_type} |" not in text:
            issues.append(f"cross-update rules missing error type: {error_type}")

    for report_field in (
        "Affected file or page:",
        "Section, exercise, or line if visible:",
        "What seems wrong:",
        "Why it matters:",
        "Minimal reproduction or screenshot:",
        "Whether it affects a submission or grade:",
        "Can this be discussed publicly? yes/no",
    ):
        if report_field not in text:
            issues.append(f"student-facing report form missing field: {report_field}")

    linked_files = {
        "README.md": "Course Errata and Correction Ledger",
        "docs/course-communication-policy.md": "course-errata-correction-ledger.md",
        "docs/material-versioning-archive-policy.md": "course-errata-correction-ledger.md",
        "docs/course-operations-log.md": "course-errata-correction-ledger.md",
        "docs/chapter-source-map.md": "course-errata-correction-ledger.md",
        "docs/chapter-claim-audit-ledger.md": "course-errata-correction-ledger.md",
        "docs/claim-audit-worksheet.md": "course-errata-correction-ledger.md",
        "docs/lecture-notes-quality-review.md": "course-errata-correction-ledger.md",
        "scripts/build_course_site_release.py": "course-errata-correction-ledger.md",
        "scripts/generate_course_evidence_manifest.py": "docs/course-errata-correction-ledger.md",
    }
    for path, marker in linked_files.items():
        if marker not in read(path):
            issues.append(f"{path} missing errata ledger marker: {marker}")

    if issues:
        fail(f"course errata/correction ledger incomplete: {'; '.join(issues[:12])}")
    ok(
        "course errata/correction ledger covers severity, schema, current fixes, workflow, "
        f"SLA, cross-update rules, report form, and release links ({len(ledger_ids)} records)"
    )


def check_enrollment_audit_public_use_policy() -> None:
    text = read("docs/enrollment-audit-public-use-policy.md")
    issues = []

    for role in (
        "正式选课 / enrolled for credit",
        "Credit / No Credit",
        "旁听 / auditor",
        "自学者 / public learner",
        "Teaching staff / mentor",
    ):
        if f"| {role} |" not in text:
            issues.append(f"missing enrollment role row: {role}")

    for resource in (
        "公开章节与学生站点",
        "assignment release",
        "LMS / Gradescope",
        "hidden tests 与评分脚本",
        "`reference_solution.py`",
        "compute credits",
        "project mentor",
        "私密沟通渠道",
    ):
        if f"| {resource} |" not in text:
            issues.append(f"missing platform/access row: {resource}")

    for required_phrase in (
        "official transcript",
        "course credit",
        "certificate",
        "public tests passing does not imply course credit",
        "只有在学校正式注册系统中完成选课",
        "archived 或 retired 材料可以作为历史参考",
        "scripts/build_course_site_release.py",
        "scripts/build_assignment_release.py",
        "LMS / Gradescope roster",
        "hidden tests",
        "reference_solution.py",
        "compute credits",
        "project mentor",
        ".venv/bin/python verify_course.py --capstone --training",
    ):
        if required_phrase not in text:
            issues.append(f"missing enrollment policy phrase: {required_phrase}")

    for linked_doc in (
        "syllabus.md",
        "course-communication-policy.md",
        "material-versioning-archive-policy.md",
        "assignment-submission-guide.md",
        "course-policies.md",
        "project-team-mentor-policy.md",
        "compute-resource-guide.md",
        "accessibility-student-support.md",
        "course-materials-index.md",
    ):
        if linked_doc not in text:
            issues.append(f"enrollment policy missing linked doc: {linked_doc}")

    if issues:
        fail(f"enrollment/audit/public-use policy is incomplete: {'; '.join(issues[:10])}")
    ok("enrollment/audit/public-use policy covers enrolled, auditor, self-study, grading, and access boundaries")


def check_lecture_media_access_policy() -> None:
    text = read("docs/lecture-media-access-policy.md")
    issues = []

    for media_type in (
        "live stream",
        "current lecture recording",
        "public historical video",
        "demo screencast",
        "caption / transcript",
        "classroom photo / board capture",
    ):
        if f"| {media_type} |" not in text:
            issues.append(f"missing lecture media row: {media_type}")

    for access_requirement in (
        "caption / transcript",
        "visual alternative",
        "async access",
        "media quality",
        "correction path",
    ):
        if f"| {access_requirement} |" not in text:
            issues.append(f"missing accessibility media row: {access_requirement}")

    for record_field in (
        "lecture_id",
        "media_type",
        "audience",
        "platform",
        "current_or_archived",
        "accessibility_asset",
        "privacy_review",
        "linked_materials",
    ):
        if f"| {record_field} |" not in text:
            issues.append(f"missing media record field: {record_field}")

    for required_phrase in (
        "CS224N Winter 2026",
        "Canvas/Panopto",
        "non enrolled students",
        "enrolled students",
        "public learner",
        "课后 24-72 小时",
        "字幕、文字稿或 structured summary",
        "hidden tests",
        "reference_solution.py",
        "API key",
        "archived / retired 视频不得作为本轮作业、quiz、项目或评分依据",
        "scripts/build_course_site_release.py",
        ".venv/bin/python verify_course.py --capstone --training",
    ):
        if required_phrase not in text:
            issues.append(f"missing lecture media phrase: {required_phrase}")

    for linked_doc in (
        "course-materials-index.md",
        "lecture-notes-index.md",
        "lecture-slide-outline.md",
        "demo-runbook.md",
        "enrollment-audit-public-use-policy.md",
        "course-communication-policy.md",
        "accessibility-student-support.md",
        "material-versioning-archive-policy.md",
    ):
        if linked_doc not in text:
            issues.append(f"lecture media policy missing linked doc: {linked_doc}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for snapshot_marker in (
        "| Lecture videos |",
        "Canvas/Panopto",
        "public historical video",
        "lecture-media-access-policy.md",
    ):
        if snapshot_marker not in snapshot:
            issues.append(f"CS224N snapshot missing lecture-media marker: {snapshot_marker}")

    if issues:
        fail(f"lecture media access policy is incomplete: {'; '.join(issues[:10])}")
    ok("lecture media access policy covers live stream, recordings, transcripts, privacy, and public media boundaries")


def check_course_calendar_deadline_ledger() -> None:
    text = read("docs/course-calendar-deadline-ledger.md")
    issues = []

    for field in (
        "term",
        "timezone",
        "lecture_date",
        "release_at",
        "due_at",
        "grace_or_late_policy",
        "regrade_open_at",
        "regrade_close_at",
        "source_of_truth",
        "change_log",
    ):
        if f"| {field} |" not in text:
            issues.append(f"missing calendar field: {field}")

    for week in range(1, 11):
        if f"| Week {week} |" not in text:
            issues.append(f"missing week ledger row: Week {week}")

    for deliverable in (
        "A1 Ch01-Ch02",
        "A2 Ch03",
        "A3 Ch04-Ch05",
        "A4 Ch06",
        "A5 Ch07",
        "A6 Ch08",
        "A7 Ch09",
        "A8 Ch11 classic NLP",
        "A9 Ch10",
        "Training capstone proposal",
        "Training capstone milestone",
        "Inference capstone proposal",
        "Final report/poster",
    ):
        if f"| {deliverable} |" not in text:
            issues.append(f"missing deadline ledger row: {deliverable}")

    for change_type in (
        "release_at 改动",
        "due_at 延后",
        "due_at 提前",
        "regrade window 改动",
        "hidden test 或 rubric 改动",
        "project deadline 改动",
    ):
        if f"| {change_type} |" not in text:
            issues.append(f"missing deadline change-control row: {change_type}")

    for freeze_point in (
        "作业 release 前 24 小时",
        "作业 due 前 24 小时",
        "项目 due 前 72 小时",
        "期末提交窗口",
    ):
        if f"| {freeze_point} |" not in text:
            issues.append(f"missing release-freeze row: {freeze_point}")

    for review_session in (
        "Python Review Session",
        "PyTorch Tutorial Session",
    ):
        if f"| {review_session} |" not in text:
            issues.append(f"missing review-session ledger row: {review_session}")

    for required_phrase in (
        "CS224N Winter 2026",
        "schedule/deadline",
        "single source of truth",
        "LMS / Gradescope",
        "课堂口头说明、讨论区回复或私信不能单独改变正式截止时间",
        "archived / retired materials 的旧 deadline 不作为本轮课程依据",
        "成绩发布后 7 天",
        "学校期末提交窗口",
        "至少提前一周公告",
        ".venv/bin/python verify_course.py --capstone --training",
    ):
        if required_phrase not in text:
            issues.append(f"missing deadline-ledger phrase: {required_phrase}")

    for linked_doc in (
        "syllabus.md",
        "lecture-plan.md",
        "course-materials-index.md",
        "assignment-submission-guide.md",
        "capstone-proposal-milestone.md",
        "course-communication-policy.md",
        "enrollment-audit-public-use-policy.md",
        "course-operations-log.md",
    ):
        if linked_doc not in text:
            issues.append(f"deadline ledger missing linked doc: {linked_doc}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for snapshot_marker in (
        "| Schedule and deadlines |",
        "Course Calendar and Deadline Ledger",
        "release freeze",
        "deadline change announcement",
    ):
        if snapshot_marker not in snapshot:
            issues.append(f"CS224N snapshot missing calendar marker: {snapshot_marker}")

    if issues:
        fail(f"course calendar/deadline ledger is incomplete: {'; '.join(issues[:10])}")
    ok("course calendar/deadline ledger covers schedule, release/due dates, late days, regrade windows, and change control")


def check_python_pytorch_review_session() -> None:
    text = read("docs/python-pytorch-review-session.md")
    issues = []

    for session in ("Python Review Session", "PyTorch Tutorial Session"):
        if f"| {session} |" not in text:
            issues.append(f"missing review session row: {session}")

    for agenda_item in (
        "环境 smoke test",
        "函数与测试",
        "字典与 pair counting",
        "non-overlapping merge",
        "Tensor shape contract",
        "Embedding lookup",
        "next-token CE",
        "autograd",
        "debug drill",
    ):
        if agenda_item not in text:
            issues.append(f"missing review agenda item: {agenda_item}")

    for failure_mode in (
        "工作目录错误",
        "模块选择错误",
        "dtype 错误",
        "shape 错误",
        "device 错误",
        "静默吞异常",
    ):
        if f"| {failure_mode} |" not in text:
            issues.append(f"missing review failure mode: {failure_mode}")

    for required_phrase in (
        "CS224N Winter 2026",
        "Week 1 Python Review Session",
        "Week 2 PyTorch Tutorial Session",
        '.venv/bin/python -c "import sys, torch;',
        "STUDENT_MODULE=starter .venv/bin/python assignments/ch01_bpe/tests.py",
        "STUDENT_MODULE=starter .venv/bin/python assignments/ch02_embeddings/tests.py",
        "[B,T,D] 到 logits",
        "[B*T,V]",
        "loss.backward()",
        "First failing test",
        "Question for office hours",
        ".venv/bin/python verify_course.py --capstone --training",
    ):
        if required_phrase not in text:
            issues.append(f"missing Python/PyTorch review phrase: {required_phrase}")

    for linked_doc in (
        "prerequisite-diagnostic.md",
        "math-prerequisites.md",
        "environment-reproducibility.md",
        "course-calendar-deadline-ledger.md",
        "lecture-plan.md",
        "student-faq-troubleshooting.md",
        "assignment-submission-guide.md",
    ):
        if linked_doc not in text:
            issues.append(f"Python/PyTorch review missing linked doc: {linked_doc}")

    snapshot = read("docs/cs224n-current-benchmark-snapshot.md")
    for snapshot_marker in (
        "| Python/PyTorch review sessions |",
        "Python and PyTorch Review Session",
        "Week 1 Python Review Session",
        "Week 2 PyTorch Tutorial Session",
    ):
        if snapshot_marker not in snapshot:
            issues.append(f"CS224N snapshot missing review-session marker: {snapshot_marker}")

    if issues:
        fail(f"Python/PyTorch review session is incomplete: {'; '.join(issues[:10])}")
    ok("Python/PyTorch review session covers environment smoke tests, Ch01/Ch02 drills, CE/autograd, and debugging evidence")


def check_assignment_scaffold() -> None:
    assignments_dir = ROOT / "assignments"
    if not assignments_dir.exists():
        fail("missing assignments directory")

    discovered = sorted(path.parent.name for path in assignments_dir.glob("ch*/tests.py"))
    if discovered != EXPECTED_ASSIGNMENTS:
        fail(f"expected assignment suites {EXPECTED_ASSIGNMENTS}, got {discovered}")

    required_files = ["README.md", "starter.py", "reference_solution.py", "tests.py"]
    for assignment in EXPECTED_ASSIGNMENTS:
        suite_dir = assignments_dir / assignment
        for name in required_files:
            path = suite_dir / name
            if not path.exists():
                fail(f"missing assignment file: {assignment}/{name}")
            if path.stat().st_size == 0:
                fail(f"empty assignment file: {assignment}/{name}")

        readme = (suite_dir / "README.md").read_text(encoding="utf-8")
        if "STUDENT_MODULE=starter" not in readme:
            fail(f"{assignment}/README.md missing student-module run instruction")
        if "评分 Rubric" not in readme:
            fail(f"{assignment}/README.md missing grading rubric")
        if "书面" not in readme and "Written questions" not in readme:
            fail(f"{assignment}/README.md missing written-explanation grading component")
        rubric = readme.split("评分 Rubric", 1)[1]
        rubric = rubric.split("\n## ", 1)[0]
        scores = [
            int(match.group(1))
            for line in rubric.splitlines()
            if (match := re.match(r"^\|[^|]+\|\s*(\d+)\s*\|", line))
        ]
        if sum(scores) != 100:
            fail(f"{assignment}/README.md rubric scores must sum to 100, got {sum(scores)}")

    root_readme = read("README.md")
    for assignment in EXPECTED_ASSIGNMENTS:
        if f"assignments/{assignment}/" not in root_readme:
            fail(f"README missing assignment link: assignments/{assignment}/")

    ok(f"assignment scaffold is complete for {len(EXPECTED_ASSIGNMENTS)} chapter suites")


def check_rubric_weight_tables() -> None:
    checks = []
    handout = read("docs/assignment-handout-pack.md")
    assignment_rubric_mismatches = []
    for assignment_number in range(1, len(EXPECTED_ASSIGNMENTS) + 1):
        handout_rows = extract_first_score_rows(handout, f"## Assignment {assignment_number}:")
        assignment = EXPECTED_ASSIGNMENTS[assignment_number - 1]
        readme_rows = extract_first_score_rows(
            read(f"assignments/{assignment}/README.md"),
            "## 评分 Rubric",
        )
        if readme_rows != handout_rows:
            assignment_rubric_mismatches.append(
                f"{assignment}: README {readme_rows} != handout {handout_rows}"
            )
        checks.append((
            f"Assignment Handout Pack assignment {assignment_number}",
            [score for _, score in handout_rows],
            100,
        ))

    checks.extend([
        (
            "Project report rubric common scoring",
            extract_first_score_table(read("docs/project-report-rubric.md"), "## 通用评分"),
            100,
        ),
        (
            "Presentation rubric",
            extract_first_score_table(read("docs/presentation-peer-review.md"), "## 展示评分"),
            100,
        ),
        (
            "Peer review rubric",
            extract_first_score_table(read("docs/presentation-peer-review.md"), "Review 质量评分"),
            100,
        ),
        (
            "Participation rubric",
            extract_first_score_table(read("docs/participation-feedback-guide.md"), "## 参与评分 Rubric"),
            10,
        ),
    ])

    bad = []
    for label, scores, expected in checks:
        total = sum(scores)
        if total != expected:
            bad.append(f"{label}: expected {expected}, got {total}")
    if bad:
        fail(f"rubric score totals are inconsistent: {'; '.join(bad)}")
    if assignment_rubric_mismatches:
        fail(f"assignment README rubrics differ from handout: {'; '.join(assignment_rubric_mismatches[:5])}")
    ok(f"rubric score totals and assignment README/handout weights are consistent ({len(checks)} tables)")


def markdown_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        fail(f"missing markdown section: {heading}")
    next_match = re.search(r"^##\s+", text[match.end() :], re.MULTILINE)
    end = match.end() + next_match.start() if next_match else len(text)
    return text[match.end() : end]


def count_numbered_questions(section: str) -> int:
    return len(re.findall(r"(?m)^\d+\.\s+", section))


def count_bullets_between(section: str, start_marker: str, end_marker: str | None = None) -> int:
    if start_marker not in section:
        return 0
    body = section.split(start_marker, 1)[1]
    if end_marker and end_marker in body:
        body = body.split(end_marker, 1)[0]
    return len(re.findall(r"(?m)^-\s+", body))


def check_frontier_seminar_handout() -> None:
    text = read("docs/frontier-seminar-handout.md")
    seminars = [
        "Seminar 0: Benchmarking, Evaluation, and Reasoning Evidence",
        "Seminar 1: Interpretability",
        "Seminar 2: Multimodality",
        "Seminar 3: Social and Broader Impacts",
        "Seminar 4: Open Questions in NLP and LLM Engineering",
    ]
    issues = []

    for heading in seminars:
        section = markdown_section(text, heading)
        target_bullets = count_bullets_between(section, "目标：", "建议阅读：")
        reading_bullets = count_bullets_between(section, "建议阅读：", "课堂问题：")
        question_count = count_numbered_questions(section.split("最低交付：", 1)[0])
        deliverable_bullets = count_bullets_between(section, "最低交付：")
        reading_block = section.split("建议阅读：", 1)[1].split("课堂问题：", 1)[0]
        external_urls = EXTERNAL_URL_RE.findall(reading_block)
        if target_bullets < 3:
            issues.append(f"{heading}: expected at least 3 target bullets, got {target_bullets}")
        if reading_bullets < 3:
            issues.append(f"{heading}: expected at least 3 reading bullets, got {reading_bullets}")
        if not external_urls:
            issues.append(f"{heading}: suggested readings need at least one external source URL")
        if question_count < 3:
            issues.append(f"{heading}: expected at least 3 classroom questions, got {question_count}")
        if deliverable_bullets < 3:
            issues.append(f"{heading}: expected at least 3 deliverable bullets, got {deliverable_bullets}")

    rubric_scores = extract_first_score_table(text, "## 评分 Rubric")
    if sum(rubric_scores) != 100:
        issues.append(f"frontier seminar rubric scores must sum to 100, got {sum(rubric_scores)}")

    for marker in [
        "来源使用规则",
        "External Source Inventory",
        "CS224N Current Benchmark Snapshot",
        "当前 Schedule 主题证据矩阵",
        "Benchmarking and Evaluation",
        "Reasoning",
        "项目或产品场景中的风险登记",
        "学生项目不得把 seminar 讨论当作未经验证的产品能力声明",
    ]:
        if marker not in text:
            issues.append(f"frontier seminar handout missing marker: {marker}")

    if issues:
        fail(f"frontier seminar handout incomplete: {'; '.join(issues[:10])}")
    ok(f"frontier seminar handout covers {len(seminars)} advanced discussion topics")


def check_classic_nlp_handout_depth() -> None:
    handout = read("docs/classic-nlp-handout.md")
    assignment = read("assignments/ch11_classic_nlp/README.md")
    written = read("docs/written-problem-set.md")
    instructor = read("docs/instructor-solution-guide.md")
    coverage = read("docs/nlp-evaluation-coverage.md")
    issues = []

    for heading in [
        "1. Dependency Parsing",
        "2. Seq2Seq / Neural Machine Translation",
        "3. Encoder-only / BERT",
        "4. Evaluation",
        "5. Ethics / Safety",
        "课堂活动建议",
        "Mini-Recitation Checklist",
    ]:
        if f"## {heading}" not in handout:
            issues.append(f"classic NLP handout missing section: {heading}")

    for marker in [
        "Worked Example: `I saw her`",
        "| Step | Stack | Buffer | Action | New arc |",
        "LEFT-ARC(nsubj)",
        "RIGHT-ARC(obj)",
        "Worked Example: Beam Search Length Bias",
        "normalized score `sum / length`",
        "length penalty",
        "Worked Example: BERT-style MLM Tensor",
        "[CLS] the [MASK] [MASK] [SEP]",
        "loss positions",
        "Metric Failure Cases",
        "LLM judge preference",
        "Mini-Recitation Checklist",
    ]:
        if marker not in handout:
            issues.append(f"classic NLP handout missing marker: {marker}")

    recitation = markdown_section(handout, "Mini-Recitation Checklist")
    for topic in ("Dependency parsing", "Seq2Seq / NMT", "BERT / MLM", "Evaluation", "Ethics / Safety"):
        if f"| {topic} |" not in recitation:
            issues.append(f"mini-recitation checklist missing topic: {topic}")

    for marker in [
        "Written Drill Expectations",
        "stack / buffer / arcs transition table",
        "length-normalized score",
        "loss positions",
        "metric failure case",
    ]:
        if marker not in assignment:
            issues.append(f"Ch11 assignment README missing classic NLP depth marker: {marker}")

    for marker in [
        "arc-standard transition system",
        "beam search length bias",
        "MLM 与 causal LM",
        "BLEU、ROUGE、F1、exact match",
    ]:
        if marker not in written:
            issues.append(f"written problem set missing classic NLP marker: {marker}")

    for marker in [
        "transition 序列必须保持 stack/buffer 合法",
        "beam length bias",
        "MLM 双向看上下文",
        "LLM-as-judge",
    ]:
        if marker not in instructor:
            issues.append(f"instructor solution guide missing classic NLP marker: {marker}")

    for marker in [
        "transition-based parsing",
        "beam search",
        "masked language modeling",
        "bootstrap confidence interval",
    ]:
        if marker not in coverage:
            issues.append(f"NLP evaluation coverage missing classic NLP marker: {marker}")

    if issues:
        fail(f"classic NLP handout lacks CS224N-style depth: {'; '.join(issues[:10])}")
    ok("classic NLP handout includes worked parsing, beam search, BERT MLM, metric failure, and recitation evidence")


def check_classic_nlp_deep_dive_module() -> None:
    module = read("docs/classic-nlp-deep-dive-module.md")
    coverage = read("docs/nlp-evaluation-coverage.md")
    lecture_plan = read("docs/lecture-plan.md")
    materials_index = read("docs/course-materials-index.md")
    slide_outline = read("docs/lecture-slide-outline.md")
    reading_list = read("docs/reading-list.md")
    audit = read("docs/university-course-quality-audit.md")
    issues = []

    for section in (
        "## Module Outcomes",
        "## Suggested Lecture Split",
        "## Dependency Parsing Deep Dive",
        "## Seq2Seq / NMT Deep Dive",
        "## Encoder-only / BERT Deep Dive",
        "## Assessment Pack",
        "## Teaching Misconception Register",
        "## Source And Update Boundary",
    ):
        if section not in module:
            issues.append(f"deep-dive module missing section: {section}")

    for outcome in ("CL-NLP-1", "CL-NLP-2", "CL-NLP-3", "CL-NLP-4", "CL-NLP-5"):
        if f"| {outcome} |" not in module:
            issues.append(f"deep-dive module missing outcome: {outcome}")

    for marker in (
        "Arc-Standard Oracle Example",
        "Neural Parser Feature Template",
        "UAS = count",
        "LAS = count",
        "p(y | x) = prod_t",
        "teacher forcing",
        "exposure bias",
        "alpha_{t,i} = softmax_i",
        "Beam Search Algorithm",
        "score_norm(y)",
        "L_MLM = - sum",
        "ignore index",
        "Encoder Fine-tuning Patterns",
        "| dimension | encoder-only | encoder-decoder | decoder-only |",
        "DP-1",
        "S2S-2",
        "BERT-1",
        "Teaching Misconception Register",
    ):
        if marker not in module:
            issues.append(f"deep-dive module missing marker: {marker}")

    lecture_split = markdown_section(module, "Suggested Lecture Split")
    for split_label in ("10 周压缩版", "12 周扩展版 A", "12 周扩展版 B", "12 周扩展版 C", "12 周扩展版 D"):
        if split_label not in lecture_split:
            issues.append(f"deep-dive module missing lecture split: {split_label}")

    assessment = markdown_section(module, "Assessment Pack")
    for check_id in ("DP-1", "DP-2", "S2S-1", "S2S-2", "BERT-1", "BERT-2"):
        if check_id not in assessment:
            issues.append(f"assessment pack missing check: {check_id}")
    for function_name in (
        "attachment_scores",
        "sentence_bleu",
        "rouge_l_f1",
        "exact_match_and_f1",
        "build_mlm_example",
    ):
        if function_name not in assessment:
            issues.append(f"assessment pack missing programming evidence: {function_name}")

    for upstream_text, upstream_name in (
        (coverage, "NLP evaluation coverage"),
        (lecture_plan, "lecture plan"),
        (materials_index, "course materials index"),
        (slide_outline, "lecture slide outline"),
        (reading_list, "reading list"),
        (audit, "university course quality audit"),
    ):
        if "classic-nlp-deep-dive-module.md" not in upstream_text and "Classic NLP Deep-Dive Teaching Module" not in upstream_text:
            issues.append(f"{upstream_name} missing deep-dive module link")

    if issues:
        fail(f"classic NLP deep-dive module incomplete: {'; '.join(issues[:10])}")
    ok("classic NLP deep-dive module covers dependency parsing, seq2seq, BERT, assessment, and misconceptions")


def check_project_report_template() -> None:
    text = read("docs/project-report-template.md")
    sections = [
        "Title and Metadata",
        "Abstract",
        "Problem Definition",
        "Method and Implementation",
        "Data, Ethics, and Limitations",
        "Experiments",
        "Results",
        "Error Analysis",
        "Cost and Reproducibility",
        "Contributions and Disclosure",
        "Conclusion and Open Questions",
        "Final Submission Checklist",
        "TA Review Checklist",
    ]
    issues = []
    for heading in sections:
        markdown_section(text, heading)

    for marker in [
        "所有数字必须能从命令、日志、配置或评测文件复现",
        "Primary reproduction command",
        "Repository commit or submission version",
        "Data source",
        "License",
        "PII / privacy",
        "Baseline",
        "Changed variable",
        "Reproduction command",
        "至少 3 个失败案例",
        "P50/P95/P99 latency",
        ".venv/bin/python verify_course.py --capstone --training",
        "AI 工具使用环节",
        "高风险 claim 有来源和适用边界",
    ]:
        if marker not in text:
            issues.append(f"project report template missing marker: {marker}")

    final_checklist = markdown_section(text, "Final Submission Checklist")
    checklist_items = re.findall(r"(?m)^\| [A-Za-z].+\|", final_checklist)
    if len(checklist_items) < 10:
        issues.append(f"final submission checklist expected at least 10 rows, got {len(checklist_items)}")

    ta_checklist = markdown_section(text, "TA Review Checklist")
    ta_bullets = re.findall(r"(?m)^-\s+", ta_checklist)
    if len(ta_bullets) < 5:
        issues.append(f"TA review checklist expected at least 5 bullets, got {len(ta_bullets)}")

    linked_docs = [
        "docs/project-report-rubric.md",
        "docs/default-final-project-guide.md",
        "docs/capstone-proposal-milestone.md",
        "docs/course-materials-index.md",
        "docs/syllabus.md",
        "README.md",
    ]
    for doc_path in linked_docs:
        doc = read(doc_path)
        if "project-report-template.md" not in doc:
            issues.append(f"{doc_path} missing project report template link")

    if issues:
        fail(f"project report template incomplete: {'; '.join(issues[:10])}")
    ok("project report template has reproducibility, evidence, and TA review checks")


def check_project_report_exemplar_pack() -> None:
    text = read("docs/project-report-exemplar-pack.md")
    template = read("docs/project-report-template.md")
    rubric = read("docs/project-report-rubric.md")
    showcase = read("docs/final-project-showcase-archive-policy.md")
    gallery = read("docs/capstone-project-gallery.md")
    readme = read("README.md")
    issues = []

    for section in (
        "## Use Rules",
        "## Exemplar Overview",
        "## EX-INF-A-01: Inference Engineering A-Band Exemplar",
        "## EX-TRAIN-B-01: Training Engineering B-Band Exemplar",
        "## EX-DEFAULT-C-01: Default Final Project C-Band Exemplar",
        "## EX-NP-FAIL-01: Not-Passing Exemplar",
        "## Rubric Mapping",
        "## Exemplar Review Worksheet",
        "## Archive Boundary",
    ):
        if section not in text:
            issues.append(f"missing section: {section}")

    for exemplar_id in ("EX-INF-A-01", "EX-TRAIN-B-01", "EX-DEFAULT-C-01", "EX-NP-FAIL-01"):
        if exemplar_id not in text:
            issues.append(f"missing exemplar id: {exemplar_id}")

    for marker in (
        "synthetic_status",
        "score_band",
        "student_visible",
        "archive_boundary",
        "public_boundary",
        "A",
        "B",
        "C",
        "not_passing",
        "split_card",
        "metric_card",
        "uncertainty_record",
        "claim_audit",
        "artifact_manifest",
        "archived_label",
        "hidden tests",
        "staff-only grading packet",
        "不能冒充 archived public report",
    ):
        if marker not in text:
            issues.append(f"missing exemplar marker: {marker}")

    for rubric_dimension in (
        "问题定义",
        "复现性",
        "实验设计",
        "指标选择",
        "错误分析",
        "工程判断",
        "数据与伦理",
        "贡献与归档",
    ):
        if f"| {rubric_dimension} |" not in text:
            issues.append(f"rubric mapping missing dimension: {rubric_dimension}")

    for upstream_text, upstream_name in (
        (template, "project report template"),
        (rubric, "project report rubric"),
        (showcase, "showcase/archive policy"),
        (gallery, "capstone project gallery"),
        (readme, "README"),
    ):
        if "project-report-exemplar-pack.md" not in upstream_text:
            issues.append(f"{upstream_name} missing project exemplar pack link")

    if issues:
        fail(f"project report exemplar pack incomplete: {'; '.join(issues[:10])}")
    ok("project report exemplar pack covers A/B/C/not-passing synthetic report evidence")


def check_safety_societal_impact_casebook() -> None:
    text = read("docs/safety-societal-impact-casebook.md")
    issues = []

    for marker in [
        "Safety and Societal Impact Casebook",
        "复核日期：2026-06-05",
        "Case Analysis Schema",
        "Core Cases",
        "Classroom Use",
        "Assessment Rubric",
        "Staff Review Workflow",
        "Release Checklist",
        "data-ethics-review.md",
        "frontier-seminar-handout.md",
        "project-report-template.md",
        "project-report-rubric.md",
        "reading-discussion-question-bank.md",
        "chapter-source-map.md",
        "external-source-verification.md",
        "experimental-rigor-evaluation-statistics.md",
        "course-policies.md",
        "student site release",
    ]:
        if marker not in text:
            issues.append(f"missing safety/societal impact casebook marker: {marker}")

    schema_rows = extract_markdown_table_after(text, "## Case Analysis Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    for field in ["case_id", "scenario", "primary_risk", "evidence_to_collect", "mitigation", "residual_risk", "course_link"]:
        if field not in schema_fields:
            issues.append(f"safety casebook schema missing field: {field}")

    case_rows = extract_markdown_table_after(text, "## Core Cases")
    if len(case_rows) < 11:
        issues.append(f"expected at least 10 safety cases plus header, got {len(case_rows)}")
    case_ids = set()
    risk_types = set()
    for cells in case_rows[1:]:
        if len(cells) != 7:
            issues.append(f"safety case row expected 7 cells, got {len(cells)}: {cells[:2]}")
            continue
        case_id, _scenario, primary_risk, evidence, mitigation, residual_risk, course_link = cells
        case_ids.add(case_id)
        risk_types.add(primary_risk)
        if not case_id.startswith("SSI-"):
            issues.append(f"safety case id must start with SSI-: {case_id}")
        if not evidence or not mitigation or not residual_risk or not course_link:
            issues.append(f"{case_id} missing evidence, mitigation, residual risk, or course link")

    for case_id in [
        "SSI-RAG-MED",
        "SSI-HIRING-BIAS",
        "SSI-RAG-PII",
        "SSI-BENCH-LEAK",
        "SSI-PROMPT-INJECT",
        "SSI-COPYRIGHT-DATA",
        "SSI-DUAL-USE",
        "SSI-ACCESS-COST",
        "SSI-LLM-JUDGE",
        "SSI-SAFETY-LOGS",
    ]:
        if case_id not in case_ids:
            issues.append(f"safety casebook missing case: {case_id}")

    for risk_type in ["privacy", "bias", "safety", "contamination", "misuse", "copyright", "access", "evaluation"]:
        if risk_type not in risk_types:
            issues.append(f"safety casebook missing primary risk: {risk_type}")
    if "governance" not in text:
        issues.append("safety casebook missing governance risk marker")

    classroom_rows = extract_markdown_table_after(text, "## Classroom Use")
    classroom_ids = {cells[0] for cells in classroom_rows[1:] if cells}
    for use_id in ["SSI-U-DISCUSS", "SSI-U-RECITATION", "SSI-U-PROPOSAL", "SSI-U-FINAL", "SSI-U-REVIEW"]:
        if use_id not in classroom_ids:
            issues.append(f"safety casebook missing classroom use: {use_id}")
    for cells in classroom_rows[1:]:
        if len(cells) != 4:
            issues.append(f"classroom use row expected 4 cells, got {len(cells)}: {cells[:2]}")

    rubric_rows = extract_markdown_table_after(text, "## Assessment Rubric")
    rubric_dimensions = {cells[0] for cells in rubric_rows[1:] if cells}
    for dimension in ["Risk specificity", "Evidence quality", "Mitigation realism", "Residual risk", "Course connection"]:
        if dimension not in rubric_dimensions:
            issues.append(f"safety casebook missing rubric dimension: {dimension}")

    for workflow_marker in [
        "Week 8-10",
        "project proposal review",
        "Learning Analytics and Remediation Plan",
        "public archive",
        "private data",
        "exploit steps",
    ]:
        if workflow_marker not in text:
            issues.append(f"safety casebook staff workflow missing marker: {workflow_marker}")

    for release_marker in [
        "real sensitive data",
        "exploit steps",
        "private grading samples",
        "hidden tests",
        "reference_solution.py",
        "real student submissions",
    ]:
        if release_marker not in text:
            issues.append(f"safety casebook release boundary missing marker: {release_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/data-ethics-review.md",
        "docs/frontier-seminar-handout.md",
        "docs/project-report-rubric.md",
        "docs/project-report-template.md",
        "docs/reading-discussion-question-bank.md",
        "docs/assessment-blueprint-coverage-matrix.md",
    ]
    for doc_path in linked_docs:
        if "safety-societal-impact-casebook.md" not in read(doc_path):
            issues.append(f"{doc_path} missing safety/societal impact casebook link")

    if "safety-societal-impact-casebook.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing safety/societal impact casebook")
    if "docs/safety-societal-impact-casebook.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing safety/societal impact casebook")

    if issues:
        fail(f"safety/societal impact casebook is incomplete: {'; '.join(issues[:10])}")
    ok("safety/societal impact casebook covers cases, risk types, classroom use, rubric, workflow, release boundaries, and links")


def check_model_benchmark_card_guide() -> None:
    text = read("docs/model-benchmark-card-guide.md")
    issues = []

    for marker in [
        "Model and Benchmark Card Guide",
        "复核日期：2026-06-05",
        "Card Schema",
        "Model Card Checklist",
        "Benchmark Card Checklist",
        "Course Card Examples",
        "Claim Rewrite Rules",
        "Student Submission Template",
        "Staff Review Workflow",
        "Release Checklist",
        "external-source-verification.md",
        "external-source-inventory.md",
        "chapter-source-map.md",
        "chapter-claim-audit-ledger.md",
        "project-report-template.md",
        "experimental-rigor-evaluation-statistics.md",
        "dataset-model-artifact-registry.md",
        "data-ethics-review.md",
        "safety-societal-impact-casebook.md",
        "capstone-proposal-milestone.md",
        "reading-discussion-question-bank.md",
        "student site release",
    ]:
        if marker not in text:
            issues.append(f"missing model/benchmark card guide marker: {marker}")

    schema_rows = extract_markdown_table_after(text, "## Card Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    for field in [
        "card_id",
        "source_kind",
        "source_record",
        "claimed_property",
        "configuration",
        "supported_claim",
        "unsupported_claim",
        "verification_action",
        "course_link",
    ]:
        if field not in schema_fields:
            issues.append(f"model/benchmark card schema missing field: {field}")

    model_rows = extract_markdown_table_after(text, "## Model Card Checklist")
    model_ids = {cells[0] for cells in model_rows[1:] if cells}
    for check_id in [
        "MBC-MODEL-ID",
        "MBC-MODEL-DATE",
        "MBC-MODEL-CONTEXT",
        "MBC-MODEL-TRAINING",
        "MBC-MODEL-LICENSE",
        "MBC-MODEL-SAFETY",
        "MBC-MODEL-ACCESS",
        "MBC-MODEL-VOLATILITY",
    ]:
        if check_id not in model_ids:
            issues.append(f"model card checklist missing check: {check_id}")
    for cells in model_rows[1:]:
        if len(cells) != 5:
            issues.append(f"model card row expected 5 cells, got {len(cells)}: {cells[:2]}")

    benchmark_rows = extract_markdown_table_after(text, "## Benchmark Card Checklist")
    benchmark_ids = {cells[0] for cells in benchmark_rows[1:] if cells}
    for check_id in [
        "MBC-BENCH-TASK",
        "MBC-BENCH-DATA",
        "MBC-BENCH-PROMPT",
        "MBC-BENCH-METRIC",
        "MBC-BENCH-BASELINE",
        "MBC-BENCH-HARDWARE",
        "MBC-BENCH-CONTAM",
        "MBC-BENCH-UNCERT",
        "MBC-BENCH-SLO",
    ]:
        if check_id not in benchmark_ids:
            issues.append(f"benchmark card checklist missing check: {check_id}")
    for cells in benchmark_rows[1:]:
        if len(cells) != 5:
            issues.append(f"benchmark card row expected 5 cells, got {len(cells)}: {cells[:2]}")

    example_rows = extract_markdown_table_after(text, "## Course Card Examples")
    example_ids = {cells[0] for cells in example_rows[1:] if cells}
    for example_id in [
        "MBC-EX-VOLATILE-CONTEXT",
        "MBC-EX-SERVING-BENCH",
        "MBC-EX-RAG-QUALITY",
        "MBC-EX-LEADERBOARD",
        "MBC-EX-API-PRICE",
    ]:
        if example_id not in example_ids:
            issues.append(f"model/benchmark card examples missing example: {example_id}")
    for cells in example_rows[1:]:
        if len(cells) != 6:
            issues.append(f"model/benchmark example row expected 6 cells, got {len(cells)}: {cells[:2]}")

    rule_rows = extract_markdown_table_after(text, "## Claim Rewrite Rules")
    rule_ids = {cells[0] for cells in rule_rows[1:] if cells}
    for rule_id in ["MBC-R1", "MBC-R2", "MBC-R3", "MBC-R4", "MBC-R5", "MBC-R6"]:
        if rule_id not in rule_ids:
            issues.append(f"claim rewrite rules missing rule: {rule_id}")
    for cells in rule_rows[1:]:
        if len(cells) != 4:
            issues.append(f"claim rewrite rule row expected 4 cells, got {len(cells)}: {cells[:2]}")

    for template_marker in [
        "card_id:",
        "source_kind:",
        "source_record:",
        "access_date:",
        "source_tier:",
        "supported_claim:",
        "unsupported_claim:",
        "verification_action:",
        "course_link:",
    ]:
        if template_marker not in text:
            issues.append(f"student submission template missing marker: {template_marker}")

    for workflow_marker in [
        "model card",
        "benchmark",
        "source tier",
        "access date",
        "frontier-source-audit.md",
        "graded assessment",
    ]:
        if workflow_marker not in text:
            issues.append(f"model/benchmark staff workflow missing marker: {workflow_marker}")

    for release_marker in [
        "hidden tests",
        "reference_solution.py",
        "private grading samples",
        "real student submissions",
    ]:
        if release_marker not in text:
            issues.append(f"model/benchmark release boundary missing marker: {release_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/project-report-template.md",
        "docs/experimental-rigor-evaluation-statistics.md",
        "docs/external-source-verification.md",
        "docs/external-source-inventory.md",
        "docs/data-ethics-review.md",
        "docs/capstone-proposal-milestone.md",
        "docs/reading-discussion-question-bank.md",
        "docs/chapter-source-map.md",
        "docs/university-course-quality-audit.md",
    ]
    for doc_path in linked_docs:
        if "model-benchmark-card-guide.md" not in read(doc_path):
            issues.append(f"{doc_path} missing model/benchmark card guide link")

    if "model-benchmark-card-guide.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing model/benchmark card guide")
    if "docs/model-benchmark-card-guide.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing model/benchmark card guide")

    if issues:
        fail(f"model/benchmark card guide is incomplete: {'; '.join(issues[:10])}")
    ok("model/benchmark card guide covers schemas, checklists, examples, rewrite rules, templates, workflow, release boundaries, and links")


def check_capstone_defense_oral_exam_bank() -> None:
    text = read("docs/capstone-defense-oral-exam-bank.md")
    issues = []

    for marker in [
        "Capstone Defense and Oral Exam Question Bank",
        "复核日期：2026-06-05",
        "Defense Format",
        "Question Schema",
        "Core Defense Questions",
        "Track-Specific Follow-Ups",
        "Scoring Rubric",
        "Sampling Rules",
        "Oral Record Template",
        "Staff Workflow",
        "Release Checklist",
        "presentation-peer-review.md",
        "project-report-template.md",
        "project-report-rubric.md",
        "project-submission-dossier.md",
        "capstone-proposal-milestone.md",
        "project-team-mentor-policy.md",
        "experimental-rigor-evaluation-statistics.md",
        "model-benchmark-card-guide.md",
        "data-ethics-review.md",
        "safety-societal-impact-casebook.md",
        "final-project-showcase-archive-policy.md",
        "assessment-administration-policy.md",
        "academic-integrity-case-process.md",
        "student site release",
    ]:
        if marker not in text:
            issues.append(f"missing capstone defense/oral exam marker: {marker}")

    format_rows = extract_markdown_table_after(text, "## Defense Format")
    format_ids = {cells[0] for cells in format_rows[1:] if cells}
    for format_id in ["DEF-GROUP-QA", "DEF-ROTATING", "DEF-INDIVIDUAL", "DEF-REMEDIAL", "DEF-ARCHIVE"]:
        if format_id not in format_ids:
            issues.append(f"defense format missing: {format_id}")
    for cells in format_rows[1:]:
        if len(cells) != 5:
            issues.append(f"defense format row expected 5 cells, got {len(cells)}: {cells[:2]}")

    schema_rows = extract_markdown_table_after(text, "## Question Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    for field in [
        "question_id",
        "category",
        "prompt",
        "strong_answer_evidence",
        "weak_answer_signal",
        "course_link",
    ]:
        if field not in schema_fields:
            issues.append(f"defense question schema missing field: {field}")

    core_rows = extract_markdown_table_after(text, "## Core Defense Questions")
    core_ids = set()
    categories = set()
    for cells in core_rows[1:]:
        if len(cells) != 6:
            issues.append(f"core defense question row expected 6 cells, got {len(cells)}: {cells[:2]}")
            continue
        question_id, category, _prompt, strong_evidence, weak_signal, course_link = cells
        core_ids.add(question_id)
        categories.add(category)
        if not question_id.startswith("DEF-"):
            issues.append(f"core defense question id must start with DEF-: {question_id}")
        if not strong_evidence or not weak_signal or not course_link:
            issues.append(f"{question_id} missing evidence, weak signal, or course link")
    for question_id in [
        "DEF-CONTRIB-01",
        "DEF-CONTRIB-02",
        "DEF-METHOD-01",
        "DEF-METHOD-02",
        "DEF-METHOD-03",
        "DEF-EXP-01",
        "DEF-EXP-02",
        "DEF-EXP-03",
        "DEF-EXP-04",
        "DEF-EXP-05",
        "DEF-REPRO-01",
        "DEF-REPRO-02",
        "DEF-SOURCE-01",
        "DEF-SOURCE-02",
        "DEF-SAFETY-01",
        "DEF-SAFETY-02",
        "DEF-FAIL-01",
        "DEF-FAIL-02",
        "DEF-COMM-01",
        "DEF-COMM-02",
    ]:
        if question_id not in core_ids:
            issues.append(f"core defense questions missing: {question_id}")
    for category in [
        "contribution",
        "method",
        "experiment",
        "reproducibility",
        "source",
        "safety",
        "failure",
        "communication",
    ]:
        if category not in categories:
            issues.append(f"core defense questions missing category: {category}")

    followup_rows = extract_markdown_table_after(text, "## Track-Specific Follow-Ups")
    followup_ids = {cells[0] for cells in followup_rows[1:] if cells}
    tracks = {cells[1] for cells in followup_rows[1:] if len(cells) >= 2}
    for question_id in [
        "DEF-TRAIN-01",
        "DEF-TRAIN-02",
        "DEF-TRAIN-03",
        "DEF-INFER-01",
        "DEF-INFER-02",
        "DEF-INFER-03",
        "DEF-DEFAULT-01",
        "DEF-DEFAULT-02",
    ]:
        if question_id not in followup_ids:
            issues.append(f"track-specific follow-ups missing: {question_id}")
    for track in ["training", "inference", "default"]:
        if track not in tracks:
            issues.append(f"track-specific follow-ups missing track: {track}")
    for cells in followup_rows[1:]:
        if len(cells) != 5:
            issues.append(f"track-specific follow-up row expected 5 cells, got {len(cells)}: {cells[:2]}")

    rubric_rows = extract_markdown_table_after(text, "## Scoring Rubric")
    rubric_dimensions = {cells[0] for cells in rubric_rows[1:] if cells}
    for dimension in [
        "evidence grounding",
        "technical ownership",
        "claim discipline",
        "reproducibility",
        "risk awareness",
    ]:
        if dimension not in rubric_dimensions:
            issues.append(f"defense scoring rubric missing dimension: {dimension}")
    for cells in rubric_rows[1:]:
        if len(cells) != 4:
            issues.append(f"defense scoring rubric row expected 4 cells, got {len(cells)}: {cells[:2]}")

    sampling_rows = extract_markdown_table_after(text, "## Sampling Rules")
    sampling_ids = {cells[0] for cells in sampling_rows[1:] if cells}
    for rule_id in [
        "DEF-SAMPLE-CO4",
        "DEF-SAMPLE-CO5",
        "DEF-SAMPLE-SAFETY",
        "DEF-SAMPLE-TEAM",
        "DEF-SAMPLE-REMEDIAL",
    ]:
        if rule_id not in sampling_ids:
            issues.append(f"defense sampling rules missing: {rule_id}")
    for cells in sampling_rows[1:]:
        if len(cells) != 3:
            issues.append(f"defense sampling rule row expected 3 cells, got {len(cells)}: {cells[:2]}")

    for template_marker in [
        "defense_id:",
        "project_id:",
        "student_or_team:",
        "format_id:",
        "question_ids:",
        "evidence_checked:",
        "answer_summary:",
        "rubric_dimension:",
        "score_or_decision:",
        "downgrade_decision:",
        "follow_up_required:",
    ]:
        if template_marker not in text:
            issues.append(f"oral record template missing marker: {template_marker}")

    for workflow_marker in [
        "question_ids",
        "evidence_checked",
        "answer_summary",
        "Project Submission Dossier",
        "Academic Integrity Case Process",
        "Course Errata and Correction Ledger",
        "individual oral follow-up",
    ]:
        if workflow_marker not in text:
            issues.append(f"defense staff workflow missing marker: {workflow_marker}")

    for release_marker in [
        "hidden tests",
        "reference_solution.py",
        "private grading samples",
        "real student submissions",
        "未公开评分脚本",
    ]:
        if release_marker not in text:
            issues.append(f"defense release boundary missing marker: {release_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/presentation-peer-review.md",
        "docs/project-report-rubric.md",
        "docs/project-report-template.md",
        "docs/project-submission-dossier.md",
        "docs/capstone-proposal-milestone.md",
        "docs/final-project-showcase-archive-policy.md",
        "docs/project-team-mentor-policy.md",
        "docs/assessment-blueprint-coverage-matrix.md",
        "docs/university-course-quality-audit.md",
    ]
    for doc_path in linked_docs:
        if "capstone-defense-oral-exam-bank.md" not in read(doc_path):
            issues.append(f"{doc_path} missing capstone defense/oral exam bank link")

    if "capstone-defense-oral-exam-bank.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing capstone defense/oral exam bank")
    if "docs/capstone-defense-oral-exam-bank.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing capstone defense/oral exam bank")

    if issues:
        fail(f"capstone defense/oral exam bank is incomplete: {'; '.join(issues[:10])}")
    ok("capstone defense/oral exam bank covers formats, schema, questions, follow-ups, rubric, sampling, oral records, workflow, release boundaries, and links")


def check_programming_assignment_code_quality_rubric() -> None:
    text = read("docs/programming-assignment-code-quality-rubric.md")
    issues = []

    for marker in [
        "Programming Assignment Code Quality Rubric",
        "复核日期：2026-06-05",
        "Rubric Dimensions",
        "Assignment-Specific Review Cues",
        "Manual Review Triggers",
        "Student Self-Check",
        "TA Review Workflow",
        "Release Checklist",
        "assignment-handout-pack.md",
        "assignment-submission-guide.md",
        "autograder-hidden-tests.md",
        "grading-calibration.md",
        "staff-assistance-code-review-policy.md",
        "academic-integrity-case-process.md",
        "notation-shape-glossary.md",
        "environment-reproducibility.md",
        "python-pytorch-review-session.md",
        "assessment-blueprint-coverage-matrix.md",
        "learning-outcome-attainment-report.md",
        "student site release",
    ]:
        if marker not in text:
            issues.append(f"missing programming code quality rubric marker: {marker}")

    dimension_rows = extract_markdown_table_after(text, "## Rubric Dimensions")
    dimension_ids = {cells[0] for cells in dimension_rows[1:] if cells}
    for dimension_id in [
        "CQR-API",
        "CQR-SHAPE",
        "CQR-VECTOR",
        "CQR-NUMERIC",
        "CQR-DEVICE",
        "CQR-BOUNDARY",
        "CQR-READABLE",
        "CQR-REPRO",
        "CQR-INTEGRITY",
    ]:
        if dimension_id not in dimension_ids:
            issues.append(f"code quality rubric missing dimension: {dimension_id}")
    for cells in dimension_rows[1:]:
        if len(cells) != 6:
            issues.append(f"code quality dimension row expected 6 cells, got {len(cells)}: {cells[:2]}")

    cue_rows = extract_markdown_table_after(text, "## Assignment-Specific Review Cues")
    cue_ids = {cells[0] for cells in cue_rows[1:] if cells}
    for cue_id in [f"CQR-CH{index:02d}" for index in range(1, 12)]:
        if cue_id not in cue_ids:
            issues.append(f"code quality rubric missing assignment cue: {cue_id}")
    for cells in cue_rows[1:]:
        if len(cells) != 5:
            issues.append(f"assignment-specific cue row expected 5 cells, got {len(cells)}: {cells[:2]}")

    trigger_rows = extract_markdown_table_after(text, "## Manual Review Triggers")
    trigger_ids = {cells[0] for cells in trigger_rows[1:] if cells}
    for trigger_id in [
        "CQR-TRIG-PUBLIC-HIDDEN",
        "CQR-TRIG-HARDCODE",
        "CQR-TRIG-REFERENCE",
        "CQR-TRIG-API",
        "CQR-TRIG-NUMERIC",
        "CQR-TRIG-DEVICE",
        "CQR-TRIG-READABILITY",
    ]:
        if trigger_id not in trigger_ids:
            issues.append(f"manual review triggers missing: {trigger_id}")
    for cells in trigger_rows[1:]:
        if len(cells) != 4:
            issues.append(f"manual review trigger row expected 4 cells, got {len(cells)}: {cells[:2]}")

    self_check_rows = extract_markdown_table_after(text, "## Student Self-Check")
    self_check_ids = {cells[0] for cells in self_check_rows[1:] if cells}
    for check_id in [
        "CQR-SC-API",
        "CQR-SC-SHAPE",
        "CQR-SC-BOUNDARY",
        "CQR-SC-NUMERIC",
        "CQR-SC-DEVICE",
        "CQR-SC-REPRO",
        "CQR-SC-INTEGRITY",
    ]:
        if check_id not in self_check_ids:
            issues.append(f"student self-check missing: {check_id}")
    for cells in self_check_rows[1:]:
        if len(cells) != 3:
            issues.append(f"student self-check row expected 3 cells, got {len(cells)}: {cells[:2]}")

    for workflow_marker in [
        "public",
        "hidden_boundary",
        "hidden_property",
        "API contract",
        "dtype/device",
        "hardcoding",
        "CQR dimension_id",
        "Course Operations and Improvement Log",
        "Academic Integrity Case Process",
    ]:
        if workflow_marker not in text:
            issues.append(f"code quality TA workflow missing marker: {workflow_marker}")

    for release_marker in [
        "hidden tests",
        "reference_solution.py",
        "private grading samples",
        "real student submissions",
        "未公开评分脚本",
    ]:
        if release_marker not in text:
            issues.append(f"code quality release boundary missing marker: {release_marker}")

    linked_docs = [
        "README.md",
        "docs/syllabus.md",
        "docs/assignment-handout-pack.md",
        "docs/assignment-submission-guide.md",
        "docs/autograder-hidden-tests.md",
        "docs/grading-calibration.md",
        "docs/staff-assistance-code-review-policy.md",
        "docs/assessment-blueprint-coverage-matrix.md",
        "docs/learning-outcome-attainment-report.md",
        "docs/university-course-quality-audit.md",
    ]
    for doc_path in linked_docs:
        if "programming-assignment-code-quality-rubric.md" not in read(doc_path):
            issues.append(f"{doc_path} missing programming code quality rubric link")

    if "programming-assignment-code-quality-rubric.md" not in read("scripts/build_course_site_release.py"):
        issues.append("course site release safe docs missing programming code quality rubric")
    if "docs/programming-assignment-code-quality-rubric.md" not in read("scripts/generate_course_evidence_manifest.py"):
        issues.append("course evidence manifest missing programming code quality rubric")

    if issues:
        fail(f"programming assignment code quality rubric is incomplete: {'; '.join(issues[:10])}")
    ok("programming assignment code quality rubric covers dimensions, assignment cues, manual triggers, self-check, TA workflow, release boundaries, and links")


def check_experimental_rigor_evaluation_statistics() -> None:
    text = read("docs/experimental-rigor-evaluation-statistics.md")
    issues = []

    for heading in [
        "Scope",
        "Evaluation Split Protocol",
        "Metric Selection and Limits",
        "Uncertainty and Confidence Intervals",
        "Significance Claim Gate",
        "Error Analysis and Failure Taxonomy",
        "Contamination and Leakage Gate",
        "Minimum Evidence Packet",
        "TA Audit Checklist",
        "发布前 Checklist",
    ]:
        markdown_section(text, heading)

    for marker in [
        "split_id",
        "train_source",
        "dev_policy",
        "test_policy",
        "leakage_check",
        "bootstrap confidence interval",
        "95% CI",
        "repeated-run seed sensitivity",
        "paired comparison",
        "load-test variance",
        "single_seed_limit",
        "significantly better / 显著提升",
        "robust / 稳健",
        "faster / 更快",
        "generalizes / 泛化",
        "train/test duplicate",
        "prompt leakage",
        "retrieval contamination",
        "benchmark contamination",
        "hidden test leakage",
        "experiment_table",
        "split_card",
        "metric_card",
        "uncertainty_record",
        "failure_cases",
        "resource_record",
        "claim_audit",
    ]:
        if marker not in text:
            issues.append(f"experimental rigor guide missing marker: {marker}")

    split_table = markdown_section(text, "Evaluation Split Protocol")
    for row in ("split_id", "train_source", "dev_policy", "test_policy", "leakage_check"):
        if f"| {row} |" not in split_table:
            issues.append(f"experimental rigor split table missing row: {row}")

    claim_gate = markdown_section(text, "Significance Claim Gate")
    for claim in ("significantly better / 显著提升", "robust / 稳健", "faster / 更快", "safer / 更安全", "generalizes / 泛化"):
        if claim not in claim_gate:
            issues.append(f"experimental rigor claim gate missing claim: {claim}")

    linked_docs = [
        "docs/project-report-template.md",
        "docs/project-report-rubric.md",
        "docs/nlp-evaluation-coverage.md",
        "docs/data-ethics-review.md",
        "docs/course-materials-index.md",
        "docs/syllabus.md",
        "docs/cs224n-benchmark-crosswalk.md",
        "docs/cs224n-current-benchmark-snapshot.md",
        "README.md",
    ]
    for doc_path in linked_docs:
        doc = read(doc_path)
        if "experimental-rigor-evaluation-statistics.md" not in doc:
            issues.append(f"{doc_path} missing experimental rigor guide link")

    template = read("docs/project-report-template.md")
    for marker in ("split_card", "metric_card", "uncertainty_record", "claim_audit", "significance claim gate"):
        if marker not in template:
            issues.append(f"project report template missing experimental rigor marker: {marker}")

    rubric = read("docs/project-report-rubric.md")
    for marker in ("confidence interval", "seed sensitivity", "single_seed_limit", "split_card", "metric_card", "uncertainty_record", "claim_audit"):
        if marker not in rubric:
            issues.append(f"project report rubric missing experimental rigor marker: {marker}")

    evaluation = read("docs/nlp-evaluation-coverage.md")
    for marker in ("bootstrap confidence interval", "seed sensitivity", "contamination/leakage gate", "uncertainty_record"):
        if marker not in evaluation:
            issues.append(f"NLP evaluation coverage missing experimental rigor marker: {marker}")

    if issues:
        fail(f"experimental rigor/evaluation statistics guide is incomplete: {'; '.join(issues[:10])}")
    ok("experimental rigor/evaluation statistics guide covers split protocol, uncertainty, claim gates, leakage checks, and TA audit evidence")


def check_written_assessment_alignment() -> None:
    written = read("docs/written-problem-set.md")
    instructor = read("docs/instructor-solution-guide.md")
    calibration = read("docs/grading-calibration.md")
    selection_matrix = instructor.split("## Ch01 Tokenization / BPE", 1)[0]
    selection_matrix_labels = {
        "Ch01 Tokenization / BPE": "Ch01 Tokenization / BPE",
        "Ch02 Embedding / Position Encoding / RoPE": "Ch02 Embedding / RoPE",
        "Ch03 Scaled Dot-Product Attention": "Ch03 Attention",
        "Ch04 MHA / GQA / MLA": "Ch04 MHA / GQA / MLA",
        "Ch05 Transformer Block / Norm / FFN": "Ch05 Block / Norm / FFN",
        "Ch06 GPT Assembly / MoE": "Ch06 GPT / MoE",
        "Ch07 Training Loop": "Ch07 Training",
        "Ch08 Generation / Decoding": "Ch08 Generation",
        "Ch09 Fine-tuning / Alignment": "Ch09 Alignment",
        "Ch10 Inference / RAG / Serving": "Ch10 Inference",
        "经典 NLP 专题": "经典 NLP 专题",
    }
    issues = []

    for written_heading, instructor_heading, min_questions in EXPECTED_WRITTEN_ASSESSMENT_SECTIONS:
        written_section = markdown_section(written, written_heading)
        question_count = count_numbered_questions(written_section)
        if question_count < min_questions:
            issues.append(
                f"{written_heading}: expected at least {min_questions} written questions, got {question_count}"
            )

        instructor_section = markdown_section(instructor, instructor_heading)
        answer_bullets = count_bullets_between(instructor_section, "答案要点：", "常见扣分：")
        deduction_bullets = count_bullets_between(instructor_section, "常见扣分：")
        if answer_bullets < 3:
            issues.append(f"{instructor_heading}: expected at least 3 answer-key bullets, got {answer_bullets}")
        if deduction_bullets < 3:
            issues.append(f"{instructor_heading}: expected at least 3 common-deduction bullets, got {deduction_bullets}")

        matrix_label = selection_matrix_labels[instructor_heading]
        if matrix_label not in selection_matrix:
            issues.append(f"{instructor_heading}: missing from written problem selection matrix")

    required_calibration_markers = [
        "## 双评一致性规则",
        "### BPE Merge",
        "### RoPE 相对位置",
        "### Attention Scaling 与 Mask",
        "### DPO / GRPO",
        "### KV Cache 显存",
        "## 校准记录模板",
    ]
    for marker in required_calibration_markers:
        if marker not in calibration:
            issues.append(f"grading calibration missing marker: {marker}")

    if issues:
        fail(f"written assessment alignment incomplete: {'; '.join(issues[:10])}")
    ok(
        "written problem set, instructor guide, and grading calibration are aligned "
        f"({len(EXPECTED_WRITTEN_ASSESSMENT_SECTIONS)} sections)"
    )


def check_grading_anchor_sample_feedback_pack() -> None:
    text = read("docs/grading-anchor-sample-feedback-pack.md")
    calibration = read("docs/grading-calibration.md")
    gradebook = read("docs/gradebook-lms-operations.md")
    readme = read("README.md")
    issues = []

    required_sections = [
        "## Use Rules",
        "## Written Anchor Samples",
        "## Programming Anchor Samples",
        "## Capstone Anchor Samples",
        "## Reading And Peer Review Anchor Samples",
        "## Regrade Anchor Samples",
        "## Feedback Templates",
        "## Double-Grading Resolution",
        "## Release Checklist",
    ]
    for section in required_sections:
        if section not in text:
            issues.append(f"missing section: {section}")

    required_anchors = [
        "WR-ROPE-FULL-01",
        "WR-ROPE-PARTIAL-01",
        "WR-ATTN-NOTPASS-01",
        "CODE-BPE-FULL-01",
        "CODE-ATTN-PARTIAL-01",
        "CODE-GEN-BORDERLINE-01",
        "CAP-INF-FULL-01",
        "CAP-TRAIN-PARTIAL-01",
        "CAP-NOTPASS-01",
        "READ-FULL-01",
        "PEER-LOW-01",
        "RG-MASK-UP-01",
        "RG-CAP-DOWN-01",
    ]
    for anchor in required_anchors:
        if anchor not in text:
            issues.append(f"missing anchor sample: {anchor}")

    for field in (
        "anchor_id",
        "rubric_item",
        "score",
        "evidence",
        "feedback_to_student",
        "calibration_note",
        "second_reader_delta",
        "final_decision",
        "original_score",
        "revised_score",
    ):
        if field not in text:
            issues.append(f"missing anchor field: {field}")

    for category in ("full_credit", "partial_credit", "borderline", "not_passing"):
        if category not in text:
            issues.append(f"missing score category: {category}")

    for linked_doc in (
        "grading-calibration.md",
        "instructor-solution-guide.md",
        "assignment-handout-pack.md",
        "autograder-hidden-tests.md",
        "project-report-rubric.md",
        "presentation-peer-review.md",
        "gradebook-lms-operations.md",
    ):
        if linked_doc not in text:
            issues.append(f"grading anchor pack missing linked doc: {linked_doc}")

    for release_guard in (
        "no hidden tests",
        "hidden test exact input",
        "no reference_solution.py",
        "`reference_solution.py`",
        "public-safe feedback",
        "rubric traceability",
        "gradebook traceability",
    ):
        if release_guard not in text:
            issues.append(f"missing release guard: {release_guard}")

    for phrase in (
        "second_reader_delta <= 3%",
        "3% < second_reader_delta <= 8%",
        "second_reader_delta > 8%",
        "release_batch",
        "rubric_version",
        "regrade_decision_id",
        "student_visible_feedback",
    ):
        if phrase not in text:
            issues.append(f"missing double-grading or gradebook phrase: {phrase}")

    if text.count("feedback_to_student") < 14:
        issues.append("expected feedback_to_student in every anchor sample plus template")
    if text.count("calibration_note") < 14:
        issues.append("expected calibration_note in every anchor sample plus template")
    if text.count("anchor_id") < 15:
        issues.append("expected anchor_id coverage across samples and templates")

    for upstream_doc, name in (
        (calibration, "grading calibration"),
        (gradebook, "gradebook/LMS guide"),
        (readme, "README"),
    ):
        if "grading-anchor-sample-feedback-pack.md" not in upstream_doc:
            issues.append(f"{name} missing grading anchor pack link")

    if issues:
        fail(f"grading anchor sample feedback pack incomplete: {'; '.join(issues[:10])}")
    ok(f"grading anchor sample feedback pack covers {len(required_anchors)} anchor samples")


def check_grading_drift_audit_ledger() -> None:
    text = read("docs/grading-drift-audit-ledger.md")
    issues: list[str] = []

    for heading in [
        "Drift Signals",
        "Calibration Session Schema",
        "Current Calibration Sessions",
        "Double-Grading Sampling Plan",
        "Drift Audit Metrics",
        "Pause and Recalibration Triggers",
        "Regrade and Batch Correction Linkage",
        "Staff Review Workflow",
        "Release Checklist",
    ]:
        markdown_section(text, heading)

    signal_rows = extract_markdown_table_after(text, "## Drift Signals")
    signal_ids = {cells[0] for cells in signal_rows[1:] if cells}
    required_signals = {
        "GD-DELTA-03",
        "GD-DELTA-08",
        "GD-RUBRIC-AMB",
        "GD-HIDDEN-BUG",
        "GD-DIST-SHIFT",
        "GD-CAPSTONE-CLAIM",
        "GD-REGRADES",
    }
    missing_signals = sorted(required_signals - signal_ids)
    if missing_signals:
        issues.append(f"grading drift ledger missing signals: {', '.join(missing_signals)}")
    for cells in signal_rows[1:]:
        if len(cells) != 4:
            issues.append(f"drift signal row expected 4 cells, got {len(cells)}: {cells[:2]}")

    schema_rows = extract_markdown_table_after(text, "## Calibration Session Schema")
    schema_fields = {cells[0] for cells in schema_rows[1:] if cells}
    required_schema = {
        "session_id",
        "assignment_id",
        "release_batch",
        "rubric_version",
        "graders",
        "anchor_samples",
        "sample_size",
        "disagreement_summary",
        "rule_added_or_clarified",
        "follow_up_owner",
        "status",
    }
    missing_schema = sorted(required_schema - schema_fields)
    if missing_schema:
        issues.append(f"calibration session schema missing fields: {', '.join(missing_schema)}")

    session_rows = extract_markdown_table_after(text, "## Current Calibration Sessions")
    session_ids = {cells[0] for cells in session_rows[1:] if cells}
    required_sessions = {"CAL-2026-CH02-PRE", "CAL-2026-CH03-PRE", "CAL-2026-CAPSTONE-PRE"}
    missing_sessions = sorted(required_sessions - session_ids)
    if missing_sessions:
        issues.append(f"current calibration sessions missing IDs: {', '.join(missing_sessions)}")
    for cells in session_rows[1:]:
        if len(cells) != 11:
            issues.append(f"calibration session row expected 11 cells, got {len(cells)}: {cells[:2]}")
            continue
        if cells[10] not in {"planned", "in_progress", "resolved", "escalated"}:
            issues.append(f"{cells[0]} has invalid status {cells[10]!r}")

    sampling_rows = extract_markdown_table_after(text, "## Double-Grading Sampling Plan")
    sampling_types = {cells[0] for cells in sampling_rows[1:] if cells}
    required_sampling = {
        "written derivations",
        "programming assignments",
        "project proposal/milestone",
        "final report/capstone",
        "regrade requests",
    }
    missing_sampling = sorted(required_sampling - sampling_types)
    if missing_sampling:
        issues.append(f"double-grading sampling plan missing types: {', '.join(missing_sampling)}")

    metric_rows = extract_markdown_table_after(text, "## Drift Audit Metrics")
    metric_ids = {cells[0] for cells in metric_rows[1:] if cells}
    required_metrics = {
        "mean_second_reader_delta",
        "high_delta_rate",
        "regrade_change_rate",
        "upward_regrade_bias",
        "hidden_category_mismatch_count",
        "capstone_log_mismatch_rate",
        "anchor_coverage",
    }
    missing_metrics = sorted(required_metrics - metric_ids)
    if missing_metrics:
        issues.append(f"drift audit metrics missing: {', '.join(missing_metrics)}")

    for trigger in (
        "GD-DELTA-08 appears twice on same rubric item",
        "hidden-test category feedback is wrong",
        "rubric interpretation changes after grading begins",
        "grade distribution outlier by grader",
        "capstone A-band reports lack reproducible logs",
    ):
        if f"| {trigger} |" not in text:
            issues.append(f"pause/recalibration trigger missing: {trigger}")

    for linkage_field in (
        "regrade_decision_id",
        "release_batch",
        "rubric_version",
        "affected_students",
        "calibration_update_needed",
        "errata_id",
    ):
        if f"| {linkage_field} |" not in text:
            issues.append(f"regrade/batch linkage missing field: {linkage_field}")

    for workflow_phrase in (
        "Before grading",
        "During grading",
        "Before release",
        "After release",
        "End of term",
    ):
        if workflow_phrase not in text:
            issues.append(f"staff review workflow missing phrase: {workflow_phrase}")

    linked_files = {
        "docs/grading-calibration.md": "grading-drift-audit-ledger.md",
        "docs/grading-anchor-sample-feedback-pack.md": "grading-drift-audit-ledger.md",
        "docs/gradebook-lms-operations.md": "grading-drift-audit-ledger.md",
        "docs/course-operations-log.md": "grading-drift-audit-ledger.md",
        "docs/staff-runbook.md": "grading-drift-audit-ledger.md",
        "scripts/generate_course_evidence_manifest.py": "docs/grading-drift-audit-ledger.md",
        "scripts/build_course_site_release.py": "grading-drift-audit-ledger.md",
    }
    for path, marker in linked_files.items():
        if marker not in read(path):
            issues.append(f"{path} missing grading drift ledger marker: {marker}")

    builder = read("scripts/build_course_site_release.py")
    if "grading-drift-audit-ledger.md" not in builder.split("EXCLUDED_DOCS = [", 1)[1].split("]", 1)[0]:
        issues.append("course site release builder must exclude grading-drift-audit-ledger.md")

    if issues:
        fail(f"grading drift audit ledger incomplete: {'; '.join(issues[:12])}")
    ok(
        "grading drift audit ledger covers drift signals, session schema, current calibrations, "
        f"sampling, metrics, pause triggers, linkage, and student-release exclusion ({len(signal_ids)} signals)"
    )


def check_ta_training_certification() -> None:
    text = read("docs/ta-training-certification.md")
    issues = []

    for marker in [
        "TA Training and Certification Dossier",
        "复核日期：2026-06-05",
        "Certification Scope",
        "Competency Modules",
        "Certification Matrix",
        "Calibration Practicum",
        "Office Hours Simulation Bank",
        "Privacy, Accessibility, and Integrity Scenario Bank",
        "Current Certification Ledger",
        "Recertification and Escalation",
        "Release Checklist",
        "staff-facing certification record",
        "不进入 student site release",
        "staff-runbook.md",
        "grading-calibration.md",
        "grading-drift-audit-ledger.md",
        "private-autograder-operations.md",
        "academic-integrity-case-process.md",
    ]:
        if marker not in text:
            issues.append(f"missing TA certification marker: {marker}")

    scope_rows = extract_markdown_table_after(text, "## Certification Scope")
    roles = {cells[0] for cells in scope_rows[1:] if cells}
    for role in ["Head TA", "Discussion TA", "Project Mentor", "Autograder Contact", "Course Manager"]:
        if role not in roles:
            issues.append(f"TA certification missing role: {role}")
    for cells in scope_rows[1:]:
        if len(cells) != 4:
            issues.append(f"TA certification scope row expected 4 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not all(cells[1:]):
            issues.append(f"{cells[0]} missing certification scope field")

    module_rows = extract_markdown_table_after(text, "## Competency Modules")
    module_ids = {cells[0] for cells in module_rows[1:] if cells}
    for module_id in ["TA-CONTENT", "TA-GRADING", "TA-DEBUG", "TA-AUTOGRADER", "TA-PROJECT", "TA-PRIVACY", "TA-COMMS"]:
        if module_id not in module_ids:
            issues.append(f"TA certification missing competency module: {module_id}")

    matrix_rows = extract_markdown_table_after(text, "## Certification Matrix")
    if len(matrix_rows) < 6:
        issues.append(f"TA certification matrix too short: {len(matrix_rows)} rows")
    for cells in matrix_rows[1:]:
        if len(cells) != 8:
            issues.append(f"TA certification matrix row expected 8 cells, got {len(cells)}: {cells[:2]}")
            continue
        if "required" not in cells[1:]:
            issues.append(f"{cells[0]} must have at least one required module")

    practicum_rows = extract_markdown_table_after(text, "## Calibration Practicum")
    practicum_ids = {cells[0] for cells in practicum_rows[1:] if cells}
    for practicum_id in ["CAL-WRITTEN-01", "CAL-CODE-01", "CAL-CAPSTONE-01", "CAL-RECAP-01", "CAL-DRIFT-01"]:
        if practicum_id not in practicum_ids:
            issues.append(f"TA certification missing practicum: {practicum_id}")

    office_rows = extract_markdown_table_after(text, "## Office Hours Simulation Bank")
    office_ids = {cells[0] for cells in office_rows[1:] if cells}
    for scenario_id in ["OH-SHAPE-01", "OH-ROPE-01", "OH-TRAIN-01", "OH-RUBRIC-01", "OH-PROJECT-01"]:
        if scenario_id not in office_ids:
            issues.append(f"TA certification missing office-hours scenario: {scenario_id}")
    for cells in office_rows[1:]:
        if len(cells) != 4:
            issues.append(f"office-hours simulation row expected 4 cells, got {len(cells)}: {cells[:2]}")
            continue
        if not cells[2] or not cells[3]:
            issues.append(f"{cells[0]} missing expected or forbidden response")

    privacy_rows = extract_markdown_table_after(text, "## Privacy, Accessibility, and Integrity Scenario Bank")
    privacy_ids = {cells[0] for cells in privacy_rows[1:] if cells}
    for scenario_id in ["PAI-ACCESS-01", "PAI-HEALTH-01", "PAI-INTEGRITY-01", "PAI-TEAM-01", "PAI-GRADE-01"]:
        if scenario_id not in privacy_ids:
            issues.append(f"TA certification missing privacy/integrity scenario: {scenario_id}")

    ledger_rows = extract_markdown_table_after(text, "## Current Certification Ledger")
    if len(ledger_rows) < 7:
        issues.append(f"expected at least 6 certification records, got {max(0, len(ledger_rows) - 1)}")
    for cells in ledger_rows[1:]:
        if len(cells) != 6:
            issues.append(f"TA certification ledger row expected 6 cells, got {len(cells)}: {cells[:2]}")
            continue
        if cells[5] != "ready":
            issues.append(f"{cells[0]} certification status must be ready, got {cells[5]}")
        if not cells[4]:
            issues.append(f"{cells[0]} missing reviewer")

    recert_rows = extract_markdown_table_after(text, "## Recertification and Escalation")
    recert_triggers = " ".join(cells[0] for cells in recert_rows[1:] if cells)
    for trigger_phrase in [
        "new assignment or rubric changed",
        "hidden-test bug or category mismatch",
        "grading drift threshold exceeded",
        "new project modality",
        "accessibility or integrity routing mistake",
        "over-boundary code help",
    ]:
        if trigger_phrase not in recert_triggers:
            issues.append(f"TA certification missing recertification trigger: {trigger_phrase}")

    for unsafe_marker in [
        "reference_solution.py",
        "hidden input",
        "私有评分脚本",
        "真实学生姓名",
        "accommodation 细节",
    ]:
        if unsafe_marker not in text:
            issues.append(f"TA certification missing safety boundary marker: {unsafe_marker}")

    linked_files = {
        "README.md": "ta-training-certification.md",
        "docs/staff-runbook.md": "ta-training-certification.md",
        "docs/grading-calibration.md": "ta-training-certification.md",
        "docs/grading-drift-audit-ledger.md": "ta-training-certification.md",
        "scripts/generate_course_evidence_manifest.py": "docs/ta-training-certification.md",
        "scripts/build_course_site_release.py": "ta-training-certification.md",
    }
    for path, marker in linked_files.items():
        if marker not in read(path):
            issues.append(f"{path} missing TA certification marker: {marker}")

    builder = read("scripts/build_course_site_release.py")
    if "ta-training-certification.md" not in builder.split("EXCLUDED_DOCS = [", 1)[1].split("]", 1)[0]:
        issues.append("course site release builder must exclude ta-training-certification.md")

    if issues:
        fail(f"TA training certification dossier incomplete: {'; '.join(issues[:12])}")
    ok("TA training certification dossier covers roles, competencies, practicums, simulations, privacy scenarios, ledger, recertification, and release exclusion")


def check_autograder_hidden_test_design() -> None:
    text = read("docs/autograder-hidden-tests.md")
    required_markers = [
        "公开单元测试",
        "隐藏边界测试",
        "隐藏性质测试",
        "书面解释/代码质量",
        "## 数值容差建议",
        "|------|----------|------|",
        "## Capstone 隐藏验收",
        "## 学术诚信与防投机检查",
        "## 失败日志规范",
    ]
    missing = [marker for marker in required_markers if marker not in text]

    for index, section in enumerate(EXPECTED_AUTOGRADER_SECTIONS):
        marker = f"## {section}"
        if marker not in text:
            missing.append(f"missing autograder section: {marker}")
            continue
        start = text.index(marker)
        next_sections = [
            text.find(f"## {next_section}", start + len(marker))
            for next_section in EXPECTED_AUTOGRADER_SECTIONS[index + 1 :]
        ]
        capstone_start = text.find("## Capstone 隐藏验收", start + len(marker))
        next_candidates = [pos for pos in next_sections + [capstone_start] if pos != -1]
        end = min(next_candidates) if next_candidates else len(text)
        body = text[start:end]
        if "隐藏测试类别：" not in body:
            missing.append(f"{section} missing hidden-test categories")
        if "人工复核触发：" not in body:
            missing.append(f"{section} missing manual-review triggers")
        hidden_bullets = re.findall(r"(?m)^- .+", body.split("人工复核触发：", 1)[0])
        if len(hidden_bullets) < 5:
            missing.append(f"{section} needs at least 5 hidden-test category bullets, got {len(hidden_bullets)}")
        review_part = body.split("人工复核触发：", 1)[1] if "人工复核触发：" in body else ""
        review_bullets = re.findall(r"(?m)^- .+", review_part)
        if len(review_bullets) < 2:
            missing.append(f"{section} needs at least 2 manual-review bullets, got {len(review_bullets)}")

    handout = read("docs/assignment-handout-pack.md")
    for assignment_number in range(1, len(EXPECTED_ASSIGNMENTS) + 1):
        if f"## Assignment {assignment_number}:" not in handout:
            missing.append(f"assignment handout missing Assignment {assignment_number}")
    if missing:
        fail(f"autograder hidden-test design incomplete: {'; '.join(missing[:10])}")
    ok(f"autograder hidden-test design covers {len(EXPECTED_AUTOGRADER_SECTIONS)} assignments")


def check_private_autograder_operations() -> None:
    text = read("docs/private-autograder-operations.md")
    assignment_guide = read("docs/assignment-submission-guide.md")
    autograder_guide = read("docs/autograder-hidden-tests.md")
    builder = ROOT / "scripts" / "run_private_autograder.py"
    issues = []

    for section in (
        "## Directory Boundary",
        "## Runbook",
        "## Manifest Schema",
        "## Rubric Mapping",
        "## Failure Log Contract",
        "## LMS And Gradescope Entrypoint",
        "## Integrity Checks",
        "## Regrade And Batch Correction",
        "## Release Checklist",
    ):
        if section not in text:
            issues.append(f"missing section: {section}")

    for marker in (
        "private_autograder/hidden_tests/",
        "private_autograder/reports/",
        "hidden_tests_stored_in_repo",
        "student_release_excludes",
        "public_unit_tests",
        "hidden_boundary_tests",
        "hidden_property_tests",
        "written_explanation_code_quality",
        "hardcoding_and_integrity_checks",
        "student_visible_feedback",
        "release_batch",
        "rubric_version",
        "regrade_decision_id",
        "hidden test exact input",
        "完整 expected output",
        "reference_solution.py",
        "scripts/build_assignment_release.py --all",
        "scripts/run_private_autograder.py --public-only",
    ):
        if marker not in text:
            issues.append(f"missing private autograder marker: {marker}")

    for upstream_text, upstream_name in (
        (assignment_guide, "assignment submission guide"),
        (autograder_guide, "autograder hidden-test guide"),
    ):
        if "scripts/run_private_autograder.py" not in upstream_text:
            issues.append(f"{upstream_name} missing private autograder script link")
        if "private-autograder-operations.md" not in upstream_text and upstream_name == "assignment submission guide":
            issues.append("assignment submission guide missing private autograder exclusion")

    with tempfile.TemporaryDirectory() as tmp:
        json_out = Path(tmp) / "private-autograder-dry-run.json"
        result = subprocess.run(
            [
                sys.executable,
                str(builder),
                "--public-only",
                "--json-out",
                str(json_out),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            fail(f"private autograder public dry run failed: {result.stderr.strip() or result.stdout[-1000:]}")
        if not json_out.exists():
            fail("private autograder dry run did not write JSON manifest")
        manifest = json.loads(json_out.read_text(encoding="utf-8"))

    if manifest.get("mode") != "private_autograder_public_dry_run":
        issues.append(f"unexpected private autograder mode: {manifest.get('mode')}")
    if manifest.get("hidden_tests_stored_in_repo") is not False:
        issues.append("private autograder manifest must state hidden_tests_stored_in_repo=False")
    excludes = set(manifest.get("student_release_excludes", []))
    for excluded in ("reference_solution.py", "private_autograder/", "hidden_tests/"):
        if excluded not in excludes:
            issues.append(f"manifest missing student release exclusion: {excluded}")

    assignments = manifest.get("assignments", [])
    if len(assignments) != len(EXPECTED_ASSIGNMENTS):
        issues.append(f"expected {len(EXPECTED_ASSIGNMENTS)} private autograder assignments, got {len(assignments)}")
    assignment_ids = {item.get("assignment_id") for item in assignments}
    if assignment_ids != set(EXPECTED_ASSIGNMENTS):
        issues.append(f"private autograder assignment ids {sorted(assignment_ids)} != expected assignments")

    for item in assignments:
        assignment_id = item.get("assignment_id", "<unknown>")
        if item.get("status") != "pass":
            issues.append(f"{assignment_id}: private autograder dry run status is {item.get('status')}")
        if item.get("public_tests", {}).get("status") != "pass":
            issues.append(f"{assignment_id}: public_tests did not pass")
        if item.get("hidden_tests", {}).get("status") != "skipped_public_only":
            issues.append(f"{assignment_id}: hidden_tests should be skipped in public dry run")
        for channel in (
            "public_unit_tests",
            "hidden_boundary_tests",
            "hidden_property_tests",
            "written_explanation_code_quality",
        ):
            if channel not in item.get("rubric_channels", []):
                issues.append(f"{assignment_id}: missing rubric channel {channel}")
        for review_field in ("written_answers", "run_log", "honor_statement", "code_quality_and_hardcoding"):
            if review_field not in item.get("manual_review_required", []):
                issues.append(f"{assignment_id}: missing manual review field {review_field}")

    summary = manifest.get("summary", {})
    if summary.get("pass_count") != len(EXPECTED_ASSIGNMENTS) or summary.get("fail_count") != 0:
        issues.append(f"unexpected private autograder summary: {summary}")

    if issues:
        fail(f"private autograder operations incomplete: {'; '.join(issues[:10])}")
    ok(f"private autograder public dry run emits manifest for {len(assignments)} assignments")


def check_capstone_files() -> None:
    capstone = ROOT / "projects/inference-engineering-capstone"
    required = [
        "acceptance.py",
        "app.py",
        "benchmark.py",
        "capacity_plan.py",
        "evaluate.py",
        "slo_check.py",
        "eval_cases.jsonl",
        "requirements.txt",
        "README.md",
    ]
    for name in required:
        if not (capstone / name).exists():
            fail(f"missing capstone file: {name}")
    capstone_readme = (capstone / "README.md").read_text(encoding="utf-8")
    for needle in ["项目报告 Rubric", "../../docs/project-report-rubric.md", "../../docs/compute-resource-guide.md", "P50/P95/P99"]:
        if needle not in capstone_readme:
            fail(f"inference capstone README missing project rubric marker: {needle}")

    for path in sorted(capstone.glob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")

    cases = 0
    for line in (capstone / "eval_cases.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            json.loads(line)
            cases += 1
    if cases < 5:
        fail(f"expected at least 5 capstone eval cases, got {cases}")
    ok(f"capstone files compile and {cases} eval cases are valid")


def check_training_capstone_files() -> None:
    capstone = ROOT / "projects/training-engineering-capstone"
    required = [
        "acceptance.py",
        "data_audit.py",
        "plan_training.py",
        "train.py",
        "sample_corpus.txt",
        "requirements.txt",
        "README.md",
    ]
    for name in required:
        if not (capstone / name).exists():
            fail(f"missing training capstone file: {name}")
    capstone_readme = (capstone / "README.md").read_text(encoding="utf-8")
    for needle in ["项目报告 Rubric", "../../docs/project-report-rubric.md", "../../docs/compute-resource-guide.md", "checkpoint resume"]:
        if needle not in capstone_readme:
            fail(f"training capstone README missing project rubric marker: {needle}")

    for path in sorted(capstone.glob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")

    corpus = (capstone / "sample_corpus.txt").read_text(encoding="utf-8")
    if len(corpus) < 128:
        fail("training capstone sample corpus is too small")
    ok("training capstone files compile and sample corpus is present")


def check_javascript() -> None:
    result = subprocess.run(["node", "--check", "js/app.js"], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        fail("node --check js/app.js failed")
    ok("js/app.js syntax is valid")


def find_chromium() -> str | None:
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        path = shutil.which(name)
        if path:
            return path
    snap_chromium = Path("/snap/bin/chromium")
    if snap_chromium.exists():
        return str(snap_chromium)
    return None


def reserve_local_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_http_server(url: str, process: subprocess.Popen[str]) -> None:
    deadline = time.monotonic() + 5
    last_error = ""
    while time.monotonic() < deadline:
        if process.poll() is not None:
            stdout, stderr = process.communicate(timeout=1)
            fail(f"browser smoke HTTP server exited early: {stdout} {stderr}".strip())
        try:
            with urlopen(url, timeout=0.5) as response:
                if response.status == 200:
                    return
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.1)
    fail(f"browser smoke HTTP server did not become ready: {last_error}")


def dump_rendered_dom(chromium: str, url: str, user_data_dir: Path) -> str:
    result = subprocess.run(
        [
            chromium,
            "--headless",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            f"--user-data-dir={user_data_dir}",
            "--virtual-time-budget=5000",
            "--dump-dom",
            url,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip().splitlines()[:8]
        fail(f"chromium --dump-dom failed for {url}: {' | '.join(details)}")
    return result.stdout


def check_browser_render_smoke() -> None:
    chromium = find_chromium()
    if not chromium:
        fail("chromium is required for browser render smoke test")

    port = reserve_local_port()
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    rendered_pages = 0
    rendered_formulas = 0
    try:
        base_url = f"http://127.0.0.1:{port}"
        wait_for_http_server(f"{base_url}/index.html", server)
        with tempfile.TemporaryDirectory(prefix="course-browser-smoke-") as tmp:
            user_data_dir = Path(tmp)
            for relative_url in RENDER_SMOKE_PAGES:
                source_path = ROOT / relative_url
                source = source_path.read_text(encoding="utf-8")
                dom = dump_rendered_dom(chromium, f"{base_url}/{relative_url}", user_data_dir)
                rel = source_path.relative_to(ROOT)

                if "<title>" in source:
                    expected_title = re.search(r"<title>(.*?)</title>", source, re.S)
                    if expected_title and expected_title.group(1).strip() not in dom:
                        fail(f"browser render missing title for {rel}")
                for marker in ("ERR_", "This site can", "File not found", "404 Not Found"):
                    if marker in dom:
                        fail(f"browser render failed for {rel}: found {marker!r}")

                if "sidebar-nav" not in dom or "ch-num" not in dom:
                    fail(f"browser render did not execute sidebar JS for {rel}")
                if dom.count('class="ch-num"') < EXPECTED_CHAPTERS:
                    fail(f"browser render sidebar is incomplete for {rel}")

                source_formula_count = source.count("data-expr=")
                if source_formula_count:
                    rendered_count = dom.count("katex-html")
                    if rendered_count < source_formula_count:
                        fail(
                            f"browser render did not render all formulas for {rel}: "
                            f"{rendered_count}/{source_formula_count}"
                        )
                    rendered_formulas += rendered_count
                rendered_pages += 1
    finally:
        server.terminate()
        try:
            server.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()
            server.communicate(timeout=3)

    ok(
        f"browser render smoke passed for {rendered_pages} pages "
        f"with {rendered_formulas} rendered KaTeX nodes"
    )


def check_assignment_tests() -> None:
    runner = ROOT / "run_assignment_tests.py"
    if not runner.exists():
        fail("missing assignment test runner: run_assignment_tests.py")

    result = subprocess.run(
        [sys.executable, "run_assignment_tests.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        fail("assignment tests failed")
    expected_summary = f"ASSIGNMENT TESTS: PASS ({len(EXPECTED_ASSIGNMENTS)} suite(s))"
    if expected_summary not in result.stdout:
        fail(f"assignment runner did not report expected suite count: {expected_summary}")
    ok("assignment tests passed")


def ast_signature(node: ast.FunctionDef) -> str:
    return ast.unparse(node.args)


def assignment_api_definitions(path: Path) -> dict[str, dict[str, object]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    definitions: dict[str, dict[str, object]] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            definitions[node.name] = {
                "kind": "function",
                "signature": ast_signature(node),
                "methods": {},
            }
        elif isinstance(node, ast.ClassDef):
            methods = {
                item.name: ast_signature(item)
                for item in node.body
                if isinstance(item, ast.FunctionDef)
            }
            definitions[node.name] = {
                "kind": "class",
                "signature": "",
                "methods": methods,
            }
    return definitions


def assignment_test_module_refs(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    refs: set[str] = set()

    class RefVisitor(ast.NodeVisitor):
        def visit_Attribute(self, node: ast.Attribute) -> None:
            if isinstance(node.value, ast.Name) and node.value.id in {"submission", "solution"}:
                refs.add(node.attr)
            self.generic_visit(node)

    RefVisitor().visit(tree)
    return refs


def check_assignment_api_contracts() -> None:
    explicit_private_exports = {
        "ch01_bpe": {"_get_stats", "_merge"},
    }
    issues = []

    for assignment in EXPECTED_ASSIGNMENTS:
        suite_dir = ROOT / "assignments" / assignment
        starter_defs = assignment_api_definitions(suite_dir / "starter.py")
        reference_defs = assignment_api_definitions(suite_dir / "reference_solution.py")
        test_refs = assignment_test_module_refs(suite_dir / "tests.py")
        required = {
            name for name in reference_defs if not name.startswith("_")
        } | test_refs | explicit_private_exports.get(assignment, set())

        for name in sorted(required):
            if name not in starter_defs:
                issues.append(f"{assignment}: starter.py missing {name}")
                continue
            if name not in reference_defs:
                issues.append(f"{assignment}: reference_solution.py missing {name}")
                continue
            starter_def = starter_defs[name]
            reference_def = reference_defs[name]
            if starter_def["kind"] != reference_def["kind"]:
                issues.append(f"{assignment}: {name} kind differs between starter and reference")
                continue
            if reference_def["kind"] == "function":
                if starter_def["signature"] != reference_def["signature"]:
                    issues.append(
                        f"{assignment}: {name} signature {starter_def['signature']} "
                        f"!= {reference_def['signature']}"
                    )
            else:
                starter_methods = starter_def["methods"]
                reference_methods = reference_def["methods"]
                if starter_methods != reference_methods:
                    issues.append(
                        f"{assignment}: class {name} methods/signatures differ "
                        f"{starter_methods} != {reference_methods}"
                    )

    if issues:
        fail(f"assignment API contracts are inconsistent: {'; '.join(issues[:10])}")
    ok(f"assignment starter/reference/tests API contracts are aligned ({len(EXPECTED_ASSIGNMENTS)} suites)")


def check_assignment_starter_failure_modes() -> None:
    issues = []
    for assignment in EXPECTED_ASSIGNMENTS:
        suite_dir = ROOT / "assignments" / assignment
        env = os.environ.copy()
        env["STUDENT_MODULE"] = "starter"
        env.setdefault("CUDA_VISIBLE_DEVICES", "")
        result = subprocess.run(
            [sys.executable, "tests.py"],
            cwd=suite_dir,
            env=env,
            text=True,
            capture_output=True,
        )
        output = result.stdout + "\n" + result.stderr
        if result.returncode == 0:
            issues.append(f"{assignment}: starter unexpectedly passes public tests")
        if "NotImplementedError" not in output:
            issues.append(f"{assignment}: starter failure does not point to NotImplementedError")
        for forbidden in ("ImportError", "ModuleNotFoundError", "FileNotFoundError"):
            if forbidden in output:
                issues.append(f"{assignment}: starter failure contains {forbidden}")

    if issues:
        fail(f"assignment starter failure modes are unclear: {'; '.join(issues[:10])}")
    ok(f"assignment starters fail with clear NotImplementedError markers ({len(EXPECTED_ASSIGNMENTS)} suites)")


def check_assignment_release_builder() -> None:
    builder = ROOT / "scripts/build_assignment_release.py"
    if not builder.exists():
        fail("missing assignment release builder: scripts/build_assignment_release.py")
    compile(builder.read_text(encoding="utf-8"), str(builder), "exec")

    dry_run = subprocess.run(
        [sys.executable, str(builder), "--all", "--dry-run"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if dry_run.returncode != 0:
        fail(f"assignment release builder dry-run failed: {dry_run.stderr.strip()}")
    try:
        manifest = json.loads(dry_run.stdout)
    except json.JSONDecodeError as error:
        fail(f"assignment release builder dry-run did not emit JSON: {error}")
    assignments = manifest.get("assignments", [])
    if [item.get("assignment") for item in assignments] != EXPECTED_ASSIGNMENTS:
        fail("assignment release builder manifest does not cover expected assignments")
    for item in assignments:
        included = set(item.get("included", []))
        excluded = set(item.get("excluded", []))
        if included != {"README.md", "starter.py", "tests.py"}:
            fail(f"unexpected release included files for {item.get('assignment')}: {included}")
        if "reference_solution.py" not in excluded:
            fail(f"release manifest does not exclude reference_solution.py for {item.get('assignment')}")
        if item.get("test_default_module") != "student_solution":
            fail(f"release manifest must default tests to student_solution for {item.get('assignment')}")

    with tempfile.TemporaryDirectory(prefix="assignment-release-") as tmp:
        relative_out = Path(tmp).relative_to(ROOT) if Path(tmp).is_relative_to(ROOT) else Path(tmp)
        build = subprocess.run(
            [sys.executable, str(builder), "--all", "--out", str(relative_out)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if build.returncode != 0:
            fail(f"assignment release builder failed: {build.stderr.strip()}")
        out_dir = Path(tmp)
        for assignment in EXPECTED_ASSIGNMENTS:
            release_dir = out_dir / assignment
            if not release_dir.exists():
                fail(f"release builder missing package directory: {assignment}")
            release_files = {path.name for path in release_dir.iterdir()}
            expected_files = {"README.md", "starter.py", "tests.py", "RELEASE_MANIFEST.json"}
            if release_files != expected_files:
                fail(f"{assignment} release files {release_files} != {expected_files}")
            if (release_dir / "reference_solution.py").exists():
                fail(f"{assignment} release package leaked reference_solution.py")
            tests_text = (release_dir / "tests.py").read_text(encoding="utf-8")
            if 'os.environ.get("STUDENT_MODULE", "student_solution")' not in tests_text:
                fail(f"{assignment} release tests.py does not default to student_solution")
            if "reference_solution" in tests_text:
                fail(f"{assignment} release tests.py still references reference_solution")
            readme_text = (release_dir / "README.md").read_text(encoding="utf-8")
            if "reference_solution" in readme_text:
                fail(f"{assignment} release README still references reference_solution")
            if "Student Release Notes" not in readme_text:
                fail(f"{assignment} release README missing Student Release Notes")

    ok(f"assignment release builder packages {len(EXPECTED_ASSIGNMENTS)} student-safe suites")


def check_course_site_release_builder() -> None:
    builder = ROOT / "scripts/build_course_site_release.py"
    if not builder.exists():
        fail("missing course site release builder: scripts/build_course_site_release.py")
    compile(builder.read_text(encoding="utf-8"), str(builder), "exec")

    with tempfile.TemporaryDirectory(prefix="course-site-release-") as tmp:
        dry_out = Path(tmp) / "dry"
        dry_run = subprocess.run(
            [sys.executable, str(builder), "--out", str(dry_out), "--dry-run"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if dry_run.returncode != 0:
            fail(f"course site release builder dry-run failed: {dry_run.stderr.strip()}")
        try:
            manifest = json.loads(dry_run.stdout)
        except json.JSONDecodeError as error:
            fail(f"course site release builder dry-run did not emit JSON: {error}")

        included_roots = set(manifest.get("included_roots", []))
        expected_roots = {
            "index.html",
            "inference-engineer-curriculum.html",
            "training-engineer-curriculum.html",
            "chapters/",
            "css/",
            "js/",
            "images/",
            "docs/",
            "assignments/",
            "projects/",
        }
        if included_roots != expected_roots:
            fail(f"course site release included roots {included_roots} != {expected_roots}")
        if "README.md" in included_roots:
            fail("course site release must not include repository README.md")

        excluded_docs = set(manifest.get("excluded_docs", []))
        for internal_doc in (
            "instructor-solution-guide.md",
            "autograder-hidden-tests.md",
            "grading-calibration.md",
            "grading-drift-audit-ledger.md",
            "grading-anchor-sample-feedback-pack.md",
            "private-autograder-operations.md",
            "staff-runbook.md",
            "ta-training-certification.md",
        ):
            if internal_doc not in excluded_docs:
                fail(f"course site release manifest does not exclude {internal_doc}")

        out_dir = Path(tmp) / "site"
        build = subprocess.run(
            [sys.executable, str(builder), "--out", str(out_dir)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if build.returncode != 0:
            fail(f"course site release builder failed: {build.stderr.strip()}")

        if (out_dir / "README.md").exists():
            fail("course site release leaked repository README.md")
        if not (out_dir / "SITE_RELEASE_MANIFEST.json").exists():
            fail("course site release missing SITE_RELEASE_MANIFEST.json")
        built_manifest = json.loads((out_dir / "SITE_RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
        for chapter_item in built_manifest.get("chapters", []):
            if int(chapter_item.get("removed_solution_blocks", 0)) <= 0:
                fail(f"course site release did not strip solution blocks for {chapter_item.get('file')}")

        for required_dir in ("chapters", "css", "js", "images", "docs", "assignments", "projects"):
            if not (out_dir / required_dir).exists():
                fail(f"course site release missing directory: {required_dir}")
        for required_page in ("inference-engineer-curriculum.html", "training-engineer-curriculum.html"):
            if not (out_dir / required_page).exists():
                fail(f"course site release missing root page: {required_page}")
        for project_dir in ("inference-engineering-capstone", "training-engineering-capstone"):
            if not (out_dir / "projects" / project_dir / "README.md").exists():
                fail(f"course site release missing project README: {project_dir}")

        for index in range(1, EXPECTED_CHAPTERS + 1):
            chapter = f"ch{index:02d}.html"
            chapter_path = out_dir / "chapters" / chapter
            if not chapter_path.exists():
                fail(f"course site release missing chapter: {chapter}")
            chapter_text = chapter_path.read_text(encoding="utf-8")
            for forbidden in ('class="solution-toggle"', 'class="solution"', "查看参考解答"):
                if forbidden in chapter_text:
                    fail(f"course site release leaked inline solution marker in {chapter}: {forbidden}")

        for safe_doc in (
            "syllabus.md",
            "reading-list.md",
            "course-policies.md",
            "capstone-defense-oral-exam-bank.md",
            "assessment-administration-policy.md",
            "assessment-item-bank-ledger.md",
            "assessment-item-analysis-psychometrics.md",
            "teaching-observation-course-evaluation.md",
            "academic-integrity-case-process.md",
            "guest-speaker-seminar-policy.md",
            "chapter-source-map.md",
            "external-source-verification.md",
            "external-expert-review-dossier.md",
            "course-materials-index.md",
            "course-calendar-deadline-ledger.md",
            "lecture-media-access-policy.md",
            "lecture-note-sample-pack.md",
            "lecture-note-core-pack.md",
            "notation-shape-glossary.md",
            "worked-example-pack.md",
            "learning-outcome-attainment-report.md",
            "lecture-notes-quality-review.md",
            "mathematical-derivation-audit.md",
            "model-benchmark-card-guide.md",
            "material-versioning-archive-policy.md",
            "paper-recap-calibration-pack.md",
            "course-communication-policy.md",
            "course-errata-correction-ledger.md",
            "course-staff-office-hours-directory.md",
            "enrollment-audit-public-use-policy.md",
            "gradebook-lms-operations.md",
            "ml-foundations-prerequisite-bridge.md",
            "concept-misconception-map.md",
            "core-concept-glossary.md",
            "topic-dependency-map.md",
            "comprehensive-review-study-guide.md",
            "classic-nlp-deep-dive-module.md",
            "chapter-claim-audit-ledger.md",
            "experimental-rigor-evaluation-statistics.md",
            "final-project-showcase-archive-policy.md",
            "capstone-project-gallery.md",
            "project-report-exemplar-pack.md",
            "presemester-readiness-audit.md",
            "python-pytorch-review-session.md",
            "programming-assignment-code-quality-rubric.md",
            "reading-discussion-question-bank.md",
            "safety-societal-impact-casebook.md",
            "project-team-mentor-policy.md",
            "staff-assistance-code-review-policy.md",
            "inference-engineer-curriculum.md",
            "training-engineer-curriculum.md",
        ):
            if not (out_dir / "docs" / safe_doc).exists():
                fail(f"course site release missing safe doc: {safe_doc}")

        for assignment in EXPECTED_ASSIGNMENTS:
            release_dir = out_dir / "assignments" / assignment
            if not release_dir.exists():
                fail(f"course site release missing assignment package: {assignment}")
            release_files = {path.name for path in release_dir.iterdir()}
            expected_files = {"README.md", "starter.py", "tests.py", "RELEASE_MANIFEST.json"}
            if release_files != expected_files:
                fail(f"course site release assignment files for {assignment} {release_files} != {expected_files}")
            if (release_dir / "reference_solution.py").exists():
                fail(f"course site release leaked assignment reference_solution.py for {assignment}")
            tests_text = (release_dir / "tests.py").read_text(encoding="utf-8")
            if 'os.environ.get("STUDENT_MODULE", "student_solution")' not in tests_text:
                fail(f"course site release assignment tests do not default to student_solution for {assignment}")
            if "reference_solution" in tests_text:
                fail(f"course site release assignment tests reference reference_solution for {assignment}")

        for forbidden_doc in (
            "instructor-solution-guide.md",
            "autograder-hidden-tests.md",
            "grading-calibration.md",
            "grading-drift-audit-ledger.md",
            "grading-anchor-sample-feedback-pack.md",
            "private-autograder-operations.md",
            "staff-runbook.md",
        ):
            if (out_dir / "docs" / forbidden_doc).exists():
                fail(f"course site release leaked internal doc: {forbidden_doc}")
            for release_file in [out_dir / "index.html", *sorted((out_dir / "docs").glob("*.md"))]:
                text = release_file.read_text(encoding="utf-8")
                forbidden_link_patterns = (
                    f"](docs/{forbidden_doc}",
                    f"]({forbidden_doc}",
                    f'href="docs/{forbidden_doc}"',
                    f'href="../docs/{forbidden_doc}"',
                    f'href="{forbidden_doc}"',
                )
                for pattern in forbidden_link_patterns:
                    if pattern in text:
                        fail(f"course site release leaked internal doc link in {release_file.name}: {pattern}")

        release_link_count, release_broken_links = collect_release_local_links(out_dir)
        if release_broken_links:
            fail(f"course site release has broken local links: {'; '.join(release_broken_links[:10])}")

        chromium = find_chromium()
        if not chromium:
            fail("chromium is required for course site release browser smoke test")
        port = reserve_local_port()
        server = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
            cwd=out_dir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        rendered_pages = 0
        rendered_formulas = 0
        try:
            base_url = f"http://127.0.0.1:{port}"
            wait_for_http_server(f"{base_url}/index.html", server)
            with tempfile.TemporaryDirectory(prefix="course-site-release-browser-") as browser_tmp:
                user_data_dir = Path(browser_tmp)
                for relative_url in RENDER_SMOKE_PAGES:
                    release_path = out_dir / relative_url
                    if not release_path.exists():
                        fail(f"course site release browser smoke missing page: {relative_url}")
                    source = release_path.read_text(encoding="utf-8")
                    dom = dump_rendered_dom(chromium, f"{base_url}/{relative_url}", user_data_dir)

                    for marker in ("ERR_", "This site can", "File not found", "404 Not Found"):
                        if marker in dom:
                            fail(f"course site release browser render failed for {relative_url}: found {marker!r}")
                    if "sidebar-nav" not in dom or dom.count('class="ch-num"') < EXPECTED_CHAPTERS:
                        fail(f"course site release browser render did not execute sidebar JS for {relative_url}")

                    source_formula_count = source.count("data-expr=")
                    if source_formula_count:
                        rendered_count = dom.count("katex-html")
                        if rendered_count < source_formula_count:
                            fail(
                                f"course site release browser render did not render all formulas for {relative_url}: "
                                f"{rendered_count}/{source_formula_count}"
                            )
                        rendered_formulas += rendered_count
                    rendered_pages += 1
        finally:
            server.terminate()
            try:
                server.communicate(timeout=3)
            except subprocess.TimeoutExpired:
                server.kill()
                server.communicate(timeout=3)

    ok(
        "course site release builder strips inline solutions, excludes instructor-only docs, "
        f"validates {release_link_count} local links, and browser-renders {rendered_pages} pages "
        f"with {rendered_formulas} KaTeX nodes"
    )


def run_capstone_acceptance() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "acceptance.py",
            "--port",
            "8023",
            "--requests",
            "4",
            "--concurrency",
            "2",
            "--min-tokens-per-second",
            "100",
        ],
        cwd=ROOT / "projects/inference-engineering-capstone",
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        fail("capstone acceptance failed")
    ok("capstone acceptance passed")


def run_training_acceptance() -> None:
    result = subprocess.run(
        [sys.executable, "acceptance.py"],
        cwd=ROOT / "projects/training-engineering-capstone",
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        fail("training capstone acceptance failed")
    ok("training capstone acceptance passed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify course metadata, scripts, and optional capstone acceptance")
    parser.add_argument("--capstone", action="store_true", help="Run the full inference Capstone acceptance flow")
    parser.add_argument("--training", action="store_true", help="Run the PyTorch training Capstone acceptance flow")
    args = parser.parse_args()

    check_chapter_counts()
    check_public_stats()
    check_university_course_scaffold()
    check_concept_misconception_map()
    check_core_concept_glossary()
    check_topic_dependency_map()
    check_learning_analytics_remediation_plan()
    check_weekly_teaching_reflection_adjustment_log()
    check_course_operations_log_records()
    check_learning_outcome_attainment_report()
    check_teaching_observation_course_evaluation()
    check_external_expert_review_dossier()
    check_workload_pacing_calibration()
    check_material_versioning_archive_policy()
    check_lecture_notes_quality_review()
    check_lecture_notes_review_ledger()
    check_lecture_note_sample_pack()
    check_lecture_note_core_pack()
    check_notation_shape_glossary()
    check_worked_example_pack()
    check_lecture_slide_sample_pack()
    check_recitation_worksheet_pack()
    check_ml_foundations_prerequisite_bridge()
    check_gradebook_lms_operations()
    check_assessment_item_bank_ledger()
    check_assessment_blueprint_coverage_matrix()
    check_assessment_item_analysis_psychometrics()
    check_comprehensive_review_study_guide()
    check_assessment_administration_policy()
    check_staff_assistance_code_review_policy()
    check_project_team_mentor_policy()
    check_capstone_proposal_milestone_rigor()
    check_project_submission_dossier()
    check_final_project_showcase_archive_policy()
    check_academic_integrity_case_process()
    check_guest_speaker_seminar_policy()
    check_course_staff_office_hours_directory()
    check_course_communication_policy()
    check_course_errata_correction_ledger()
    check_enrollment_audit_public_use_policy()
    check_lecture_media_access_policy()
    check_course_calendar_deadline_ledger()
    check_python_pytorch_review_session()
    check_assignment_scaffold()
    check_rubric_weight_tables()
    check_frontier_seminar_handout()
    check_classic_nlp_handout_depth()
    check_classic_nlp_deep_dive_module()
    check_experimental_rigor_evaluation_statistics()
    check_project_report_template()
    check_project_report_exemplar_pack()
    check_safety_societal_impact_casebook()
    check_model_benchmark_card_guide()
    check_capstone_defense_oral_exam_bank()
    check_programming_assignment_code_quality_rubric()
    check_written_assessment_alignment()
    check_grading_drift_audit_ledger()
    check_ta_training_certification()
    check_grading_anchor_sample_feedback_pack()
    check_autograder_hidden_test_design()
    check_private_autograder_operations()
    check_capstone_files()
    check_training_capstone_files()
    check_javascript()
    check_browser_render_smoke()
    check_html_links()
    check_image_accessibility()
    check_markdown_links()
    check_markdown_table_structure()
    check_text_and_formula_format()
    check_release_placeholders()
    check_command_conventions()
    check_key_derivation_consistency()
    check_chapter_code_contracts()
    check_python_code_blocks_compile()
    check_exercise_widgets()
    check_unqualified_claim_phrasing()
    check_external_source_inventory_coverage()
    check_dataset_model_artifact_registry()
    check_source_governance_docs()
    check_frontier_source_evidence_cards()
    check_frontier_source_verifier_script()
    check_cs224n_snapshot_refresh_script()
    check_presemester_readiness_audit()
    check_course_evidence_manifest_script()
    check_chapter_claim_audit_ledger()
    check_mathematical_derivation_audit()
    check_paper_recap_calibration_pack()
    check_reading_discussion_question_bank()
    check_paper_to_code_traceability_matrix()
    check_assignment_api_contracts()
    check_assignment_starter_failure_modes()
    check_assignment_release_builder()
    check_course_site_release_builder()
    check_assignment_tests()
    if args.capstone:
        run_capstone_acceptance()
    if args.training:
        run_training_acceptance()
    print("COURSE VERIFY: PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"COURSE VERIFY: FAIL ({exc})", file=sys.stderr)
        sys.exit(1)
