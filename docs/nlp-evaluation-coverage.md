# 经典 NLP 与评测覆盖说明

本课程主线是 LLM 构建与工程化，不是传统 NLP 全覆盖课程。为了接近 Stanford CS224N 这类高校课程的覆盖宽度，授课时需要明确哪些主题已覆盖、哪些主题作为专题或项目阅读补齐。专题讲义见 [经典 NLP 专题 Handout](classic-nlp-handout.md)，可独立拆成 2-4 讲的扩展授课材料见 [Classic NLP Deep-Dive Teaching Module](classic-nlp-deep-dive-module.md)，书面题见 [书面推导与概念题题库](written-problem-set.md)，可运行补充作业见 `assignments/ch11_classic_nlp/`。项目和扩展实验中的统计不确定性、split、contamination 和 claim 强度按 [Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md) 复核。

## 已覆盖主线

| 主题 | 课程位置 | 证据 |
|------|----------|------|
| Tokenization / BPE | Ch01 | BPE 作业与测试 |
| Word/Token Embedding | Ch02 | TokenEmbedding、Sinusoidal、RoPE 作业 |
| Attention | Ch03-Ch04 | scaled dot-product、causal mask、MHA/GQA/MLA |
| Transformer Decoder | Ch05-Ch06 | norm、FFN、GPT-2 style model |
| Language Model Training | Ch07 | next-token dataset、CE、AdamW、scheduler、训练 capstone |
| Generation | Ch08 | greedy、temperature、top-k、top-p、speculative decoding |
| Fine-tuning / Alignment | Ch09 | SFT、LoRA、DPO、GRPO |
| RAG / Serving / Inference | Ch10 | KV Cache、quantization、RAG、benchmark、SLO |

## 需要专题补齐的 CS224N 风格内容

| 主题 | 最低授课要求 | 推荐交付 |
|------|--------------|----------|
| Dependency Parsing | 解释 transition-based parsing、UAS/LAS 指标、arc-standard 操作、neural parser feature template 和合法 tree 边界 | 书面题：给定句子执行 shift/reduce；补充作业：实现 UAS/LAS；deep-dive 模块：oracle trace |
| Seq2Seq / NMT | encoder-decoder、teacher forcing、exposure bias、attention alignment、BLEU、beam search 和 length penalty | 小作业：实现 beam search 并分析长度惩罚；deep-dive 模块：cross-attention equation |
| Encoder-only / BERT | masked language modeling、loss mask、CLS pooling、fine-tuning 分类/抽取/检索和 causal LM 对比 | 补充作业：构造 BERT-style MLM masked input 和 labels；deep-dive 模块：MLM labels 与 fine-tuning patterns |
| Evaluation | intrinsic/extrinsic、accuracy/F1/BLEU/ROUGE/perplexity、LLM judge 风险、bootstrap confidence interval、seed sensitivity、significance claim gate | 补充作业：实现 BLEU、ROUGE-L、QA EM/F1；项目报告：至少一个自动指标、一个人工错误分析、split_card、metric_card 和 uncertainty_record |
| Ethics / Safety | 数据偏见、隐私、幻觉、安全拒答、评测污染 | 书面题：列出 failure modes 与缓解方案 |

## 项目评测最低要求

每个项目报告至少包含：

- 固定评测集或固定 prompt 集。
- 至少一个质量指标。
- 至少一个效率指标。
- 至少三个失败案例。
- 至少一个不确定性说明：bootstrap CI、seed sensitivity、paired comparison、load-test variance 或 single_seed_limit。
- 一个 contamination/leakage gate 记录，说明 train/test duplicate、prompt leakage、retrieval contamination 或 benchmark contamination 如何处理。
- 对失败案例的分类，例如事实错误、格式错误、检索失败、过度拒答、延迟超标。

推理工程项目必须报告 `TTFT`、`TPOT`、`tokens/s`、错误率和 P95 latency。训练工程项目必须报告 `train_loss`、`val_loss`、`perplexity`、`grad_norm`、`tokens/s` 和 checkpoint resume 证据。

## 推荐阅读

- Jurafsky and Martin, Speech and Language Processing.
- Vaswani et al., Attention Is All You Need.
- Devlin et al., BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.
- Sutskever et al., Sequence to Sequence Learning with Neural Networks.
- Chen and Manning, A Fast and Accurate Dependency Parser using Neural Networks.
- Papineni et al., BLEU: a Method for Automatic Evaluation of Machine Translation.
