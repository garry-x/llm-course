# Lecture Notes Index

本索引用于把 20 讲的课堂 notes、板书推导、章节正文、阅读复盘和作业证据连起来。它补充 [10 周 / 20 讲 Lecture Plan](lecture-plan.md)、[Lecture Slide Outline](lecture-slide-outline.md)、[Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md)、[Lecture Notes Review Ledger](lecture-notes-review-ledger.md)、[Lecture Note Sample Pack](lecture-note-sample-pack.md)、[Board Derivation and Instructor Notes Pack](board-derivation-pack.md)、[Classroom Demo Runbook](demo-runbook.md) 和 [Course Materials Index](course-materials-index.md)：lecture plan 说明课堂流程，slide outline 说明课件结构，lecture notes quality review 说明每讲 notes 的 notation、derivation、shape、source boundary 和 correction workflow，lecture notes review ledger 记录 L1-L20 的 review_record，lecture note sample pack 提供 L1/L3/L9/L18 的学生可见样例，board derivation pack 提供可直接板书的推导脚本，demo runbook 说明现场命令，本文件说明学生课前/课后应阅读哪份 notes、复盘哪些推导、提交什么证据。

## 使用规则

- 每讲至少对应一个章节、handout 或项目 README，不能只有 slides。
- Notes 应包含：核心符号、关键推导、shape 约定、常见误区、课堂 demo 入口、课后证据。
- Notes 样例结构见 [Lecture Note Sample Pack](lecture-note-sample-pack.md)，正式 notes 至少应达到样例中的字段完整度。
- 每讲正式 notes 应按 [Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md) 保留 review_record，至少检查 notation_checked、derivation_checked、code_binding_checked、source_boundary_checked 和 accessibility_checked。
- L1-L20 当前 review_record 见 [Lecture Notes Review Ledger](lecture-notes-review-ledger.md)；若新增 PDF slides、录屏、notebook 或外部 lecture notes，必须追加 material-specific review record。
- 若课堂临时增加板书推导，教师应在 48 小时内把符号和结论补到本索引或对应章节。
- 若某讲使用外部 lecture notes，应记录来源、访问日期和课程内使用位置，并按 [External Source Verification Guide](external-source-verification.md) 复核。
- 学生复盘时优先引用本索引列出的 notes，再引用论文或官方文档。

## Notes 发布状态

| 状态 | 含义 |
|------|------|
| ready | notes 可直接作为学生课前/课后材料 |
| needs-review | 内容可用，但教师应在开课前复核符号、版本或来源 |
| instructor-only | 只作为教师备课或板书脚本，不要求学生提交 |
| planned | 尚未发布，不能作为正式评分依据 |

## 20 讲 Lecture Notes 索引

| 讲次 | Notes / 正文 | 板书推导重点 | 复盘问题 | 证据 | 状态 |
|------|--------------|--------------|----------|------|------|
| L1 | Ch01; [math-prerequisites.md](math-prerequisites.md) | BPE merge 对长度和词表的影响；贪心 merge 的局限 | byte-level BPE 为什么通常没有 OOV？ | Ch01 BPE tests + reading recap | ready |
| L2 | Ch02 | `one_hot @ E` 等价于 embedding lookup；`R_m^T R_n = R_{n-m}` | 类比推理是不是训练目标直接保证的性质？ | Ch02 embedding/RoPE tests + written proof | ready |
| L3 | Ch03 | `Var(q^T k)=d_k`；attention score/prob/context shape | 为什么 scaling 必须在 softmax 前？ | Ch03 scaled attention tests | ready |
| L4 | Ch03; [classic-nlp-handout.md](classic-nlp-handout.md) | causal mask 广播；softmax+CE 梯度 | softmax 后 mask 为什么会破坏概率分布？ | causal mask failure analysis | ready |
| L5 | Ch04 | MHA/GQA 参数量与 KV cache 元素数 | GQA 减少的是哪些 heads？ | Ch04 MHA/GQA tests | ready |
| L6 | Ch04-Ch05 | MLA latent cache；LayerNorm/RMSNorm；Pre-Norm residual | latent cache 低维是否意味着 attention 免费？ | Ch05 block grad-flow tests | ready |
| L7 | Ch06 | 自回归分解；tied LM head 参数审计 | labels 为什么右移一位？ | Ch06 GPT forward tests | ready |
| L8 | Ch06 | top-k routing；activated parameters；load balancing | 稀疏激活为什么不自动等于负载均衡？ | MoE router tests + written audit | ready |
| L9 | Ch07 | CE 数值稳定性；AdamW decoupled decay；warmup+cosine | weight decay 和 L2 regularization 在 Adam 中有什么差别？ | Ch07 loss/optimizer tests | ready |
| L10 | Ch07; training capstone README | checkpoint/resume；tokens/s；GPU hours；曲线诊断 | loss 曲线下降但验证集变差时如何定位？ | training capstone acceptance | ready |
| L11 | Ch08 | greedy/top-k/top-p 的候选集定义；重复生成机理 | top-p 和 top-k 哪个候选数固定？ | Ch08 sampling tests | ready |
| L12 | Ch08 | speculative decoding 接受率；约束解码边界；MTP 来源等级 | 推测解码什么时候可能不加速？ | speculative decoding tests + source check | ready |
| L13 | Ch09 | SFT label mask；LoRA low-rank delta；参数冻结 | LoRA 初始输出为什么应接近 base model？ | LoRA/SFT tests | ready |
| L14 | Ch09 | DPO log-ratio；GRPO group advantage whitening | preference loss 如何避免只看 chosen 概率？ | DPO/GRPO tests + written proof | ready |
| L15 | [classic-nlp-handout.md](classic-nlp-handout.md); [nlp-evaluation-coverage.md](nlp-evaluation-coverage.md) | dependency parsing action constraints；BLEU/ROUGE/EM/F1 | 为什么 exact match 不能替代 F1？ | Ch11 classic NLP tests | ready |
| L16 | [data-ethics-review.md](data-ethics-review.md) | data license/PII/contamination/safety risk matrix | 一个项目何时必须降级或移除数据？ | data ethics review form | ready |
| L17 | Ch10 | KV cache memory；per-channel int8；RAG chunk overlap | KV cache 为什么随 batch/context 线性增长？ | Ch10 KV/RAG tests | ready |
| L18 | Ch10; inference capstone README | TTFT/TPOT/TPS；P95/P99；capacity plan | 哪些指标证明系统可上线，哪些只能证明 demo 可跑？ | inference capstone benchmark/SLO | ready |
| L19 | capstone READMEs; [project-report-rubric.md](project-report-rubric.md) | seed/log/checkpoint/report 的复现链 | 复现失败时报告应保留哪些证据？ | project draft + peer review | ready |
| L20 | [presentation-peer-review.md](presentation-peer-review.md); [course-operations-log.md](course-operations-log.md) | final claim/evidence/risk alignment | 如何区分实验结论、工程假设和前沿推测？ | final presentation + operations log | ready |

## Notes 模板

每讲正式 notes 应至少包含：

| 字段 | 要求 |
|------|------|
| Learning goals | 2-4 条可测目标，避免只写主题名 |
| Notation | 列出 batch、sequence、heads、hidden、vocab 等符号 |
| Derivation | 给出关键公式的中间步骤，不只给结论 |
| Shape checks | 标出输入/输出 shape、mask shape 和 broadcast 规则 |
| Failure modes | 至少 2 个常见错误或误解 |
| Demo link | 指向 demo runbook 或作业测试 |
| Evidence | 指向作业、书面题、阅读复盘或 capstone 交付 |
| Source boundary | 对论文结论、模型卡声明和课程解释分别标注 |
| Review record | 按 lecture notes quality review 记录 reviewer、status、affected materials 和 verification command |

## 学生复盘模板

学生每讲复盘建议控制在 300-500 字，包含：

1. 一个能用公式或 shape 复述的核心结论。
2. 一个课堂 demo 或测试失败对应的实现细节。
3. 一个来自阅读材料的证据或反例。
4. 一个仍不确定的问题，供 discussion section 或 office hours 使用。

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| 讲次覆盖 | L1-L20 均有 notes/正文入口、推导重点、复盘问题和证据 |
| 链接有效 | 所有本地链接通过 `.venv/bin/python verify_course.py` |
| 符号一致 | notes 使用的 shape 和章节/作业测试一致 |
| 来源边界 | 前沿模型、benchmark、API 或价格不写成未复核事实 |
| 可访问性 | 外部 slides/录屏若作为正式材料，应提供文字 notes 或替代材料 |
| 版本记录 | 修改 notes 后更新 Course Materials Index 或 Course Operations Log |
