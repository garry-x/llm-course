# Staff Assistance and Code Review Boundary Policy

本政策用于规定教师、助教、mentor 和 autograder contact 在作业、office hours、discussion section、capstone 和 regrade 中可以提供何种帮助。它补充 [课程 Syllabus](syllabus.md)、[Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)、[Discussion Section and Office Hours Guide](discussion-office-hours-guide.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Programming Assignment Code Quality Rubric](programming-assignment-code-quality-rubric.md)、[Project Team and Mentor Policy](project-team-mentor-policy.md)、[Academic Integrity Case Process](academic-integrity-case-process.md) 和 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md)。

本课程对标 CS224N 风格的大课运行口径：早期作业可以给更多代码级 debugging 支持，后期作业和 final project 必须保护独立完成、公平评分和项目原创性。任何 staff 帮助都不能替代学生自己的代码、推导、实验判断或报告结论。

## Assistance Levels

| assistance_level | staff 可以做 | staff 不可以做 | 典型场景 |
|------------------|--------------|----------------|----------|
| concept_hint | 解释概念、公式、shape、复杂度或阅读材料 | 给出作业专用实现步骤 | lecture、discussion、public forum |
| debug_trace | 看 traceback、公开测试名、shape、dtype、device、最小复现 | 查看完整学生解法并逐行修正 | coding office hours、A1/A2 support |
| limited_code_view | 查看学生局部代码片段，指出 API、shape、mask 或边界问题 | 写核心函数、给最终代码、复制答案 | early programming assignments |
| pseudocode_review | 讨论算法结构、伪代码、测试思路和失败分类 | 审阅完整可提交实现 | later assignments、capstone planning |
| artifact_review | 看日志、benchmark、report outline、data/ethics form、capacity plan | 代写报告结论或调实验数字 | capstone milestone、mentor meeting |
| rubric_explanation | 解释 rubric、隐藏测试类别级反馈和复核材料 | 透露 hidden tests、评分脚本或 reference solution | grade release、regrade support |

## Assignment Assistance Matrix

| course_item | 代码查看边界 | 允许帮助 | 禁止帮助 |
|-------------|--------------|----------|----------|
| Ch01 BPE | limited_code_view | pair counting、non-overlapping merge、encode/decode failure 的局部 debug | staff 写 `train` / `encode` 完整实现 |
| Ch02 Embeddings / RoPE | limited_code_view | tensor shape、buffer、RoPE rotation、公开测试失败定位 | staff 给出完整 RoPE 代码或隐藏测试条件 |
| Ch03 Attention | pseudocode_review | mask 方向、softmax 前后、shape trace、最小反例 | staff 查看并修正完整 attention 实现 |
| Ch04 MHA / GQA / MLA | pseudocode_review | head split、KV cache 公式、API contract、复杂度讨论 | staff 给出完整 forward 或 cache 代码 |
| Ch05 Transformer Block | pseudocode_review | norm/residual/FFN 顺序、gradcheck 思路 | staff 逐行修 block 实现 |
| Ch06 GPT / MoE | pseudocode_review | 参数审计、causal 失败诊断、router shape | staff 写 model assembly 或 router 逻辑 |
| Ch07 Training Loop | pseudocode_review | loss log、scheduler、checkpoint/resume 证据、NaN 排查 | staff 调参到可提交结果或写训练循环 |
| Ch08 Generation | pseudocode_review | top-k/top-p/speculative decoding 边界案例 | staff 给最终 sampling 实现 |
| Ch09 Alignment | pseudocode_review | label mask、LoRA rank、DPO/GRPO 方向解释 | staff 写 SFT/LoRA/DPO/GRPO 核心函数 |
| Ch10 Inference / RAG | pseudocode_review | benchmark、SLO、RAG failure taxonomy、capacity plan | staff 代搭服务或写 RAG pipeline |
| Ch11 Classic NLP | pseudocode_review | UAS/LAS、BLEU/ROUGE、EM/F1、MLM labels 例子 | staff 给完整 metric/parser 实现 |

早期 limited_code_view 的目的是帮助学生建立调试方法。进入 Ch03 后，staff 应逐步转向 pseudocode、shape、最小反例和公开测试解释，而不是直接审阅完整可提交代码。

## Final Project and Capstone Boundary

final project / capstone 中 staff 和 mentor 可以看项目计划、实验日志、评测表、报告结构、数据/伦理表和失败案例，但默认不看完整项目实现。

| 项目阶段 | staff 可以看 | staff 不可以看 |
|----------|--------------|----------------|
| proposal | scope、baseline、data source、risk register、compute estimate | 现成项目代码并承诺可得高分 |
| milestone | logs、metric table、ablation plan、failure cases、data/ethics review | 替团队 debug 到通过最终验收 |
| mentor meeting | strongest evidence、largest risk、downgrade trigger、next step | 写实验设计、代码、报告段落或最终结论 |
| final report draft | outline、claim/evidence alignment、source boundary、repro checklist | 代写结果分析或隐藏评分意见 |
| presentation rehearsal | timing、evidence clarity、risk disclosure、Q&A readiness | 预先给出所有评分问题或项目最终分 |

若项目因环境、数据或平台问题完全阻塞，staff 可以帮助构造最小复现、确认资源故障或建议降级路径；不能把 staff 的修复代码作为学生核心贡献。

## Office Hours Interaction Rules

学生进入 coding/debugging office hours 前应提供：

| field | 要求 |
|-------|------|
| course_item | 章节、作业或项目 |
| command | 原始运行命令和 cwd |
| first_failure | 第一个 traceback、assert message 或测试名 |
| expected_shape_or_behavior | 学生自己的 shape 推导或预期输出 |
| minimal_reproduction | 最小输入、短 tensor、日志片段或报告段落 |
| attempted_fix | 已尝试的 1-3 个方向 |

staff 回答时应优先给：

- 定位路径。
- shape / dtype / device 检查点。
- 一个更小反例。
- 相关章节、handout 或 public test 的链接。
- 可复现命令。
- 下一步学生自己要验证的假设。

staff 不应在公开或私密渠道粘贴参考实现、完整核心函数、隐藏测试输入、其他学生提交或未公开评分脚本。

## Public Forum and Private Channel Boundary

| 渠道 | 适合 | 不适合 |
|------|------|--------|
| public forum | 概念、公开错误信息、环境命令、rubric 解释、课程材料链接 | 完整学生代码、个人成绩、hidden tests、私密情况 |
| private message | 个人环境、便利安排、成绩争议、团队贡献、诚信沟通 | 寻求单独获得额外作业提示 |
| office hours queue | 最小复现、shape 推导、debug hypothesis | 贴完整答案或大段未脱敏代码 |
| LMS regrade | 具体 rubric 项、原始提交、复核理由 | 修改后代码、事后新实验作为原始评分依据 |

如果 private channel 中给出的答复会改变全班的 deadline、rubric、API、测试或政策口径，staff 必须把类别级信息转为公开公告或文档更新。

## Regrade and Academic Integrity Boundary

regrade 支持可以解释反馈和 rubric，但不能把复核变成二次完成作业。

| 场景 | 允许 | 禁止 |
|------|------|------|
| rubric explanation | 解释扣分项和证据要求 | 暗示 hidden test 输入或 exact expected output |
| environment dispute | 检查原始提交、命令、版本和平台日志 | 接受修改后代码作为原始提交 |
| manual review | 对照 rubric 复查指定项 | 私下改变全班评分口径 |
| integrity concern | 按 academic integrity process 私密收集证据 | 在公开论坛讨论个人 similarity report |
| staff mistake | 批量修正受影响学生并公告类别 | 只给提出问题的学生秘密修正 |

若 staff assistance 本身可能影响评分公平性，例如某位学生得到超出政策的代码级帮助，Head TA 应记录 incident、通知 instructor，并决定是否需要公告、补充 office hours、统一提示或评分调整。

## Staff Assistance Log

为了让支持可复盘但不侵入隐私，课程组可以记录类别级 assistance log。

| field | 内容 |
|-------|------|
| date | 日期 |
| staff_role | Discussion TA、Head TA、Project Mentor、Autograder Contact |
| course_item | 作业、项目或政策项 |
| assistance_level | concept_hint、debug_trace、limited_code_view、pseudocode_review、artifact_review、rubric_explanation |
| public_or_private | public forum、office hours、private message、LMS regrade |
| issue_category | shape、mask、dtype、optimizer、RAG、rubric、policy 等 |
| action_taken | hint、doc link、minimal reproduction、announcement、escalation |
| fairness_followup | none、public clarification、FAQ update、rubric update、incident review |

日志不应包含学生完整代码、个人健康信息、成绩细节、hidden test 输入或诚信个案细节。高频问题应进入 [Course Operations and Improvement Log](course-operations-log.md)、FAQ 或 discussion drill。

## Staff Checklist

- syllabus、staff directory、discussion guide、assignment submission guide、project mentor policy 和 CS224N crosswalk 均链接本政策。
- Ch01-Ch02 允许 limited_code_view；Ch03-Ch11 以 pseudocode_review、debug_trace 和 shape guidance 为主。
- final project / capstone 不默认查看完整项目实现；mentor 聚焦 scope、evidence、risk 和 reproducibility。
- regrade support 不泄露 hidden tests、reference solution 或评分脚本。
- 如果 staff 给出会影响全班规则的答复，必须转为公告或文档更新。
- `.venv/bin/python verify_course.py` 通过。

## 发布前 Checklist

- 学生站点发布包包含本文件。
- 本文件不包含 reference solution、hidden tests、评分脚本或学生提交。
- 每轮开课前确认 assignment assistance matrix 与当轮作业难度、LMS 设置和学校 honor code 一致。
- Course staff 在第一次 office hours 前阅读本政策并记录确认。
