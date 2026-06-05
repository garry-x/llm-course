# Frontier Seminar Handout: Interpretability, Multimodality, Social Impact, and Open Questions

本 handout 用于补齐 CS224N 风格课程后半段的 seminar 主题：interpretability、多模态、社会影响与开放问题。它不替代 Ch08-Ch10 的工程主线，而是要求学生把模型能力、评测证据、风险边界和前沿论文联系起来。安全、伦理与社会影响案例见 [Safety and Societal Impact Casebook](safety-societal-impact-casebook.md)。若 seminar 来自 guest lecture、工业分享或外部公开报告，活动准入、录制、替代任务、参与分和讲者材料边界按 [Guest Speaker and External Seminar Policy](guest-speaker-seminar-policy.md) 执行。

基准参照：Stanford CS224N Winter 2026 公开 schedule 包含 Benchmarking and Evaluation、Reasoning、Tokenization and Multilinguality、Interpretability、Social and Broader Impacts、Multimodality、Tinker and LoRA Without Regret、Open Questions 等后半段主题。逐项证据矩阵见 [CS224N Current Benchmark Snapshot](cs224n-current-benchmark-snapshot.md#当前-schedule-主题证据矩阵) 的“当前 Schedule 主题证据矩阵”。

来源使用规则：

- 论文和官方项目页按 [External Source Inventory](external-source-inventory.md) 分层管理；学生报告需写访问日期。
- seminar 讨论可以提出假设，但不能把未复现实验、模型演示或论文摘要写成课程事实。
- 若阅读材料是 blog/thread 或非同行评审材料，必须明确写成解释框架或研究线索。

## 使用方式

建议安排在 Week 8-10，每次 30-45 分钟，可作为 lecture 尾段讨论、discussion section 或项目报告前的专题检查。

每个 seminar 都必须产出一页短报告：

- 主题与阅读对象。
- 一个核心 claim。
- 支持 claim 的实验或证据。
- 一个不能外推的边界。
- 与本课程章节、作业或 capstone 的连接。
- 一个项目或产品场景中的风险登记。

## Seminar 0: Benchmarking, Evaluation, and Reasoning Evidence

目标：

- 区分 benchmark score、human preference、system SLO、project-specific metric 和 reasoning trace evidence。
- 说明 MMLU、HELM、AlpacaEval 或课程自建 benchmark 的数字为什么必须写明任务版本、prompt/shot 设置和污染风险。
- 把 reasoning、self-consistency、verifier、test-time compute 和 RL 结论限定在可复核实验条件内。

建议阅读：

- Srivastava et al. [Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models](https://arxiv.org/abs/2206.04615). 重点看 benchmark suite 的任务多样性和外推边界。
- Liang et al. [Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110). 重点看多维评测框架。
- Wang et al. [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171). 重点看 sampling 和 aggregation 条件。
- 本课程 [Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md)。

课堂问题：

1. 一个模型在数学题 benchmark 上更高分，能否直接说明它更适合课程项目？还缺哪些任务、成本和失败案例证据？
2. reasoning trace 是解释、训练信号、搜索中间态，还是只是一种可观察输出？项目报告应如何措辞？
3. 如果 benchmark 样本可能出现在预训练数据中，学生报告需要保留哪些不确定性说明？

最低交付：

- 选一个 benchmark 或 reasoning claim。
- 写出 metric_card、prompt/shot 条件、contamination risk 和不能外推的边界。
- 给出一个本课程两周内能运行的复核实验。

## Seminar 1: Interpretability

目标：

- 区分 attention visualization、feature attribution、mechanistic interpretability 和行为层面 error analysis。
- 解释为什么 attention heatmap 只能作为诊断线索，不能直接等价于模型解释。
- 把可解释性证据连接到项目错误分析，而不是只展示好看的图。

建议阅读：

- Geva et al. [Transformer Feed-Forward Layers Are Key-Value Memories](https://arxiv.org/abs/2012.14913). 重点看 FFN key/value 解释框架和实验边界。
- Jain and Wallace. [Attention is not Explanation](https://arxiv.org/abs/1902.10186). 重点看 attention 权重与特征重要性的关系为何需要实验证据。
- Elhage et al. [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html). 重点看 mechanistic interpretability 的假设、适用模型规模和分析边界。

课堂问题：

1. 如果某个 head 对答案 token 权重最高，是否足以说明模型“因为它”而回答？需要什么反证或干预？
2. FFN key-value memory 视角如何帮助解释 Ch05 中 FFN 的参数规模？
3. 项目报告中怎样把 interpretability 从“图示”变成可评分证据？

最低交付：

- 选一个 Ch03 attention 热力图、Ch05 FFN 例子或项目失败案例。
- 写出一个可解释性假设。
- 给出一个验证或反驳该假设的干预实验，例如 mask、patch、prompt counterfactual 或特征替换。

## Seminar 2: Multimodality

目标：

- 解释 image encoder、projection layer、LLM backbone 和 multimodal instruction tuning 的基本接口。
- 区分早期融合、后期融合、检索增强多模态和统一自回归多模态建模。
- 说明多模态评测为什么不能只看文本指标。

建议阅读：

- Liu et al. [Visual Instruction Tuning](https://arxiv.org/abs/2304.08485). 重点看 image encoder、projection 和 instruction tuning 数据构造。
- Chameleon Team. [Chameleon: Mixed-Modal Early-Fusion Foundation Models](https://arxiv.org/abs/2405.09818). 重点看 early-fusion token 化路线和 mixed-modal evaluation。
- Zhou et al. [Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model](https://arxiv.org/abs/2408.11039)，或同类统一多模态生成论文的 evaluation section。

课堂问题：

1. 图像 patch token 与文本 token 拼接后，causal mask 或 attention mask 应如何设计？
2. 多模态模型的 hallucination 与纯文本 RAG hallucination 有什么相同和不同？
3. 如果项目声称“支持图表问答”，最小评测集应包含哪些失败类型？

最低交付：

- 画出一个 multimodal LLM 的数据流：image encoder、projection、text tokens、LLM、输出。
- 列出 3 个评测维度：感知正确性、语言回答质量、安全/隐私边界。
- 给出至少 2 个失败案例，例如 OCR 错误、空间关系错误、图表数值误读或过度推断。

## Seminar 3: Social and Broader Impacts

目标：

- 把隐私、偏见、版权、评测污染、安全拒答和部署误用写成可审查的风险，而不是抽象口号。
- 区分模型本身风险、数据风险、评测风险和产品部署风险。
- 让 capstone 报告中的 data/ethics section 能被助教一致评分。

建议阅读：

- Bommasani et al. [On the Opportunities and Risks of Foundation Models](https://arxiv.org/abs/2108.07258). 重点看风险分类和治理边界。
- Bender et al. [On the Dangers of Stochastic Parrots](https://dl.acm.org/doi/10.1145/3442188.3445922). 重点看数据、规模、环境和社会风险的论证方式。
- 本课程 [Data and Ethics Review](data-ethics-review.md)。

课堂问题：

1. 一个 RAG 医疗问答 demo 的最大风险来自检索、生成、日志还是用户界面？
2. “没有收集真实用户数据”是否足以排除隐私风险？
3. 哪些 benchmark 可能被训练数据污染？你如何记录不确定性？

最低交付：

- 填写一个四行风险登记表：风险、触发样例、缓解措施、残余风险。
- 至少包含 privacy、bias 或 safety 中的两个类别。
- 明确哪些风险不能被当前项目完全解决。

## Seminar 4: Open Questions in NLP and LLM Engineering

目标：

- 训练学生把前沿主题写成可验证问题，而不是追逐名词。
- 区分基础理论问题、工程系统问题、评测问题和政策/治理问题。
- 为最终项目报告准备“未来工作”和“不能推广的结论”。

候选开放问题：

- 长上下文：模型是否真的利用远距离信息，还是只是在检索局部证据？
- Reasoning：RL、test-time compute、self-consistency 和 verifier 分别改变了什么？
- Agent：工具调用成功率、权限边界和错误恢复如何评估？
- 多模态：统一 token 空间是否带来可迁移推理，还是主要依赖数据规模？
- 训练系统：算力、数据质量和优化稳定性之间如何做可复现 trade-off？

建议阅读：

- [Stanford CS224N 当前 schedule](https://web.stanford.edu/class/cs224n/) 中的 Reasoning、Agents/RAG、Benchmarking、Multimodality 和 Open Questions 相关 suggested readings。
- 本课程 [前沿模型来源等级与复核记录](frontier-source-audit.md) 中 A/B/C/D 来源分层。
- 与个人项目最接近的一篇近一年论文，优先选择官方论文、模型卡或框架文档。

课堂问题：

1. 一个“开放问题”怎样改写成本课程 2 周内能做完的最小实验？
2. 如果实验失败，哪些证据能说明问题来自假设错误，而不是实现错误？
3. 项目报告中的 future work 应该如何避免变成无法验证的愿望清单？

最低交付：

- 把一个开放问题改写成可评测假设。
- 指定一个最小实验、一个成功指标和一个失败判据。
- 标出需要的新数据、算力、人工标注或安全审查。

## 评分 Rubric

| 维度 | 分值 | 通过标准 |
|------|:--:|----------|
| 证据质量 | 30 | claim 能追溯到论文、课程章节、实验或项目日志 |
| 边界意识 | 25 | 明确说明实验条件、不能外推处和残余风险 |
| 课程连接 | 20 | 至少连接一个章节、作业函数、capstone 模块或阅读复盘 |
| 可执行性 | 15 | 提出可运行、可复核或可人工评分的后续检查 |
| 表达清晰 | 10 | 术语准确，避免“保证”“完全解决”等绝对化表述 |

## 与课程证据的连接

| Seminar | 对应课程材料 | 可评分证据 |
|---------|--------------|------------|
| Benchmarking / Reasoning | Ch08-Ch10、[Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md) | metric card、prompt/shot 条件、contamination risk、reasoning claim boundary |
| Interpretability | Ch03、Ch05、[Chapter Source and Accuracy Map](chapter-source-map.md) | attention/FFN 诊断、反事实实验、错误分析 |
| Multimodality | Ch10、[reading-list.md](reading-list.md) Week 10 | 多模态数据流图、失败案例、评测维度 |
| Social impact | [Data and Ethics Review](data-ethics-review.md)、[课程政策](course-policies.md) | 风险登记、缓解措施、残余风险 |
| Open questions | [frontier-source-audit.md](frontier-source-audit.md)、capstone 报告 | 可评测假设、实验设计、来源等级 |

## 发布前 Checklist

- seminar 主题至少覆盖 benchmarking/evaluation、reasoning、interpretability、multimodality、social impact 和 open questions。
- 每个 seminar 都有目标、建议阅读、课堂问题和最低交付。
- 所有前沿 claim 必须标注来源等级或在报告中写明访问日期。
- 学生项目不得把 seminar 讨论当作未经验证的产品能力声明。
