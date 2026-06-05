# Classic NLP Deep-Dive Teaching Module

本模块用于把 [经典 NLP 专题 Handout](classic-nlp-handout.md) 从讨论课材料扩展为可独立授课的 2-4 讲专题。它补充 [经典 NLP 与评测覆盖说明](nlp-evaluation-coverage.md)、[10 周 / 20 讲 Lecture Plan](lecture-plan.md)、Lecture Slide Outline、Board Derivation and Instructor Notes Pack、[书面推导与概念题题库](written-problem-set.md)、Instructor Solution Guide 和 `assignments/ch11_classic_nlp/`。

目标不是把课程改成传统 NLP 全覆盖课，而是确保学生能解释 CS224N 风格神经 NLP 主线中三类非 decoder-only 模型：structured prediction、encoder-decoder 和 encoder-only representation learning。

## Module Outcomes

完成本模块后，学生应能：

| outcome_id | 学习结果 | 可评分依据 |
|------------|----------|------------|
| CL-NLP-1 | 用 transition system 描述 dependency parsing，并计算 UAS/LAS | 手写 stack/buffer/arcs trace；Ch11 `attachment_scores` 测试 |
| CL-NLP-2 | 写出 seq2seq teacher forcing 和 beam search 的目标、搜索状态和 length bias | 书面题；beam table；metric failure case |
| CL-NLP-3 | 区分 encoder-decoder attention alignment 与 decoder-only causal self-attention | 信息流图；错误解释短答 |
| CL-NLP-4 | 构造 BERT-style MLM input、labels、loss mask 和 `[CLS]` fine-tuning 产出 | Ch11 `build_mlm_example` 测试；书面题 |
| CL-NLP-5 | 判断 BLEU/ROUGE/EM/F1 与人工评价各自能支持什么 claim | 指标反例；项目 metric_card |

最低通过标准：学生不能只背术语。每个主题都必须给出一个状态/张量/指标的可计算例子，并说明该例子不能证明什么。

## Suggested Lecture Split

| 版本 | 讲次 | 内容 | 交付 |
|------|------|------|------|
| 10 周压缩版 | L15 | Dependency parsing、seq2seq、BERT 关键差异 | Ch11 written drill + tests |
| 12 周扩展版 A | L15 | Dependency parsing and structured prediction | UAS/LAS drill |
| 12 周扩展版 B | L16 | Seq2Seq/NMT, attention alignment, beam search | beam search / BLEU drill |
| 12 周扩展版 C | L17 | BERT/encoder-only and representation fine-tuning | MLM label mask drill |
| 12 周扩展版 D | L18 | Evaluation failure cases and ethics | metric_card + failure taxonomy |

如果课时有限，依然应保留 dependency parsing、seq2seq、BERT 三者与 decoder-only LM 的对比表；否则学生容易把所有 NLP 任务都误解为 prompt-based generation。

## Dependency Parsing Deep Dive

### Formal Setup

给定句子 token 序列 `x_1, ..., x_n`，dependency parser 预测每个 token 的 head `h_i` 和 label `l_i`。一个合法 dependency tree 通常要求：

- 每个非 root token 恰有一个 head。
- 存在一个 root。
- 依存边不形成有向环。
- 项目化 parsing 还要求边不交叉；不是所有语言现象都满足严格项目化。

UAS 与 LAS：

```text
UAS = count(pred_head_i == gold_head_i) / n
LAS = count(pred_head_i == gold_head_i and pred_label_i == gold_label_i) / n
```

课堂边界：UAS/LAS 衡量句法边是否对齐，不衡量语义充分性、事实性或生成质量。

### Arc-Standard Oracle Example

句子：`I saw her yesterday`

Gold arcs:

- `saw -> I (nsubj)`
- `saw -> her (obj)`
- `saw -> yesterday (advmod)`
- `ROOT -> saw (root)`

| step | stack | buffer | action | arc added | oracle reason |
|------|-------|--------|--------|-----------|---------------|
| 0 | `[]` | `[I, saw, her, yesterday]` | `SHIFT` | - | 需要把 dependent 和 head 放入 stack |
| 1 | `[I]` | `[saw, her, yesterday]` | `SHIFT` | - | `saw` 是 `I` 的 head |
| 2 | `[I, saw]` | `[her, yesterday]` | `LEFT-ARC(nsubj)` | `saw -> I` | 次顶 `I` 的 gold head 是栈顶 `saw` |
| 3 | `[saw]` | `[her, yesterday]` | `SHIFT` | - | 读取 object |
| 4 | `[saw, her]` | `[yesterday]` | `RIGHT-ARC(obj)` | `saw -> her` | 栈顶 `her` 的 gold head 是次顶 `saw` |
| 5 | `[saw]` | `[yesterday]` | `SHIFT` | - | 读取 adverbial |
| 6 | `[saw, yesterday]` | `[]` | `RIGHT-ARC(advmod)` | `saw -> yesterday` | 栈顶 dependent 已无未处理 child |
| 7 | `[saw]` | `[]` | `ROOT` | `ROOT -> saw` | root token 留在 stack |

### Neural Parser Feature Template

经典神经 dependency parser 常把 parser state 转成固定长度特征：

| source | example feature | intuition |
|--------|-----------------|-----------|
| stack top | `s_0`, `s_1`, `s_2` words/POS/labels | 当前局部结构 |
| buffer front | `b_0`, `b_1`, `b_2` words/POS | 可移入词 |
| left/right children | leftmost/rightmost child of `s_0`, `s_1` | 已建局部子树 |

模型输出是下一步 action 分布：

```text
p(a_t | state_t) = softmax(W h(state_t) + b)
```

误区边界：

- action classifier 的局部准确率不等于最终 tree 合法性。
- greedy parsing 快但会累积错误；beam 或 dynamic oracle 可缓解但增加复杂度。
- attention heatmap 不能自动替代 dependency tree。

## Seq2Seq / NMT Deep Dive

### Encoder-Decoder Factorization

给定源句 `x` 和目标句 `y`：

```text
p(y | x) = prod_t p(y_t | y_<t, x)
```

训练时 teacher forcing 使用 gold prefix：

```text
L = - sum_t log p(y_t^gold | y_<t^gold, x)
```

推理时模型只能使用自己已生成的 prefix：

```text
y_t ~ p(y_t | y_<t^model, x)
```

这就是 exposure bias 的基本来源：训练条件分布和推理条件分布不完全一致。

### Attention Alignment

decoder 第 `t` 步：

```text
e_{t,i} = score(s_t, h_i)
alpha_{t,i} = softmax_i(e_{t,i})
c_t = sum_i alpha_{t,i} h_i
p(y_t | y_<t, x) = softmax(W [s_t; c_t] + b)
```

其中 `h_i` 是 source encoder state，`s_t` 是 decoder state，`alpha_t` 可作为 alignment 诊断。

边界：

- attention alignment 可帮助定位翻译漏译、重译或错译。
- attention 权重不是严格因果解释，也不是人工 word alignment 的替代品。
- decoder-only causal attention 的 K/V 都来自同一前缀；encoder-decoder cross-attention 的 K/V 来自 source。

### Beam Search Algorithm

```text
beam = [([BOS], score=0)]
for t in 1..T:
    candidates = []
    for prefix, score in beam:
        for token in top_k(p(token | prefix, x)):
            candidates.append((prefix + [token], score + log p(token)))
    beam = top_B(candidates by score + length_penalty)
return best finished hypothesis
```

Length penalty 示例：

```text
score_norm(y) = log p(y | x) / ((5 + len(y))^alpha / (5 + 1)^alpha)
```

课堂检查：

- beam search 是 decoding/search，不是训练目标。
- beam size 增大不保证语义质量提升；可能降低多样性。
- BLEU 系统级有用，但单句和开放式生成风险很高。

## Encoder-only / BERT Deep Dive

### MLM Objective

BERT-style MLM 先采样 mask positions `M`，再只在这些位置计算 loss：

```text
L_MLM = - sum_{i in M} log p(x_i | x_{\not M})
```

输入示例：

```text
original: [CLS] the cat sat on mat [SEP]
masked:   [CLS] the [MASK] sat on [MASK] [SEP]
labels:   -100  -100 cat   -100 -100 mat    -100
```

`-100` 表示 ignore index；不是未 mask token 的真实分类目标。

### Encoder Fine-tuning Patterns

| task | representation | head | typical loss |
|------|----------------|------|--------------|
| sentence classification | `[CLS]` final hidden state | linear classifier | cross entropy |
| token classification | each token hidden state | per-token classifier | masked CE |
| extractive QA | token hidden states | start/end classifiers | two CE losses |
| retrieval / embedding | pooled representation | contrastive head | contrastive / triplet loss |

与 decoder-only 的关键区别：

| dimension | encoder-only | encoder-decoder | decoder-only |
|-----------|--------------|-----------------|--------------|
| attention visibility | bidirectional | source bidirectional + target causal | causal |
| main objective | MLM / supervised discriminative | conditional generation | next-token prediction |
| best-fit tasks | classification, tagging, extraction | translation, summarization with source conditioning | generation, dialogue, code, tool use |
| generation ability | not native | native conditional generation | native autoregressive generation |

误区边界：

- BERT 不是默认的自回归生成器。
- MLM loss 不等同于 perplexity in causal LM。
- `[CLS]` embedding 不是天然“句子语义真值”；它依赖预训练和 fine-tuning。

## Assessment Pack

### In-Class Checks

| check_id | prompt | expected learning output |
|----------|--------|-------------------|
| DP-1 | 给定 4-token sentence 和 gold arcs，写出合法 transition sequence | stack/buffer/arcs 表，action 合法 |
| DP-2 | 给定 pred/gold heads 和 labels，计算 UAS/LAS | 分母、head match、label match 正确 |
| S2S-1 | 画 encoder-decoder attention 信息流 | source encoder states、decoder state、cross-attention context |
| S2S-2 | 给定 beam candidates，比较 raw score 与 length-normalized score | 能解释短句偏置 |
| BERT-1 | 给定 mask positions，写 masked input 与 labels | only mask positions have labels |
| BERT-2 | 为分类、抽取、生成各选模型族 | 能说明 encoder-only/encoder-decoder/decoder-only 边界 |

### Written Problem Templates

1. Dependency parsing：给出 sentence、gold arcs 和 transition system，要求学生写 action trace 并说明一个非法 action。
2. Seq2Seq/NMT：给出 source/target 和 decoder step，要求学生写 `p(y_t | y_<t, x)` 的依赖项、attention context 和 exposure bias。
3. Beam search：给出候选 log probabilities，要求比较 unnormalized、length-normalized 和 length penalty 后的排名。
4. BERT/MLM：给出 tokens 与 mask positions，要求写 masked input、labels、loss mask，并和 causal LM labels 对比。
5. Evaluation：给出一个高 BLEU/低人工质量或低 BLEU/高人工质量例子，要求判断 claim strength。

### Programming Learning output

本模块的最低可运行产出由 `assignments/ch11_classic_nlp/` 提供：

| function | concept learning output |
|----------|------------------|
| `attachment_scores` | UAS/LAS head 与 label 对齐 |
| `sentence_bleu` | clipped precision 与 brevity penalty |
| `rouge_l_f1` | LCS-based precision/recall/F1 |
| `exact_match_and_f1` | QA normalization 与 token overlap |
| `build_mlm_example` | MLM mask positions、labels 和 ignore index |

可选扩展：让学生实现一个小 beam search 函数，输入 step-level log probability table，输出 top beam 和 length-normalized score。若加入扩展，hidden tests 应覆盖 EOS、empty beam、tie-breaking 和 length penalty。

## Teaching Misconception Register

| misconception | correction | learning output to request |
|---------------|------------|---------------------|
| “dependency parsing 只是 attention heatmap” | parsing 输出离散 tree，attention 是连续权重诊断 | 给出 heads/labels 并计算 UAS/LAS |
| “beam search 找到全局最优翻译” | beam 是近似搜索，受 beam size、length penalty 和 model score 影响 | 比较 beam size 1/2/4 的候选 |
| “BLEU 高就说明翻译语义正确” | BLEU 看 n-gram overlap，不能保证事实和语义 | 构造词面重合但语义错误样例 |
| “BERT 和 GPT 只是 mask 不同” | objective、attention visibility、输出用途和 fine-tuning head 都不同 | 写出 MLM labels 与 causal labels |
| “encoder-only 不能用于现代 LLM 项目” | classification、reranking、retrieval embedding、span extraction 仍常用 | 设计一个 RAG reranker 或 classifier |

## Topic Boundary

本模块内容属于稳定神经 NLP 基础。若后续课程加入新的 encoder-only 模型、NMT benchmark 或 parser 论文，不应替换本模块的基础定义；应作为 extension reading 加入 [reading-list.md](reading-list.md)，并明确新论文的任务设置和适用范围。
