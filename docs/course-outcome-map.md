# Course Outcome Map

本文件把课程目标映射到可检查证据。它用于教师开课前审查、助教分工、期末课程复盘，以及判断课程是否达到高校课程水平。原则是：每个目标必须同时有教学材料、学生交付、自动证据和人工评分证据；自动测试只证明一部分，不替代人工审阅。评估渠道、认知层级和证据 gate 的总表见 [Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)，知识点先修、章节 unlock path 和 spiral review 路径见 [Topic Dependency and Spiral Review Map](topic-dependency-map.md)，开课后 direct/indirect evidence、达标阈值和改进动作汇总见 [Learning Outcome Attainment Report](learning-outcome-attainment-report.md)。

## 证据等级

| 等级 | 含义 | 例子 |
|------|------|------|
| A | 自动可验证，且覆盖明确 | `verify_course.py`、`run_assignment_tests.py`、capstone acceptance |
| B | 可评分但需人工判断 | 书面推导、项目报告、同伴 review、阅读复盘、课堂参与 |
| C | 教学材料证据 | 章节正文、lecture plan、reading list、handout |
| D | 待课程运行中收集 | 课堂 exit ticket、答疑记录、隐藏测试统计、学生项目复现记录 |

## Outcome 1: 解释 Decoder-only LLM 数据流

目标表述：学生能从 tokenizer、embedding、attention、Transformer block 到 GPT model 解释 decoder-only LLM 的完整数据流。

教学材料：

- Ch01-Ch06 正文。
- [10 周 / 20 讲 Lecture Plan](lecture-plan.md) Week 1-4。
- [数学与 PyTorch 先修复习](math-prerequisites.md) 的 shape 与 attention 复习。

学生交付：

- `assignments/ch01_bpe/` 到 `assignments/ch06_gpt/`。
- 书面题 Ch01-Ch06。
- Exit ticket 中的 shape trace。

自动证据：

- `run_assignment_tests.py` 中 Ch01-Ch06 suite 通过。
- `verify_course.py` 检查章节脚手架、作业入口、KaTeX 格式和链接。

人工评分证据：

- 学生能画出从 `input_ids` 到 logits 的 shape 流。
- 学生能解释 causal mask、position encoding、weight tying 和 MoE routing 的作用。

最低通过标准：

- Ch01-Ch06 公开测试通过。
- 书面题至少覆盖 BPE、RoPE、attention scaling、GPT 参数量四类推导。
- 报告或答辩中能说明“哪个张量在哪一层改变了 shape”。

## Outcome 2: 用 PyTorch 实现核心模块

目标表述：学生能用 PyTorch 实现并测试核心模块，而不是只调用现成 API。

教学材料：

- Ch01-Ch10 编程练习。
- [Autograder 与隐藏测试设计指南](autograder-hidden-tests.md)。
- [Instructor Solution Guide](instructor-solution-guide.md) 的常见扣分点。

学生交付：

- Ch01-Ch10 starter 实现。
- Ch11 classic NLP 补充作业。
- 测试输出和错误分析。

自动证据：

- `run_assignment_tests.py` 报告 11 个 suite 全通过。
- `verify_course.py` 检查 assignment scaffold、Python 编译、作业测试。

人工评分证据：

- 代码没有硬编码公开测试。
- 学生能解释一个失败测试的根因。
- 助教抽查隐藏边界测试、性质测试和代码质量。

最低通过标准：

- 每个作业目录包含 `README.md`、`starter.py`、`reference_solution.py`、`tests.py`。
- 所有公开测试通过。
- 隐藏测试覆盖 shape、mask、dtype、非法参数和数值稳定性。

## Outcome 3: 推导关键公式与复杂度

目标表述：学生能推导或解释 BPE merge、RoPE 相对位置、attention scaling、LayerNorm、cross entropy、DPO/GRPO、KV Cache 显存。

教学材料：

- Ch01-Ch10 公式和 shape 说明。
- [Mathematical Derivation Audit](mathematical-derivation-audit.md) 的 DER-01 到 DER-14。
- [书面推导与概念题题库](written-problem-set.md)。
- [数学与 PyTorch 先修复习](math-prerequisites.md)。

学生交付：

- 每次书面作业 2-3 道推导题。
- 阅读复盘中的一个公式或实验设计。
- Capstone 报告中的复杂度、显存或成本估算。

自动证据：

- `verify_course.py` 检查 393 个公式属性、控制字符和 HTML 链接。
- `verify_course.py` 检查 mathematical derivation audit 的 assumptions、shape、evidence 和 boundary 字段。
- Ch02、Ch03、Ch05、Ch07、Ch09、Ch10 作业测试覆盖 RoPE、attention、norm、CE、DPO/GRPO、KV cache。

人工评分证据：

- 推导链条完整，shape 一致。
- 能说明公式适用条件和边界。
- 能区分计算复杂度、显存复杂度和工程瓶颈。

最低通过标准：

- 书面题覆盖至少 7 类关键公式中的 5 类。
- 推导不只写结论，必须包含符号定义、shape 和边界条件。

## Outcome 4: 复现训练与推理工程实验

目标表述：学生能设计并复现训练工程与推理工程实验，报告 seed、环境、日志、指标和失败案例。

教学材料：

- Ch07、Ch10。
- `projects/training-engineering-capstone/`。
- `projects/inference-engineering-capstone/`。
- [Capstone 项目报告 Rubric](project-report-rubric.md)。
- [Compute Resource and Cost Guide](compute-resource-guide.md)。

学生交付：

- 训练 capstone：数据审计、训练日志、checkpoint/resume、成本估算。
- 推理 capstone：OpenAI-compatible API、评测、benchmark、SLO、容量规划。
- 资源预算：CPU/GPU/API 使用、成本记录、失败重跑和降级路径。
- 项目展示和复现包。

自动证据：

- `verify_course.py --capstone --training`。
- inference capstone acceptance：health、evaluation、benchmark、SLO、capacity plan。
- training capstone acceptance：data audit、train、resume、training plan。

人工评分证据：

- 项目报告包含 ablation、失败案例、日志和环境说明。
- 项目报告中的成本、GPU/API 使用和失败重跑次数能从日志或平台记录复核。
- 同伴 review 能复现命令或指出首个失败点。
- 助教检查报告数字与日志一致。

最低通过标准：

- 两个 capstone acceptance 通过。
- 报告中必须有 seed、环境、固定评测集、至少三个失败案例和复现命令。

## Outcome 5: 区分来源等级与前沿不确定性

目标表述：学生能区分基础理论、论文结论、模型卡声明、新闻报道和社区传闻。

教学材料：

- [前沿模型来源等级与复核记录](frontier-source-audit.md)。
- [逐周阅读清单与复盘 Handout](reading-list.md)。
- [Paper Recap Calibration Pack](paper-recap-calibration-pack.md)。
- [Paper-to-Code Traceability Matrix](paper-to-code-traceability-matrix.md)。
- Ch09-Ch10 的来源边界说明。

学生交付：

- 阅读复盘。
- Paper recap anchor sample 校准记录。
- 项目报告引用表。
- 前沿模型 claim 的来源审计。

自动证据：

- `verify_course.py` 检查 README 和 source audit 中的来源等级、复核日期和 D 级 monitor-only 降级标记。
- `verify_course.py` 检查 paper recap calibration pack 的 anchor samples、required fields 和 TA calibration procedure。
- Markdown/HTML 链接检查防止引用入口断裂。

人工评分证据：

- 引用包含作者/机构、标题、链接、访问日期、使用位置。
- 学生能说明哪些说法来自论文，哪些来自模型卡，哪些只是课程解释。
- 对 D 级 monitor-only 项不写成稳定事实，也不放入作业、考试或项目评分事实。

最低通过标准：

- 所有前沿模型数字或规格必须有来源等级和复核日期。
- C/D 级来源不得作为考试或作业事实。

## Outcome 6: 理解经典 NLP 与评测专题

目标表述：学生能理解 dependency parsing、seq2seq/NMT、BERT/encoder-only、BLEU/ROUGE/F1/EM 和安全/伦理评测。

教学材料：

- [经典 NLP 专题 Handout](classic-nlp-handout.md)。
- [经典 NLP 与评测覆盖说明](nlp-evaluation-coverage.md)。
- [10 周 / 20 讲 Lecture Plan](lecture-plan.md) Week 8。

学生交付：

- `assignments/ch11_classic_nlp/`。
- 经典 NLP 专题书面题。
- 第 8 周阅读复盘和同伴 review。

自动证据：

- Ch11 测试覆盖 UAS/LAS、BLEU、ROUGE-L、QA EM/F1 和 BERT MLM mask。
- `verify_course.py` 检查 Ch11 scaffold 并运行 11 个 assignment suite。

人工评分证据：

- 学生能比较 encoder-only、encoder-decoder 和 decoder-only 的适用任务。
- 学生能说明 BLEU/ROUGE/F1/EM 的局限。
- 学生能列出隐私、偏见、幻觉、评测污染和安全拒答中的至少三个风险与缓解策略。

最低通过标准：

- Ch11 公开测试通过。
- 书面题至少覆盖 dependency parsing、BERT/MLM 和 evaluation 三类专题。

## 自动门禁覆盖矩阵

| 门禁 | 覆盖内容 | 不能证明什么 |
|------|----------|--------------|
| `.venv/bin/python verify_course.py` | 章节统计、链接、文档标记、作业 scaffold、JS/Python 编译、公式格式、11 个公开测试 suite | 学生答案质量、隐藏边界、课堂互动质量 |
| `.venv/bin/python run_assignment_tests.py` | 公开作业测试可运行，参考解通过 | 隐藏测试和非典型实现质量 |
| `.venv/bin/python verify_course.py --capstone --training` | 两个 capstone 的最小 acceptance、benchmark、SLO、resume | 项目报告深度、真实生产部署质量 |
| Markdown/HTML link checks | 本地文档、章节、图片、脚本和项目链接不破 | 外部链接仍需定期人工复核 |
| KaTeX/data-expr checks | 公式属性非空、无异常拼接、无控制字符 | 公式数学内容是否正确 |

## 人工审查清单

教师或助教在课程发布前应抽查：

- 每个 outcome 至少有一项自动证据和一项人工评分证据。
- 每个作业至少有一个隐藏边界测试和一个隐藏性质测试。
- 每个 capstone 报告 rubric 项都有可观察证据。
- 每周阅读复盘至少有一个来源审计问题。
- 前沿模型 claims 在 `frontier-source-audit.md` 中有复核日期和来源等级。

## 课程运行后应收集的证据

| 证据 | 用途 |
|------|------|
| 隐藏测试通过率分布 | 判断公开测试是否过窄或过难 |
| 学生最常见错误 | 更新 lecture recap、office hours 和 autograder hints |
| 项目复现失败日志 | 改进 capstone README 和验收脚本 |
| 阅读复盘质量样例 | 校准来源审计和引用评分 |
| 同伴 review 修改说明 | 判断 peer review 是否真正改善项目 |
