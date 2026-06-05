# Programming Assignment Code Quality Rubric

复核日期：2026-06-05

本 rubric 用于评估 Ch01-Ch11 编程作业中公开测试和隐藏测试之外的代码质量证据。它补充 [Assignment Handout Pack](assignment-handout-pack.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Autograder 与隐藏测试设计指南](autograder-hidden-tests.md)、[Grading Calibration Guide](grading-calibration.md)、[Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md)、[Academic Integrity Case Process](academic-integrity-case-process.md)、[Notation and Shape Glossary](notation-shape-glossary.md)、[Environment and Reproducibility Guide](environment-reproducibility.md)、[Python and PyTorch Review Session](python-pytorch-review-session.md)、[Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md) 和 [Learning Outcome Attainment Report](learning-outcome-attainment-report.md)。

使用边界：本文件可以进入 student site release。它公开评分维度、人工复核触发器和学生自查清单，但不包含 hidden tests、reference_solution.py、private grading samples、real student submissions 或未公开评分脚本。

## Rubric Dimensions

| dimension_id | dimension | full_credit_evidence | partial_credit_signal | no_credit_signal | evidence |
|--------------|-----------|----------------------|-----------------------|------------------|----------|
| CQR-API | API contract | 保持 starter 函数、类、参数名、返回类型和异常语义 | 主路径可用但改动 optional 参数或返回附加对象 | 改函数签名、改 tests、绕过 STUDENT_MODULE | starter.py、tests.py、run_log |
| CQR-SHAPE | shape discipline | 每个核心 tensor 变换能解释 batch、time、head、dim 或 vocab 轴 | 典型 shape 通过但边界 shape 解释不完整 | 硬编码 batch、seq_len、head 数或 vocab size | written_answers、shape trace |
| CQR-VECTOR | idiomatic PyTorch | 使用张量操作、broadcast、matmul、gather、mask 和模块组合完成核心计算 | 小规模循环可接受但复杂度或设备迁移说明不足 | 用逐元素 Python 循环替代应向量化的 attention、loss 或 metric | code review、timing note |
| CQR-NUMERIC | numerical stability | 对 softmax、CE、norm、quantization、mask 和 optimizer 更新有稳定实现 | 主路径稳定但极端 logits、零方差或全 mask 处理弱 | NaN、inf、除零或未定义概率未处理 | public/hidden category feedback |
| CQR-DEVICE | dtype and device | buffer、parameter、输入 tensor 在 CPU、GPU、dtype 迁移时一致 | 仅 CPU 通过或 dtype 假设写死但容易修 | 创建新 tensor 时脱离输入 device 或强制 float64/int64 导致失败 | smoke test、manual review |
| CQR-BOUNDARY | boundary handling | 对空输入、非法参数、odd dimension、超长序列和错误 overlap 给出清晰行为 | 只覆盖部分非法输入或错误信息不清 | 静默返回错误结果或靠默认值掩盖异常 | tests、error_analysis |
| CQR-READABLE | readability and modularity | 代码分层清楚，变量名对应课程符号，复杂块有简短注释 | 可读但重复较多或局部命名不清 | 大段复制、不可解释魔法常数或无关重构破坏 starter | code review |
| CQR-REPRO | reproducibility evidence | 提交 run_log、环境、seed、失败案例和必要的小反例 | run_log 有但缺 cwd、版本或 first failure | 不能复现测试输出或依赖本机绝对路径、网络、隐藏变量 | run_log、environment record |
| CQR-INTEGRITY | integrity and anti-hardcoding | 不读取 reference、tests 或隐藏路径；不硬编码公开输入、seed 或断言 | 写法过窄但能解释并修正 | 复制 reference、读取 tests、硬编码公开样例或伪造日志 | academic integrity review |

## Assignment-Specific Review Cues

| cue_id | assignment | code_quality_focus | strong_manual_check | red_flag |
|--------|------------|--------------------|---------------------|----------|
| CQR-CH01 | Ch01 BPE | 非重叠 merge、tie-breaking、UTF-8 round trip | 换未见中英文混合文本仍能 encode/decode | 对公开字符串做字典匹配 |
| CQR-CH02 | Ch02 Embedding/RoPE | buffer、lookup、成对旋转、device/dtype | 改 batch、seq_len、head_dim 后 shape 和 norm 仍正确 | RoPE 写成绝对加法位置编码 |
| CQR-CH03 | Ch03 Attention | mask broadcast、softmax 前 mask、数值稳定 | 2D/3D/4D mask 和大 logits 不产生 NaN | softmax 后乘 mask 且不重归一 |
| CQR-CH04 | Ch04 MHA/GQA/MLA | head split、GQA 分组、latent cache shape | 非默认 head 配置仍能拒绝或正确计算 | 只返回正确 shape，未实际计算 attention |
| CQR-CH05 | Ch05 Block/Norm/FFN | norm 公式、eps、pre-norm、grad flow | 零方差输入和 gradcheck 有解释 | 跳过子层但靠 residual 掩盖 |
| CQR-CH06 | Ch06 GPT/MoE | 参数对象、causal leakage、初始化、router | 改 GPTConfig 后参数量和 forward 仍一致 | 参数量或 logits 依赖硬编码常数 |
| CQR-CH07 | Ch07 Training | CE、AdamW、scheduler、checkpoint resume | resume 后 step、optimizer state 和 logs 连贯 | 每步重建 optimizer 或不保存 state |
| CQR-CH08 | Ch08 Generation | 采样过滤、renormalization、EOS、speculative stats | top-k/top-p 边界和 max_new_tokens 行为明确 | 过滤后概率未重归一 |
| CQR-CH09 | Ch09 Alignment | ignore index、LoRA 冻结、DPO 方向、GRPO group | chosen/rejected 方向和单样本 group 不出 NaN | 更新 base model 或 log-ratio 方向反 |
| CQR-CH10 | Ch10 Inference/RAG | KV cache、quantization、RAG overlap、benchmark summary | batch/layer/KV 两份和 P95/P99 都能解释 | 只报告平均 latency 或漏 K/V 2 倍 |
| CQR-CH11 | Ch11 Classic NLP | metric normalization、multi-reference、MLM labels | BLEU/ROUGE/EM/F1 在空输入和多答案下稳定 | 把指标当开放生成质量充分证明 |

## Manual Review Triggers

| trigger_id | condition | required_action | possible_outcome |
|------------|-----------|-----------------|------------------|
| CQR-TRIG-PUBLIC-HIDDEN | public tests pass but hidden boundary or hidden property category fails | 抽查 shape、dtype、边界和错误分析 | keep score, partial credit, or require correction note |
| CQR-TRIG-HARDCODE | 输出只匹配公开样例、公开 seed 或固定 shape | 运行公开样例变体并检查代码路径 | integrity review or code-quality cap |
| CQR-TRIG-REFERENCE | 提交导入、读取或复制 reference_solution.py | 冻结提交并按 Academic Integrity Case Process 处理 | integrity case |
| CQR-TRIG-API | 函数签名、类名、返回类型或模块入口改变 | 对照 starter API contract | reject or manual adapter not allowed |
| CQR-TRIG-NUMERIC | 出现 NaN、inf、全 mask 未定义或极端 logits 不稳 | 检查稳定公式和容差 | numerical stability deduction |
| CQR-TRIG-DEVICE | CPU 通过但 device/dtype 迁移失败 | 检查 new tensor 创建、buffer 注册和 dtype cast | device/dtype deduction |
| CQR-TRIG-READABILITY | 代码难以解释、魔法常数多或无关重构破坏 starter | 要求学生指出核心函数和变量含义 | readability deduction or oral follow-up |

## Student Self-Check

提交前逐项确认：

| check_id | question | evidence_to_submit |
|----------|----------|--------------------|
| CQR-SC-API | 我是否保留 starter API、文件名和 STUDENT_MODULE 入口 | diff or note |
| CQR-SC-SHAPE | 我能否写出核心 tensor 的输入输出 shape | written_answers or comments |
| CQR-SC-BOUNDARY | 我是否尝试至少一个公开测试外的边界输入 | error_analysis |
| CQR-SC-NUMERIC | 我是否检查 NaN、inf、全 mask、零方差或大 logits | run_log or small repro |
| CQR-SC-DEVICE | 我是否避免把新 tensor 固定在错误 device 或 dtype | code review note |
| CQR-SC-REPRO | TA 能否用我的命令复现公开测试结果 | run_log.txt |
| CQR-SC-INTEGRITY | 我是否披露 AI 工具、外部代码和协作 | honor_statement |

## TA Review Workflow

1. 先运行公开测试和正式 autograder 类别，记录 public、hidden_boundary、hidden_property 和 error category。
2. 对触发 Manual Review Triggers 的提交，抽查代码质量维度，不用逐行审阅所有通过提交。
3. 抽查时优先看 API contract、核心 tensor shape、非法输入、dtype/device、新 tensor 创建、硬编码迹象和 run_log。
4. 将扣分映射到 CQR dimension_id，并把类别级高频问题写入 [Course Operations and Improvement Log](course-operations-log.md) 或下一次 recitation。
5. 对 integrity 线索只记录必要证据摘要，按 [Academic Integrity Case Process](academic-integrity-case-process.md) 私密处理。

## Release Checklist

- Rubric Dimensions 覆盖 API、shape、idiomatic PyTorch、numerical stability、dtype/device、boundary handling、readability、reproducibility 和 integrity。
- Assignment-Specific Review Cues 覆盖 Ch01-Ch11。
- Manual Review Triggers 覆盖 public/hidden split、hardcoding、reference access、API drift、numeric instability、device/dtype 和 readability。
- Student Self-Check 包含 API、shape、boundary、numeric、device、reproducibility 和 integrity。
- TA Review Workflow 能把扣分映射到 CQR dimension_id，并连接 operations log 和 academic integrity process。
- student site release 排除 hidden tests、reference_solution.py、private grading samples、real student submissions 和未公开评分脚本。
