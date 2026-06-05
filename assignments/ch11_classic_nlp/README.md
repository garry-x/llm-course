# Supplemental Assignment: Classic NLP and Evaluation

本补充作业对应经典 NLP 专题 handout 和第 8 周讨论课。目标是把 RNN 长程依赖、dependency parsing transition system、seq2seq cross-attention、BERT/MLM mask、BLEU、ROUGE、Exact Match/F1 从概念题推进到可运行实现。

## Files

- `starter.py`: 学生起始代码。
- `reference_solution.py`: 参考实现。
- `tests.py`: 可运行测试。

## Run

```bash
.venv/bin/python assignments/ch11_classic_nlp/tests.py
```

默认测试 `reference_solution.py`。测试学生代码时：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch11_classic_nlp/tests.py
```

## Requirements

- `attachment_scores` 计算 UAS/LAS，必须检查 heads 与 labels 长度一致。
- `run_arc_standard_transitions` 执行 `SHIFT`、`LEFT_ARC(label)`、`RIGHT_ARC(label)` 和 `ROOT(label)`，返回 heads、labels、arcs 和 stack/buffer trace。
- `scalar_rnn_forward` 和 `recurrent_gradient_factors` 展示 tanh RNN 的状态递推与 BPTT 梯度乘积。
- `additive_attention_context` 按 `v^T tanh(W_s s_t + W_h h_i)` 计算 alignment scores、softmax weights 和 context vector。
- `sentence_bleu` 使用 clipped n-gram precision 和 brevity penalty。
- `rouge_l_f1` 使用最长公共子序列计算 precision、recall 和 F1。
- `exact_match_and_f1` 对 QA 字符串做标准化，再计算 exact match 和 token F1。
- `build_mlm_example` 根据 mask positions 生成 BERT-style masked input 和 labels。
- `select_extractive_qa_span` 根据 encoder-only QA head 的 start/end logits 选择合法答案 span，并支持 `[CLS]` no-answer。

## Written Drill Expectations

- 按 `classic-nlp-handout.md` 的 `I saw her` worked example，写出 stack / buffer / arcs transition table。
- 给定标量 RNN 参数，手算 3 步 hidden state 和 `prod_t w_hh * (1 - h_t^2)`，解释梯度消失或爆炸。
- 写出 seq2seq 的 `p(y | x)` 条件概率分解、teacher forcing loss，并解释 cross-attention 中 `alpha_{t,i}` 与 `c_t` 的含义。
- 给定一组 beam candidates，比较 sum log prob、length-normalized score 和 length penalty 后的排序。
- 给定 BERT tokens 和 mask positions，写出 masked input、labels 和 loss positions；给定 start/end logits，写出抽取式 QA 的最佳答案 span。
- 给定一个 candidate/reference，说明 BLEU clipped precision、ROUGE-L、EM/F1 分别会奖励或惩罚什么。
- 构造一个 BLEU、ROUGE、EM/F1 或 LLM-as-judge 看似高分但人工质量差的 metric failure case。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 40 | 解释 RNN 长程依赖、dependency parsing、seq2seq/cross-attention、beam search length bias、BLEU、ROUGE-L、QA EM/F1、BERT MLM mask 和 LLM 评测之间的关系 |
| Programming parts | 50 | 实现 arc-standard transition parsing、RNN recurrence、BPTT gradient factors、UAS/LAS、seq2seq additive attention、BLEU、ROUGE-L、QA EM/F1、MLM mask example 和 extractive QA span selection |
| Analysis / style | 10 | 构造至少 2 个指标高但人工质量差的例子，并说明指标局限 |
