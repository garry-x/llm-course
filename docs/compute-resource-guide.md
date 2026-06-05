# Compute Resource and Cost Guide

本指南用于管理课程中的 CPU/GPU、云额度、API 调用和成本复现实验。它补充 [课程 Syllabus](syllabus.md)、[LLM Training Engineering Capstone](../projects/training-engineering-capstone/)、[LLM Inference Engineering Capstone](../projects/inference-engineering-capstone/)、[Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md)、[Data and Ethics Review](data-ethics-review.md) 和 [Course Staff Runbook](staff-runbook.md)。

高校 LLM 课程不能只要求学生“跑大模型”，还必须说明：哪些任务 CPU 可完成，哪些任务需要 GPU，额度如何公平分配，成本如何记录，失败时如何降级，项目报告如何证明实验不是浪费算力或不可复现。

## 资源原则

- 所有必交作业必须能在 CPU 或普通笔记本上完成；GPU 只能用于加速或 capstone 扩展。
- 默认训练 capstone 使用小模型和小语料，CPU 可通过 acceptance；GPU 版本必须保留同一份 seed、config 和日志格式。
- 默认推理 capstone 使用 mock engine，CPU 可完成 API、评测、压测、SLO 和容量规划；真实引擎替换属于进阶项目。
- 云额度、实验室 GPU 或 API key 只用于课程相关实验，不能用于私人任务、商业任务或与课程无关的 benchmark。
- 学生报告必须记录资源类型、运行时长、估算成本、失败重跑次数和最终可复现命令。

## 推荐资源档位

| 档位 | 适用任务 | 资源 | 通过标准 |
|------|----------|------|----------|
| CPU baseline | Ch01-Ch11 作业、两个 capstone acceptance | 4-8 CPU cores, 8-16GB RAM | `.venv/bin/python verify_course.py` 和公开测试通过 |
| Small GPU | LoRA/SFT 小实验、训练 capstone 扩展 | 1 张 8-24GB GPU | 相同 seed 下日志、loss 曲线和 checkpoint 可复现 |
| Serving GPU | vLLM/SGLang/llama.cpp/TensorRT-LLM 替换实验 | 1 张 24-80GB GPU 或量化 CPU/GPU 混合 | 报告 TTFT、TPOT、P95/P99、tokens/s 和显存 |
| Cloud/API budget | RAG、结构化输出、工具调用或外部模型评测 | 固定额度 API key 或云 credit | 记录模型名、日期、价格假设、请求数和失败重试 |

## 每周资源预期

| 周 | 任务 | 最低资源 | 可选扩展 |
|----|------|----------|----------|
| 1-4 | BPE、Embedding、Attention、GPT/MoE 作业 | CPU | 无需 GPU |
| 5 | 训练 loop 与 checkpoint | CPU | small GPU 观察吞吐和 AMP |
| 6 | 采样与推测解码 | CPU | 小模型 GPU decode 延迟对比 |
| 7 | SFT/LoRA/DPO/GRPO | CPU baseline | small GPU 做 LoRA 微调 |
| 8 | 经典 NLP、评测、数据伦理 | CPU | API 评测需固定预算 |
| 9 | 推理工程、RAG、benchmark | CPU mock engine | serving GPU 替换真实引擎 |
| 10 | Capstone 展示与复现 | CPU acceptance | GPU/API 结果需附降级复现路径 |

## 配额与公平使用

若课程提供共享 GPU、云额度或 API key，建议采用以下规则：

| 项目 | 建议规则 |
|------|----------|
| 默认额度 | 每队固定初始额度，训练和推理项目分开记录 |
| 追加额度 | 只有在 proposal/milestone 证明实验设计、评测集和失败处理合理后批准 |
| 抢占策略 | 作业和 milestone 优先于开放探索；即将到期任务优先于长期实验 |
| 空闲释放 | 训练或服务进程超过规定 idle 时间应停止或转为 checkpoint |
| 失败重跑 | 必须记录失败原因；同一配置反复失败不得无限重跑 |
| 队伍规模 | 多人项目不得简单按人数线性消耗额度，必须说明每个成员的实验贡献 |
| 外部资源 | 使用个人云账号、公司账号或开源集群必须在报告中披露，不得影响评分公平性 |

## 成本记录模板

每次正式实验应记录：

| 字段 | 示例 |
|------|------|
| 日期 | 2026-06-04 |
| 任务 | LoRA rank sweep / serving benchmark |
| 资源 | CPU / A10 / A100 / API model name |
| 配置 | seed, batch size, context, dtype, model size |
| 运行时长 | wall-clock seconds / GPU hours |
| 估算成本 | cloud price, API price, or course credit usage |
| 产物 | log file, checkpoint, benchmark report, eval output |
| 失败次数 | failed runs and first failure reason |
| 降级路径 | CPU command or smaller config that reproduces the claim |

项目报告中的成本表不得只写“用了 GPU”；必须能让助教复核数字是否来自日志、容量规划或平台账单。

## CPU Fallback 要求

所有正式评分项都应提供 CPU fallback：

| 场景 | CPU fallback |
|------|--------------|
| 训练项目 GPU 不可用 | 使用 sample corpus、小 batch 和短 step 跑通 acceptance，再把 GPU 结果标为扩展 |
| 推理真实引擎不可用 | 使用 mock engine 跑 API、评测、benchmark、SLO 和 capacity plan |
| API 额度耗尽 | 使用固定 mock responses 或本地小模型重放评测流程 |
| 长上下文实验失败 | 缩短 context 并保留同一指标定义，说明外推边界 |
| LoRA 微调失败 | 提交小规模 sanity check、loss 曲线和失败分析，不伪造完整训练 |

## 安全与数据边界

- 不上传包含 PII、受限许可证或未获授权的数据到外部云或第三方 API。
- 使用外部 API 时，必须按 [Data and Ethics Review](data-ethics-review.md) 检查数据来源、隐私、模型卡和使用条款。
- 不把课程 API key、云凭证或私有 endpoint 写入代码、日志、报告或截图。
- 对可能产生有害内容的评测，必须记录安全边界和拒答策略；不得用共享额度做无约束红队探索。
- 若平台条款禁止某类 benchmark、数据用途或模型用途，课程要求自动降级，不得以项目需求为理由绕过。

## Staff Checklist

| 时间 | 检查项 |
|------|--------|
| 开课前 | 确认所有必交测试 CPU 可跑；记录 `.venv`、PyTorch 和 Python 版本 |
| Week 4 | 公布 capstone 可用资源、额度规则、申请方式和支持窗口 |
| Week 5 | 检查训练项目 proposal 是否有资源预算和降级路径 |
| Week 8 | 检查推理项目 proposal 是否有 SLO、容量估算和 API/GPU 成本假设 |
| Week 9 | 汇总额度使用异常、失败重跑和公平性问题 |
| Week 10 | 抽查项目报告中的成本、日志、checkpoint 和复现命令是否一致 |

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| CPU baseline | 所有必交作业和 capstone acceptance 无 GPU 可通过 |
| 配额规则 | 共享资源、云额度和 API key 有公平使用规则 |
| 成本模板 | 项目报告有可复核的资源、运行时长、成本和失败重跑记录 |
| 降级路径 | 每个 GPU/API 实验有 CPU 或小配置 fallback |
| 安全边界 | 数据、隐私、凭证和平台条款有明确约束 |
| Staff 流程 | staff runbook 或 operations log 能记录额度、事故和改进项 |
