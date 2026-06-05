# Midterm and Final Review Pack

本文件提供可直接发布给学生的期中 checkpoint 样卷和期末复习样题。它补充 [Comprehensive Review Study Guide](comprehensive-review-study-guide.md)、[Quiz and Checkpoint Guide](quiz-checkpoint-guide.md)、[Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md)、[Board Derivation and Instructor Notes Pack](board-derivation-pack.md)、[书面推导与概念题题库](written-problem-set.md) 和 [Instructor Solution Guide](instructor-solution-guide.md)。目标是让阶段评估不只停留在“指南”，而有可执行的样题、评分口径、管理流程和补救路径。

复核日期：2026-06-05

## 使用规则

- 本文件可以公开给学生作为样卷和复习材料。
- 正式 checkpoint 应替换数字、语料或日志片段，保持能力目标不变。
- 不使用隐藏测试、reference solution 代码或学生提交作为题目。
- 评分时优先检查推导链条、shape、边界条件、实验判断和来源边界。
- 若本样卷变成计分 assessment，必须按 [Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md) 公告 assessment_id、allowed materials、duration、makeup、regrade window 和 accommodation path。
- 若学生有正式便利安排，按 [Accessibility and Student Support Guide](accessibility-student-support.md) 调整时间或形式。

## Midterm Checkpoint Sample

建议时长：60 分钟。
覆盖范围：Ch01-Ch07。
建议计分：可计入书面/参与小分，不超过课程总评 5%。
允许材料：一页手写公式表；不允许联网搜索或运行代码。

### 题 1：BPE 与 Embedding Shape

给定语料片段：

```text
low lower lowest newer
```

1. 写出 byte/character-level 起始 token 序列后，说明 BPE 每轮 merge 如何选择 pair。
2. 解释为什么贪心 BPE 不保证全局最优压缩。
3. 若词表大小 `V=32000`，embedding dim `D=768`，计算 token embedding 参数量。
4. 说明 `one_hot @ E` 与 `E[token_id]` 为什么等价。

评分要点：

- 能说明相邻 pair 统计和非重叠 merge。
- 能指出贪心只优化当前频次，不回溯。
- 参数量为 `32000 * 768`，可写成约 24.6M。
- embedding lookup 应明确输出 shape，例如单 token 为 `[D]`，batch 序列为 `[B,T,D]`。

### 题 2：RoPE 与 Attention Scaling

设 `q,k in R^{D_h}`，RoPE 对位置 `m,n` 分别使用旋转矩阵 `R_m, R_n`。

1. 推导 `(R_m q)^T (R_n k) = q^T R_{n-m} k`。
2. 指出这个推导为什么不等于“任意长度上下文都能稳定外推”。
3. 若 `q_i,k_i` 独立、均值 0、方差 1，推导 `Var(q^T k)`。
4. 说明 attention score 为什么除以 `sqrt(D_h)`。

评分要点：

- 必须写出 `R_m^T R_n = R_{n-m}`。
- 长上下文边界需提到训练长度、频率设计、数值范围或注意力模式。
- 方差推导应得到 `D_h`。
- scaling 应放在 softmax 前，用于防止 logits 方差过大导致 softmax 饱和。

### 题 3：Causal Mask 与 MHA/GQA Cache

1. 写出 `T=4` 的 causal mask 可见矩阵。
2. 说明 mask 应在 softmax 前还是后应用，以及原因。
3. 给定 `B=2, layers=24, T=4096, H_kv=8, D_h=128, dtype=FP16`，推导 KV cache 显存公式并估算 GB。
4. 解释 GQA 减少的是哪个变量，为什么不等于减少所有 attention 计算。

评分要点：

- 可见矩阵应为下三角。
- softmax 前 mask；softmax 后直接置零会破坏概率归一化。
- 公式：`2 * B * layers * T * H_kv * D_h * dtype_bytes`。
- 估算：`2*2*24*4096*8*128*2 = 805,306,368 bytes`，约 0.75 GiB。
- GQA 减少 `H_kv`，Q head 和其他投影/调度成本仍存在。

### 题 4：GPT / MoE / Training Loop

1. 解释 next-token label 为什么要右移一位。
2. 说明 tied LM head 如何影响参数量审计。
3. MoE 的 total parameters 与 activated parameters 有什么区别？
4. 给出 AdamW 与 Adam + L2 的关键区别。
5. 训练日志出现 loss spike、grad norm 突增、tokens/s 下降时，各列出一个可能原因。

评分要点：

- 位置 `t` 的 hidden state 预测 `x_{t+1}`。
- tied LM head 不重复计数输出 projection。
- MoE total 是所有专家总参数，activated 是每 token 实际走过的专家参数。
- AdamW 将 weight decay 与 Adam 自适应梯度更新解耦。
- 失败诊断应具体：学习率/异常样本/AMP 溢出/梯度爆炸/dataloader/长样本/硬件争用等。

### 题 5：来源与复现边界

给定报告片段：

```text
某模型支持 1M context，因此我们的 RAG 系统在所有长文档问答上都能保持准确。
我们使用一次 demo 的平均延迟 210ms 证明系统满足上线要求。
训练从 checkpoint 恢复后 loss 继续下降，但报告没有给 seed、optimizer state 或 step。
```

指出至少 5 个问题，并给出修正建议。

评分要点：

- 模型卡 context 不等于所有任务准确。
- RAG 需要检索质量、生成质量和忠实性评测。
- 平均延迟不足以证明 SLO，需要 P95/P99、TTFT/TPOT、错误率和并发设置。
- checkpoint resume 需要 seed、model/optimizer/scheduler state、step、config 和日志连续性。
- 前沿模型 claim 需要来源、日期、任务设置和边界。

## Midterm Remediation Map

| 低分模块 | 触发条件 | 补救任务 | 验收证据 |
|----------|----------|----------|----------|
| Token / embedding | 题 1 低于 60% | 重做 Ch01-Ch02 starter，并写 1 页 token cost 分析 | Ch01/Ch02 tests + 助教口头抽查 |
| RoPE / scaling | 题 2 低于 60% | 完成 board derivation pack 中 RoPE 和 attention scaling 两节复述 | 交一页推导和 shape |
| Mask / cache | 题 3 低于 60% | 完成 Ch03 mask failure drill 和 Ch10 KV cache 公式题 | 助教检查公式和一个数值例子 |
| Training loop | 题 4 低于 60% | 提交 loss spike / NaN 排查记录 | 包含命令、日志、原因和修正 |
| Source / reproducibility | 题 5 低于 60% | 复核 1 个模型卡 claim，补 checkpoint resume 证据模板 | source audit 表 + resume checklist |

## Final Review Sample

建议用途：Week 10 复习，不替代 capstone report。
建议形式：开卷讨论或 45 分钟短测。

### 题 A：Generation / Decoding

给定词表概率 `[0.40, 0.25, 0.20, 0.10, 0.05]`：

1. top-k 当 `k=2` 时保留哪些 token？
2. top-p 当 `p=0.7` 和 `p=0.9` 时分别保留哪些 token？
3. 为什么 distinct n-gram 不能单独证明回答质量？
4. 推测解码为什么可能不加速？

评分要点：

- top-k 保留前两个。
- `p=0.7` 保留前三个；`p=0.9` 保留前四个。
- distinct 只看局部多样性，不看事实、任务完成和安全。
- draft 过慢、接受率低、batching/kernel/服务瓶颈都会影响收益。

### 题 B：SFT / LoRA / DPO / GRPO

1. 给定 prompt + response 序列，说明哪些 label 应设为 `-100`。
2. LoRA rank 增大会影响哪些量？
3. DPO chosen/rejected 方向写反会怎样？
4. GRPO 组内白化解决什么问题，又不能解决什么问题？

评分要点：

- prompt 和 padding mask 掉，只训练 assistant response。
- rank 影响可训练参数、表达能力、显存/计算和过拟合风险。
- 写反会奖励 rejected response。
- 组内白化缓解 reward scale 差异，不能修复错误 reward、分布外泛化或安全漏洞。

### 题 C：Classic NLP / Evaluation

1. 区分 UAS 和 LAS。
2. 比较 BERT MLM 与 causal LM 的 mask 和训练目标。
3. 说明 BLEU、ROUGE、EM/F1 各自适用场景和局限。
4. 给一个开放式回答，为什么 LLM-as-judge 也需要校准？

评分要点：

- UAS 只看 head，LAS 同时看 head 和 label。
- BERT 双向 MLM，causal LM 只看左侧上下文预测下一个 token。
- 自动指标有任务假设，不能单独证明开放式 LLM 质量。
- LLM-as-judge 可能有位置偏置、模型偏置、污染和不可复现问题。

### 题 D：Inference / RAG / Serving

1. 推导 KV cache 显存公式。
2. 区分 TTFT、TPOT、tokens/s、throughput、P95 latency。
3. 给定 RAG 错误回答，按 chunking、embedding、retrieval、reranking、prompt assembly、generation 分类可能根因。
4. 为什么平均延迟不能证明系统可上线？

评分要点：

- 公式必须包含 K/V 两份、batch、layers、context、KV heads、head dim、dtype bytes。
- 指标解释要对应用户体验或成本。
- RAG 失败应定位到 pipeline 环节，而不是只说“模型不好”。
- 上线证据需要 P95/P99、错误率、并发、容量规划和回归评测。

### 题 E：Capstone Evidence and Source Audit

检查下面的项目声明：

```text
我们使用 V4 模型卡的 context 数字作为依据，认为系统可以处理所有 1M token 任务。
压测只跑了 5 个请求，均值延迟 300ms。
报告没有列出失败案例，因为最终 demo 成功。
引用了一个博客中的 benchmark 数字，没有访问日期。
```

列出问题并改写为可评分的项目结论。

评分要点：

- context 能力不是任务质量保证。
- 压测请求数、并发、P95/P99、错误率不足。
- 项目报告必须包含失败案例、ablation 或错误分析。
- benchmark 需要来源等级、访问日期、任务设置、模型/硬件/上下文。
- 结论应写成“在某配置和评测集下观察到”，不能写成普遍事实。

## Final Review Rubric

| 维度 | 满分标准 |
|------|----------|
| Core formulas | 能写出 RoPE、attention scaling、CE、DPO、KV cache 等关键公式的中间步骤 |
| Shape discipline | 每题能标出关键 tensor shape 或指标维度 |
| Engineering judgment | 能把公式连接到显存、延迟、训练稳定性、服务指标或复现证据 |
| Evaluation literacy | 能说明自动指标、RAG、LLM-as-judge 和 benchmark 的局限 |
| Source boundary | 前沿模型或性能数字均标注来源、日期、配置和边界 |

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| 可发布性 | 不含隐藏测试、reference solution 代码或学生提交 |
| 覆盖范围 | Midterm 覆盖 Ch01-Ch07；Final review 覆盖 Ch08-Ch10、经典 NLP、capstone 和来源审计 |
| 评分口径 | 每题有评分要点或最低合格答案 |
| 补救闭环 | Midterm 低分项能映射到补救任务和验收证据 |
| 管理流程 | 计分版本按 assessment administration policy 管理 allowed materials、makeup 和 regrade window |
| 链接有效 | 本文件链接通过 `.venv/bin/python verify_course.py` |
