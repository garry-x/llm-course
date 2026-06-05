# External Source Inventory

本清单记录课程当前使用的外部来源类型、稳定性、课程用途和复核要求。它补充 [External Source Verification Guide](external-source-verification.md)、[Chapter Source and Accuracy Map](chapter-source-map.md)、[Paper-to-Code Traceability Matrix](paper-to-code-traceability-matrix.md)、[Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md)、[Claim Audit Worksheet](claim-audit-worksheet.md)、[Model and Benchmark Card Guide](model-benchmark-card-guide.md)、[Dataset, Model, and Artifact Provenance Registry](dataset-model-artifact-registry.md)、[前沿模型来源等级与复核记录](frontier-source-audit.md)、[Frontier Source Evidence Cards](frontier-source-evidence-cards.md) 和 [CS224N Benchmark Crosswalk](cs224n-benchmark-crosswalk.md)。目标不是替代正文引用，而是让教师在开课前能快速知道“哪些外部来源支撑了哪些课程事实，哪些链接只是运行资源或背景阅读”。

复核日期：2026-06-05

## 来源分层规则

| 层级 | 可支撑内容 | 例子 | 复核要求 |
|------|------------|------|----------|
| A-stable | 基础理论、经典论文、教材结论 | arXiv/ACL/NeurIPS/ACM 论文、Deep Learning book | 每次大改版复核链接和引用位置 |
| A-volatile | 前沿模型规格、模型卡、官方 API/发布说明 | DeepSeek API 新闻、HuggingFace 模型卡、官方 API 文档 | 每次发布课程或引用数字前复核 |
| B-implementation | 框架能力、安装、API 行为、性能案例 | vLLM/SGLang/Triton/llama.cpp/Transformers 文档 | 涉及版本或性能时复核 |
| C-background | 教学视频、课程网页、第三方教材或博客 | CS224N 页面、Karpathy 视频、Manning 书页 | 可作学习资源，不单独支撑考试事实 |
| Runtime asset | CDN、本地 API、badge、示例数据 | KaTeX CDN、shields.io、127.0.0.1、tinyshakespeare raw URL | 不作为课程事实；检查是否影响运行或展示 |

## 基础论文与教材

| 来源组 | 课程用途 | 代表链接 | 层级 | 复核频率 | 边界 |
|--------|----------|----------|------|----------|------|
| Transformer / attention | Ch03-Ch06 attention、mask、MHA、position encoding | `https://arxiv.org/abs/1706.03762` | A-stable | 大改版 | 不支撑具体厂商模型性能 |
| Tokenization / word vectors | Ch01-Ch02 BPE、word2vec、GloVe、类比现象 | `https://arxiv.org/abs/1508.07909`, `https://arxiv.org/abs/1301.3781`, `https://nlp.stanford.edu/pubs/glove.pdf` | A-stable | 大改版 | 类比现象是经验结构，不是训练目标保证 |
| Optimization / training | Ch07 Adam/AdamW、Chinchilla、ZeRO | `https://arxiv.org/abs/1412.6980`, `https://arxiv.org/abs/1711.05101`, `https://arxiv.org/abs/2203.15556`, `https://arxiv.org/abs/1910.02054` | A-stable | 大改版 | scaling law 不直接外推到课程小模型 |
| Generation / decoding | Ch08 top-p、speculative decoding、attention sink | `https://arxiv.org/abs/1904.09751`, `https://arxiv.org/abs/2211.17192`, `https://arxiv.org/abs/2309.17453` | A-stable | 大改版 | 采样质量和加速比依赖模型与 workload |
| Alignment / fine-tuning | Ch09 InstructGPT、LoRA、DPO、QLoRA | `https://arxiv.org/abs/2203.02155`, `https://arxiv.org/abs/2106.09685`, `https://arxiv.org/abs/2305.18290`, `https://arxiv.org/abs/2305.14314` | A-stable | 大改版 | 不支撑“完整安全对齐已解决” |
| Classic NLP / evaluation | Ch11 dependency parsing、seq2seq、BERT、BLEU、ROUGE | `https://aclanthology.org/D14-1082/`, `https://arxiv.org/abs/1409.3215`, `https://arxiv.org/abs/1810.04805`, `https://aclanthology.org/P02-1040/` | A-stable | 大改版 | 自动指标不能单独证明开放式 LLM 质量 |
| Interpretability seminar | Ch03/Ch05 可解释性讨论、attention heatmap 边界、FFN key-value 视角 | `https://arxiv.org/abs/2012.14913`, `https://arxiv.org/abs/1902.10186`, `https://transformer-circuits.pub/2021/framework/index.html` | A-stable | 大改版 | mechanistic interpretability 框架不能自动外推到所有大模型或产品解释 |
| Multimodality seminar | Ch10 多模态专题、image encoder/projection、early fusion、统一多模态生成 | `https://arxiv.org/abs/2304.08485`, `https://arxiv.org/abs/2405.09818`, `https://arxiv.org/abs/2408.11039` | A-stable | 大改版 | benchmark 和演示能力依赖数据、模型规模和评测设置 |
| Social impact seminar | 数据/伦理、风险登记、社会影响与治理讨论 | `https://arxiv.org/abs/2108.07258`, `https://dl.acm.org/doi/10.1145/3442188.3445922` | A-stable | 大改版 | 风险框架不替代本校政策或项目级人工审查 |

## 前沿模型与厂商来源

| 来源组 | 课程用途 | 代表链接 | 层级 | 复核频率 | 边界 |
|--------|----------|----------|------|----------|------|
| DeepSeek-V2/V3 technical reports | MLA、MoE、MTP、FP8、DualPipe、参数/激活参数 | `https://arxiv.org/abs/2405.04434`, `https://arxiv.org/abs/2412.19437` | A-volatile | 每次引用前沿数字前 | 正文必须写成报告值；性能数字不外推 |
| DeepSeek-R1 | GRPO/RL 推理能力案例 | `https://arxiv.org/abs/2501.12948`, `https://www.nature.com/articles/s41586-025-09422-z` | A-volatile | 每次课程发布前 | 不把 GRPO 写成完整安全对齐方案 |
| DeepSeek API / V3.2 | DSA、长上下文效率案例 | `https://api-docs.deepseek.com/news/news250929` | A-volatile | 每次课程发布前 | API 新闻可支撑“发布说明”，不能替代独立 benchmark |
| DeepSeek-V4 model card | CSA+HCA、mHC、Muon、OPD、reasoning modes、context | `https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro` | A-volatile | 每次课程发布前 | 模型卡数字必须标注日期；D 级 monitor-only 项不能进入作业事实 |
| OpenAI/GPT-2 historical source | GPT-2 架构与报告 | `https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf`, `https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf` | A-stable | 大改版 | GPT-2 细节不代表现代 chat API 行为 |

## 框架与工程文档

| 来源组 | 课程用途 | 代表链接 | 层级 | 复核频率 | 边界 |
|--------|----------|----------|------|----------|------|
| vLLM / PagedAttention | Ch10 serving、KV cache、paged attention | `https://arxiv.org/abs/2309.06180` | B-implementation | 涉及性能或 API 时 | benchmark 只在给定模型、硬件、workload 下成立 |
| Triton | Ch10 kernel 学习路径 | `https://triton-lang.org/main/getting-started/tutorials/01-vector-add.html`, `https://dl.acm.org/doi/10.1145/3315508.3329973` | B-implementation | 每次课程发布前 | 版本变化可能影响 API |
| OpenAI tiktoken / nanoGPT | Ch01/Ch06 代码阅读资源 | `https://github.com/openai/tiktoken`, `https://github.com/karpathy/nanoGPT` | B-implementation | 大改版 | 代码库实现不是课程作业 reference |
| tinyshakespeare raw URL | Ch07 教学下载示例 | `https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt` | Runtime asset | 发布前 | 不能作为必需联网依赖；capstone sample corpus 才是验收数据 |
| KaTeX CDN | HTML 公式渲染 | `https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css` | Runtime asset | 发布前 | 影响展示，不支撑课程事实 |

## 课程与学习资源

| 来源组 | 课程用途 | 代表链接 | 层级 | 复核频率 | 边界 |
|--------|----------|----------|------|----------|------|
| Stanford CS224N | 高校课程结构对标 | `https://web.stanford.edu/class/cs224n/` | C-background | 每轮开课前 | 只作结构 benchmark，不复制作业或政策 |
| Annotated Transformer | attention/Transformer 教学辅助 | `http://nlp.seas.harvard.edu/annotated-transformer/` | C-background | 大改版 | 教学解释不能替代原论文 |
| Karpathy videos / Zero to Hero | 代码学习路径 | `https://www.youtube.com/watch?v=kCc8FmEb1nY`, playlist URL | C-background | 大改版 | 不作为评分事实 |
| External books/courses | 课外学习资源 | `https://www.manning.com/books/build-a-large-language-model-from-scratch`, `https://github.com/NJUDeepEngine/llm-course-lecture`, `https://www.deeplearningbook.org/` | C-background | 大改版 | 与本课程版本和作业要求可能不同 |

## 非来源外链

| 链接类型 | 例子 | 处理 |
|----------|------|------|
| README badge | `https://img.shields.io/...` | 只影响展示；不进入来源等级 |
| 本地服务 URL | `http://127.0.0.1:8000` | capstone 运行示例；不做外部链接复核 |
| Git clone 示例 | `https://github.com/garry-x/llm-learner.git` | 仓库使用说明；不支撑课程事实 |
| CDN asset | KaTeX CSS/JS | 若离线授课，应准备本地替代 |

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| 高风险数字 | 参数量、context、GPU hours、FLOPs、KV cache、latency、tokens/s 均能映射到 A-volatile 来源或被降级 |
| 框架行为 | vLLM/SGLang/Triton/llama.cpp 等 API 或性能说法标注为版本/配置相关 |
| 学习资源 | 视频、书页、课程网页不作为唯一事实依据 |
| 运行资源 | CDN、badge、本地 URL 与课程事实来源分开 |
| 更新记录 | 来源变更同步到 source map、frontier audit 或 operations log |
