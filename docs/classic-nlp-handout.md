# 经典 NLP 专题 Handout

本 handout 用于补齐 CS224N 风格课程中常见但本课程主线没有展开成独立章节的内容。授课时建议安排 1-2 次讨论课，或把它作为期末项目的背景阅读。

## 1. Dependency Parsing

Dependency parsing 的目标是为句子中的词建立有向依存边。例如 `I saw her` 中，`saw` 是谓词中心，`I` 依赖于 `saw` 作为主语，`her` 依赖于 `saw` 作为宾语。

### Arc-Standard Transition System

状态包含：

- Stack：已经部分处理的词。
- Buffer：尚未处理的词。
- Arcs：已建立的依存边。

操作：

- `SHIFT`：把 buffer 第一个词移到 stack。
- `LEFT-ARC(label)`：把 stack 顶部词作为 head，连接到次顶部 dependent，并弹出 dependent。
- `RIGHT-ARC(label)`：把次顶部词作为 head，连接到顶部 dependent，并弹出 dependent。

### Worked Example: `I saw her`

设 token 编号为 `0=I, 1=saw, 2=her`，gold arcs 为 `saw -> I (nsubj)`、`saw -> her (obj)`，`saw` 是 root。一个合法 arc-standard transition 序列如下：

| Step | Stack | Buffer | Action | New arc |
|------|-------|--------|--------|---------|
| 0 | `[]` | `[I, saw, her]` | `SHIFT` | - |
| 1 | `[I]` | `[saw, her]` | `SHIFT` | - |
| 2 | `[I, saw]` | `[her]` | `LEFT-ARC(nsubj)` | `saw -> I` |
| 3 | `[saw]` | `[her]` | `SHIFT` | - |
| 4 | `[saw, her]` | `[]` | `RIGHT-ARC(obj)` | `saw -> her` |
| 5 | `[saw]` | `[]` | `ROOT` 或结束 | `ROOT -> saw` |

课堂检查：

- `LEFT-ARC` 和 `RIGHT-ARC` 的 head/dependent 方向不能靠“左/右”字面猜，要看系统定义。
- 若预测 heads 为 `[1, -1, 1]`，labels 为 `["nsubj", "root", "obj"]`，UAS/LAS 都是 1.0。
- 若 `her` 的 head 预测为 `I`，但 label 仍是 `obj`，UAS 和 LAS 都会下降；LAS 只有在 head 与 label 同时正确时才计入。

### 指标

- UAS：Unlabeled Attachment Score，只看 head 是否正确。
- LAS：Labeled Attachment Score，同时要求 head 和 dependency label 正确。

课程用途：训练学生把结构预测问题拆成状态、动作、损失和评测，而不只看生成式 LLM。

## 2. Seq2Seq / Neural Machine Translation

Seq2Seq 模型把输入序列编码成上下文表示，再由 decoder 自回归生成目标序列。Attention 让 decoder 每一步根据当前状态对源端 token 加权，而不是只依赖一个固定向量。

### 核心问题

- Exposure bias：训练时 decoder 看到 gold prefix，推理时看到自己生成的 prefix。
- Beam search：保留多个候选序列，但容易偏向短句，因此常加 length penalty。
- Alignment：attention 权重可以粗略解释源词与目标词的对应关系，但不是严格因果解释。

### BLEU

BLEU 基于 n-gram precision 和 brevity penalty，适合机器翻译系统级比较，但对单句质量、语义等价改写和开放式生成不稳定。

### Worked Example: Beam Search Length Bias

假设 decoder 在某一步给出两个候选：

| Candidate | token log probs | sum log prob | length | normalized score `sum / length` |
|-----------|-----------------|--------------|--------|---------------------------------|
| `a` | `[-0.20]` | `-0.20` | 1 | `-0.20` |
| `a b c` | `[-0.20, -0.30, -0.30]` | `-0.80` | 3 | `-0.27` |

若只比较 log prob sum，短候选 `a` 更容易胜出，因为每多生成一个 token 都会乘上小于 1 的概率。长度归一化或 length penalty 不保证长句一定更好，但能减少“过短翻译”偏差。开放式生成中，beam search 还可能导致低多样性；sampling 则更适合探索多样输出，但需要温度、top-k/top-p 和安全过滤。

课堂检查：

- beam search 是搜索策略，不是训练目标。
- attention alignment 可作为翻译诊断，但不能自动证明模型因果解释。
- BLEU 的 brevity penalty 只能缓解过短输出，不解决语义等价改写、事实性或指代错误。

课程用途：帮助学生理解 decoder-only LLM 之前的 encoder-decoder 传统，以及为什么现代 instruction model 仍会用 beam/search/rerank 思路。

## 3. Encoder-only / BERT

BERT 使用双向 Transformer encoder，通过 Masked Language Modeling (MLM) 和 Next Sentence Prediction 预训练。与 causal LM 不同，MLM 可以同时看左右上下文，只预测被 mask 的位置。

### 与 Causal LM 的区别

| 维度 | BERT / Encoder-only | GPT / Decoder-only |
|------|---------------------|--------------------|
| 注意力 | 双向可见 | causal mask |
| 预训练 | MLM | next-token prediction |
| 输出 | token/CLS 表示 | 下一个 token logits |
| 典型任务 | 分类、抽取、序列标注 | 生成、对话、代码 |

课程用途：补齐表示学习和判别式 NLP 的经典路线，让学生理解并非所有 NLP 任务都天然需要自回归生成。

### Worked Example: BERT-style MLM Tensor

输入 tokens：

```text
[CLS] the cat sat [SEP]
```

若 mask positions 为 `[2, 3]`，则：

| Field | Value |
|-------|-------|
| masked input | `[CLS] the [MASK] [MASK] [SEP]` |
| labels | `None, None, cat, sat, None` |
| attention | 双向 self-attention，可看左右上下文 |
| loss positions | 只在 mask positions 计算 loss |

与 causal LM 对比：

- causal LM 训练 `the -> cat -> sat` 的 next-token prediction，只能看左侧上下文。
- MLM 可以同时利用 `the` 和 `[SEP]` 附近上下文预测 `cat/sat`，但不直接训练自回归生成。
- BERT fine-tuning 常用 `[CLS]` 表示做分类，也可做 token classification 或 span extraction；它不是默认的 decoder-only 生成模型。

## 4. Evaluation

高校 NLP 课程必须让学生区分“优化目标”和“评测指标”。

| 指标 | 适用任务 | 局限 |
|------|----------|------|
| Perplexity | 语言模型拟合 | 不直接等于事实正确或有用 |
| Accuracy / F1 | 分类、抽取 | 标签定义和类别不平衡会影响解释 |
| Exact Match | QA、代码、数学 | 对等价表达过于严格 |
| BLEU | 机器翻译 | 对语义改写和单句评价不稳定 |
| ROUGE | 摘要 | 偏向词面重合 |
| Human Eval | 开放式任务 | 成本高，一致性难保证 |
| LLM-as-judge | 大规模偏好评测 | 可能有位置偏置、模型偏置和污染风险 |

项目报告不能只给一个平均分。至少应包含分任务结果、失败案例、错误类型和指标局限。

### Metric Failure Cases

| Case | Metric looks good | Human issue | Lesson |
|------|-------------------|-------------|--------|
| Translation synonym | BLEU 低，因为 n-gram 不重合 | 语义可能正确 | BLEU 不能单句决定质量 |
| Extractive QA punctuation | EM 低，因为格式不同 | 答案实体相同 | EM 过严，需配合 normalized F1 |
| RAG copy overlap | ROUGE 高，因为复制检索片段 | 片段可能不回答问题 | 词面重合不等于事实正确 |
| Long answer latency | quality score 高 | P95 latency 超 SLO | 质量指标必须配合系统指标 |
| LLM judge preference | judge 偏好更长回答 | 可能冗余或幻觉 | 需要 blind pairwise、position swap 和人工抽查 |

课堂检查：

- 指标是任务假设的压缩，不是“真实质量”的同义词。
- 报告平均值时必须说明样本数、split、置信区间或 single_seed_limit。
- 对开放式 LLM 任务，自动指标、人工错误分析和资源指标应同时出现。

## 5. Ethics / Safety

LLM 课程的工程项目必须覆盖以下风险：

- 数据隐私：训练或 RAG 语料是否包含敏感信息。
- 偏见与代表性：数据是否系统性忽略某些语言、地区或群体。
- 幻觉：模型生成无法由检索证据支持的内容。
- 评测污染：benchmark 或答案是否出现在训练/调参数据中。
- 安全拒答：模型是否在高风险请求中给出不当操作建议。
- 版权与引用：生成内容或训练数据是否需要来源说明。

建议项目报告固定加入 “Safety and Limitations” 小节，至少列出 3 个风险、触发样例和缓解策略。

## 课堂活动建议

1. 用 10 分钟手算一个 dependency parsing transition 序列。
2. 用 15 分钟比较同一句翻译的 BLEU 与人工偏好差异。
3. 用 15 分钟把一个文本分类任务分别设计成 BERT fine-tuning 和 GPT prompting。
4. 用 20 分钟审查一个 RAG 失败案例，标出 retrieval、generation 和 evaluation 的责任边界。

## Mini-Recitation Checklist

| Topic | Board artifact | Student action |
|-------|----------------|----------------|
| Dependency parsing | stack / buffer / arcs transition table | 写出合法 action 序列并计算 UAS/LAS |
| Seq2Seq / NMT | beam table with sum and normalized score | 解释 length bias 和 length penalty |
| BERT / MLM | masked input + labels table | 区分 MLM loss positions 与 causal LM labels |
| Evaluation | metric failure-case table | 判断哪个指标支持结论、哪个指标失效 |
| Ethics / Safety | risk / trigger / mitigation table | 把 failure case 连接到数据、模型、系统或评测原因 |
