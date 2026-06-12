# LLM 推理工程师课程路线与学习成果

这份文档把课程从“学完 11 章”转换为“达到 LLM 推理工程师入门岗位能力”。它不是额外章节，而是学习、复盘和检查用的路线图。

## 目标画像

完成课程后，你应该能独立完成一个小型 LLM 推理服务的设计、实现、压测、评估和上线复盘。最低能力不是“背熟名词”，而是面对一个慢、贵、不稳定、质量波动或多模态输入成本失控的 LLM 服务时，能拆解问题、定位瓶颈并给出可验证的改进方案。

## 学习路径

| 阶段 | 章节与项目 | 主要问题 | 学习产出 |
|------|------------|----------|----------|
| 1. 模型内部结构 | Ch01-Ch06 | Token 如何进入模型，attention/FFN/MoE 如何产生 logits | 能从 shape 和参数量解释一次前向传播 |
| 2. 生成链路 | Ch08-Ch10 | Prefill、decode、采样、reasoning 和推测解码如何影响用户体验 | 能解释 TTFT、TPOT、TPS、质量、随机性、test-time compute 和 speculative gate 的 trade-off |
| 3. 显存与吞吐 | Ch03-Ch04、Ch10 | KV Cache、FlashAttention、GQA/MLA、量化、active KV tokens 和 admission control 如何降低成本 | 能手算 KV Cache 显存，设置准入阈值，并说明瓶颈在算力、带宽还是显存 |
| 4. 服务化工程 | Ch10、Capstone | 如何把模型包装成可观测、可压测、可回归的 API | 跑通 OpenAI-compatible Chat API、SSE、metrics、benchmark |
| 5. 多模态与质量评估 | Ch09-Ch11、Capstone | 如何评测文本、RAG、结构化输出、多模态任务、安全和成本 | 有固定评测集、上线方案和压测报告 |

## 能力目标

### A. 模型结构读懂

- 能解释 tokenizer、embedding、RoPE、attention、FFN、MoE、LM head 的输入输出 shape。
- 能读懂 GPTConfig 里的 `n_layer`、`n_head`、`d_model`、`vocab_size` 对参数量和显存的影响。
- 能说明 MHA、MQA、GQA、MLA 的 KV Cache 差异。

**对应内容：**Ch01-Ch06，Ch10 10.2-10.4。

### B. 推理性能分析

- 能区分 prefill 与 decode 的瓶颈：prefill 更偏计算密集，decode 更偏带宽密集。
- 能定义并测量 TTFT、TPOT、tokens/s、P50/P95/P99、错误率。
- 能解释 batch size、continuous batching、prefix cache、speculative decoding 对吞吐和延迟的影响。
- 能用 acceptance rate、speedup、draft overhead、quality regression、额外显存和 workload QPS 判断是否启用 speculative decoding。
- 能用 active KV tokens 和 admission limit 描述容量，而不是只用并发请求数。

**对应内容：**Ch08，Ch10 10.1、10.10、10.12、10.13、10.17A，Capstone `benchmark.py`、`slo_check.py` 与 speculative gate 表。

### C. 显存与成本预算

- 能估算权重显存、KV Cache 显存、激活峰值和安全余量。
- 能比较 FP16、INT8、INT4、FP8/FP4 的收益与风险。
- 能把 tokens/s、GPU 小时成本、输入/输出 token 单价转换为容量规划指标。
- 能说明长上下文下为什么 KV Cache、prefix cache hit rate 和上下文长度分布会共同决定可服务请求数。

**对应内容：**Ch04 4.9，Ch07，Ch10 10.4、10.6、10.15，Capstone `capacity_plan.py`。

### D. 推理服务实现

- 能实现或接入 OpenAI-compatible `/v1/chat/completions`。
- 能支持非流式响应和 SSE 流式响应。
- 能记录 request id、model、tokens、latency、finish reason、错误类型。
- 能把 mock engine 替换为 vLLM、SGLang、TensorRT-LLM、llama.cpp 或远程 OpenAI-compatible endpoint。

**对应内容：**Ch10 10.12-10.13，Capstone `app.py`。

### E. RAG、工具调用与输出约束

- 能解释 RAG 解决知识更新和可追溯问题，但不等于模型推理能力增强。
- 能设计检索命中文档、prompt 注入、引用返回、结构化 JSON 响应、工具 schema 和失败兜底。
- 能说明 JSON schema / constrained decoding 比“请输出 JSON”的 prompt 更可靠。

**对应内容：**Ch08 约束生成，Ch10 10.8、10.13，Capstone RAG stub、`response_format` 与 `tools`。

### F. 评测与上线

- 能维护固定评测集，覆盖事实、格式、安全、拒答、工具调用和回归问题。
- 能区分自动指标、LLM-as-judge、人审抽检、安全拒答、过度拒答和任务可用性。
- 能用压测报告和 SLO 目标回答“最大并发多少、P95 是否达标、成本是否可接受”。
- 能写上线方案：限流、超时、降级、监控、日志、告警、回滚。

**对应内容：**Ch09，Ch10 10.13，Ch11 评测专题，Capstone `evaluate.py` 与 README 上线方案。

### G. 多模态输入评估

- 能区分图像问答、OCR/文档理解、图表数值推理、视觉定位和视频理解。
- 能估算视觉 token 数对 prefill latency、KV Cache 和成本的影响。
- 能说明 VQA 高分不能推出 OCR、图表或视觉定位可靠。

**对应内容：**Ch10 10.20，Inference Capstone research question。

## 学习成果

完成以下项目后，可以认为你已经达到“初级 LLM 推理工程师”课程目标。

| 项目项 | 合格标准 | 产出 |
|--------|----------|------|
| 章节主线 | Ch01-Ch11 每章至少完成一个编程练习和全部概念练习 | 页面进度或个人笔记 |
| 结构理解 | 能画出从 prompt 到 logits 再到 token 的完整数据流 | 一页架构图或文字说明 |
| 显存预算 | 能手算 8B/70B 模型在 8K/32K/128K 上下文的 KV Cache，并估算每 1M tokens 成本 | 表格或 `capacity_plan.py` 输出 |
| 准入控制 | 能用 active KV tokens、输入/输出长度分布和安全余量给出 admission limit | 容量规划说明 |
| 服务运行 | Capstone API 能启动，`/health`、非流式、流式、`/metrics` 可用 | `curl` 输出或 `acceptance.py` |
| 压测报告 | 至少跑 3 组并发配置，输出 P50/P95/P99、TTFT/TPOT、tokens/s，并用 SLO 目标判定是否达标 | `benchmark.py` JSON + `slo_check.py` 输出 |
| 回归评测 | 固定评测集通过率可复现，覆盖 RAG 命中、JSON 格式正确性、工具调用、LLM-as-judge 和安全/过度拒答，失败样例有记录 | `evaluate.py` 输出 |
| 实验结论 | 项目有 research question、baseline、workload、ablation 和结论边界 | proposal / milestone / final report |
| 优化复盘 | 选择一个瓶颈，提出优化前后指标对比 | 简短复盘文档 |
| 引擎替换 | 至少说明如何把 `MockEngine` 替换为一个真实推理引擎 | 代码 diff 或设计说明 |

## 推荐 8 周节奏

| 周次 | 学习内容 | 工程任务 |
|------|----------|----------|
| 1 | Ch01-Ch02 | 跑通 tokenizer、embedding、RoPE，记录 shape |
| 2 | Ch03-Ch04 | 实现 attention，比较 MHA/GQA/MLA KV Cache |
| 3 | Ch05-Ch06 | 组装 GPT，完成参数量和显存估算 |
| 4 | Ch07 | 跑微型训练循环，理解优化器和混合精度 |
| 5 | Ch08 | 实现生成、采样、TTFT/TPS 分析 |
| 6 | Ch09 | 跑 SFT/LoRA/DPO/GRPO 概念练习，理解质量评测 |
| 7 | Ch10 | 完成 KV Cache、量化、RAG、speculative gate、benchmark、服务蓝图 |
| 8 | Ch11 + Capstone | 补齐结构化任务与评测指标，跑通 `acceptance.py`，完成服务、压测、评测、容量估算和上线复盘 |

## 常见误区

- 只看 tokens/s，不看 TTFT 和 P95/P99。
- 只做模型调用，不记录 tokens、latency、错误率和检索命中文档。
- 只用平均延迟评估服务，忽略排队时间和尾延迟。
- 只靠 prompt 要求 JSON，不做 schema 校验或失败重试。
- 把 RAG 当成“知识增强万能药”，不评估召回、噪声和引用质量。
- 只会启动 demo，不会解释显存、吞吐、成本和上线风险。

## 最终交付模板

```text
项目名称：
research question：
baseline：
模型/引擎：
硬件环境：
API：
是否支持 streaming：
是否支持 RAG：
是否支持多模态输入：
评测集规模：
pass rate：
压测配置：
P50/P95/P99 latency：
P95 TTFT：
P95 TPOT：
speculative decoding gate：
SLO 是否通过：
tokens/s：
显存峰值：
active KV tokens / admission limit：
LLM-as-judge / safety 指标：
主要瓶颈：
已做优化：
ablation：
结论边界：
下一步优化：
上线风险：
```
