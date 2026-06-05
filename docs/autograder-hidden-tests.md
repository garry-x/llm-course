# Autograder 与隐藏测试设计指南

本指南供教师和助教设计正式评分环境使用。公开测试用于帮助学生定位实现错误；隐藏测试用于覆盖边界条件、数值稳定性、泛化输入和防止针对公开样例的硬编码。每个作业的 written/programming 组成见 [Assignment Handout Pack](assignment-handout-pack.md)，代码质量人工复核见 [Programming Assignment Code Quality Rubric](programming-assignment-code-quality-rubric.md)；真实私有运行流程、manifest 和 LMS entrypoint 见 [Private Autograder Operations Guide](private-autograder-operations.md)。

不要把隐藏测试源码或精确输入发布给学生。可以公开测试类别、评分比例、允许误差和复核流程。

## 评分分层

| 层级 | 权重建议 | 目的 | 示例证据 |
|------|:--:|------|----------|
| 公开单元测试 | 40-50 | 验证核心 API、shape、典型路径 | `assignments/ch*/tests.py` |
| 隐藏边界测试 | 20-30 | 覆盖空输入、极端 shape、mask、dtype、非法参数 | autograder 私有用例 |
| 隐藏性质测试 | 15-25 | 检查数学不变量，而不是固定输出 | norm preservation、概率归一化、cache equivalence |
| 书面解释/代码质量 | 10-20 | 检查学生能否解释实现、复杂度和失败模式 | 报告、推导题、代码审阅 |

正式成绩不应只由公开测试决定。公开测试全过只能证明典型用例正确，不能证明边界条件、数值稳定性或工程判断达标。

## Autograder 基本规则

- 每个作业必须固定 Python、PyTorch、NumPy 版本范围，并记录运行命令。
- 学生发布包必须由 `scripts/build_assignment_release.py` 构建或按同等规则排除 `reference_solution.py`。
- 教师私有 dry run 和正式 hidden-test manifest 应由 `scripts/run_private_autograder.py` 或同等入口生成。
- 所有随机测试必须设置 seed，并在失败日志中输出 seed。
- 浮点比较使用 `rtol`/`atol`，不要要求逐 bit 相等。
- 隐藏测试应调用学生提交的公开 API，不依赖私有变量名，除非该变量是作业明确要求。
- 对 GPU 非必需作业，隐藏测试默认在 CPU 可运行；GPU 项目另设性能验收。
- 每个失败项都应映射到 rubric 中的具体评分项。
- 学生提交不得访问网络、读取参考答案、修改测试文件或依赖当前工作目录外的非授权文件。

## 数值容差建议

| 场景 | 建议容差 | 说明 |
|------|----------|------|
| 纯整数/token 操作 | 精确相等 | BPE merge、vocab id、mask boolean |
| FP32 attention/logits | `rtol=1e-5`, `atol=1e-6` | 与 PyTorch 或 reference 对齐 |
| FP64 gradcheck | `rtol=1e-4`, `atol=1e-6` | 小张量、双精度、确定性输入 |
| 采样分布 | 统计范围或集合约束 | 不比较单次随机 token |
| 训练 loss | 趋势和有限值 | 不要求固定最终 loss，检查 loss finite、下降区间、checkpoint |
| 量化/近似检索 | 误差上界或 ranking 约束 | 检查 top candidate、cosine order、反量化误差 |

## Ch01 Tokenization / BPE

隐藏测试类别：

- 空语料、单 token 序列、多字节 UTF-8、emoji、中文和英文混合文本。
- 多个 pair 频率相同的 tie-breaking；要求学生输出稳定且与作业规则一致。
- `_merge` 中重叠 pair：例如 `[1, 1, 1]` 合并 `(1, 1)` 只能产生一个新 token 加一个剩余 token。
- vocab size 小于 256、等于 256、略大于 byte vocab 的边界。
- encode/decode round trip 不应依赖训练语料只出现过的字符串。

人工复核触发：

- 公开测试通过但隐藏测试显示 tie-breaking 不稳定。
- 学生实现绕过 BPE 训练，直接对测试字符串做字典匹配。

## Ch02 Embedding / Position Encoding / RoPE

隐藏测试类别：

- batch/sequence 维度为 1、长序列、不同 `d_model` 和 odd dimension 拒绝。
- embedding lookup 与 one-hot 矩阵乘法等价，但不能实际构造巨大 one-hot 作为默认路径。
- sinusoidal buffer 不应是可训练参数；device/dtype 迁移后仍能 forward。
- RoPE 应保持向量范数；相对位置 attention score 应满足 Toeplitz 性质。
- 对非法 head_dim、超出 max_len 的输入给出清晰错误或扩展策略。

人工复核触发：

- 只对固定 shape 通过，换 batch 或 seq_len 即失败。
- 把 RoPE 实现成绝对位置加法编码。

## Ch03 Scaled Dot-Product Attention

隐藏测试类别：

- 2D/3D/4D mask broadcast；全 mask 行的行为需按作业说明处理。
- softmax 前 mask 与 softmax 后 mask 的差异；被 mask token 概率必须为 0。
- 大 logits 数值稳定性，不能产生 NaN。
- causal mask 在 `T=1`、`T=2`、非方阵 decode query 场景下正确。
- backward 梯度存在且 shape 正确。

人工复核触发：

- 学生在 softmax 后乘 mask 且不重新归一化。
- 用 Python 循环逐元素实现导致合理规模输入超时。

## Ch04 MHA / GQA / MLA

隐藏测试类别：

- `d_model` 不能整除 `n_heads` 时必须拒绝。
- MHA 输出 shape、attention probability 归一化、mask 广播。
- GQA 中 `n_heads` 与 `n_kv_heads` 的分组关系；非法分组拒绝。
- KV cache size ratio 对不同 head 数、batch、dtype 的公式正确。
- MLA latent cache shape、RoPE 分支 shape 和参数量不能退化为完整 MHA cache。

人工复核触发：

- 把 GQA 错误实现为减少 Q heads。
- 只返回正确 shape，但 attention 权重没有实际参与计算。

## Ch05 Transformer Block / Norm / FFN

隐藏测试类别：

- LayerNorm/RMSNorm 与 PyTorch reference 或数学定义对齐。
- `eps` 对接近零方差输入防止 NaN。
- Pre-Norm block 梯度能流到 attention、FFN 和 norm 参数。
- GELU FFN 与 SwiGLU 参数量、hidden width 和输出 shape。
- dropout/eval 模式行为符合 PyTorch 约定。

人工复核触发：

- LayerNorm backward 只写局部项，未包含 mean/variance 的耦合。
- block forward 跳过 attention 或 FFN 但用 residual 掩盖 shape 错误。

## Ch06 GPT Assembly / MoE

隐藏测试类别：

- GPTConfig 默认值、可自定义小模型配置和超长序列拒绝。
- tied/untied LM head 参数对象关系和参数量审计。
- causal attention 不泄露未来 token：改变未来 token 不应改变当前位置 logits。
- 初始化 scale、bias、LayerNorm 参数符合要求。
- MoERouter top-k 权重归一化、非法 `top_k` 拒绝、负载偏置能改变路由倾向。

人工复核触发：

- 参数量靠硬编码常数通过，换配置后失败。
- forward 忽略 position embedding 或 block 列表。

## Ch07 Training Loop

隐藏测试类别：

- Dataset 对短文本、刚好一个 block、多个 block 的切片边界。
- Cross entropy 对极大/极小 logits 数值稳定。
- AdamW 单步更新与手算 reference 对齐。
- warmup/cosine scheduler 在 step 0、warmup 结束、总步数结束边界正确。
- 训练循环记录 loss、lr、grad_norm、tokens/s，并能处理 resume checkpoint。

人工复核触发：

- 每步重新创建 optimizer，导致状态无法累积。
- checkpoint 保存但 resume 后 step、optimizer state 或 scheduler state 不一致。

## Ch08 Generation / Decoding

隐藏测试类别：

- temperature 为 0 时退化为 greedy；非法 temperature/top-k/top-p 拒绝。
- top-p 必须保留累计概率达到阈值的最小集合，并至少保留一个 token。
- top-k 大于 vocab size 时应 clamp 或按说明处理。
- speculative decoding 的返回 token 数、target 调用次数、接受率统计合理。
- generation loop 遇到 EOS、max_new_tokens、空 prompt 的行为明确。

人工复核触发：

- 采样前没有重新归一化过滤后的概率。
- speculative decoding 只是顺序调用 target model，没有利用 draft 验证。

## Ch09 Fine-tuning / Alignment

隐藏测试类别：

- SFT labels 中 prompt 和 padding 必须为 `-100`；gather 前要处理 ignore index。
- LoRA 初始输出应等于 base layer；训练参数只包含 LoRA 参数。
- merge_lora 后权重增量正确，且推理不再依赖 adapter 分支。
- DPO loss 对 chosen/rejected log-ratio 的方向正确。
- GRPO advantage 在每个 prompt group 内白化，单样本 group 不产生 NaN。

人工复核触发：

- 学生把 rejected/chosen 方向写反但公开样例没覆盖。
- 冻结参数不彻底，导致 base model 被更新。

## Ch10 Inference / RAG / Serving

隐藏测试类别：

- incremental KV attention 与 full causal attention 在多个 batch、head、decode step 下等价。
- KV cache memory 必须包含 batch、layers、K/V 两份、kv heads、head_dim、context、dtype bytes。
- INT8 per-channel quantization 对全零、常数、大范围权重稳定。
- RAG chunk overlap 非法值拒绝；检索按 cosine similarity 排序。
- benchmark summary 必须包含 TTFT、TPOT、tokens/s、P50/P95/P99、error_rate。
- LSH 只能在同桶候选中排序；空桶 fallback 行为明确。

人工复核触发：

- 容量规划公式漏 batch 或漏 K/V 2 倍。
- 只报告平均延迟，缺少尾延迟或错误率。

## Ch11 Classic NLP and Evaluation

隐藏测试类别：

- Dependency parsing 的 UAS/LAS 对 root、非法 head、长度不匹配和 label mismatch 的处理。
- BLEU 的 clipped precision、brevity penalty、多 reference 和空候选/空参考边界。
- ROUGE-L 的 LCS、precision/recall/F1、空输入和完全不重叠输入。
- QA exact match / F1 的 normalize 规则、多个 gold answer、标点和大小写处理。
- BERT-style MLM example 的 mask position 合法性、原始 token label、未 mask token 的 ignore index。

人工复核触发：

- 学生把 BLEU/ROUGE/EM/F1 当成开放式生成质量的充分证明。
- 只对公开样例字符串硬编码，换 reference、标点或大小写即失败。

## Capstone 隐藏验收

训练工程：

- 数据审计应发现空行、重复行、长度异常和字符集异常。
- 训练必须能从 checkpoint resume，且 resume 后 step 单调增加。
- metrics 文件应包含 train_loss、val_loss、lr、grad_norm、tokens_per_second。
- 成本规划必须能随 tokens、batch、吞吐、GPU 单价变化。

推理工程：

- OpenAI-compatible endpoint 应处理 invalid JSON、空 message、tool call 和 stream。
- 评测集至少包含事实问答、结构化输出、RAG、工具调用和拒答/安全边界。
- benchmark 必须输出 P50/P95/P99、TTFT、TPOT、tokens/s、error_rate。
- SLO 检查必须能让失败指标明确失败，而不是只打印报告。

## 学术诚信与防投机检查

自动检查：

- 禁止提交文件读取 `reference_solution.py`、`tests.py` 或隐藏测试路径。
- 禁止硬编码公开测试输入、输出或文件名。
- 禁止在作业测试中访问网络。
- 对相似度过高的提交进行人工复核，尤其是非平凡错误也完全一致的情况。

人工复核：

- 要求学生解释一个隐藏失败用例的原因和修复思路。
- 抽查代码能否在改名模块、不同 seed、不同 shape 下运行。
- 对高分但解释薄弱的提交，要求补充 shape、复杂度或错误分析。

## 失败日志规范

隐藏测试失败日志应包含：

- 作业名和 rubric 项。
- 测试类别，不暴露完整隐藏输入。
- seed、shape、dtype、device。
- 期望性质，例如“masked probability must be zero”。
- 学生输出的摘要，例如 shape、是否 NaN、误差上界。

示例：

```text
Assignment: ch03_attention
Rubric: mask application
Hidden category: 4D broadcast mask
Seed: 22403
Shape: batch=2, heads=3, query=4, key=4, dtype=float32
Expected property: masked probabilities sum to 0 on masked positions and unmasked rows sum to 1
Observed: masked probability max=0.18
```
