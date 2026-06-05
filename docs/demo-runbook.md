# Classroom Demo Runbook

本 runbook 把 20 讲中的课堂 demo 组织成可复现的运行清单。它补充 [10 周 / 20 讲 Lecture Plan](lecture-plan.md)、[Lecture Slide Outline](lecture-slide-outline.md) 和 [Course Materials Index](course-materials-index.md)。正式开课前，教师应按本文件完成一次 dry run，并把失败项写入 [Course Operations and Improvement Log](course-operations-log.md)。

## 使用规则

- 所有命令默认从仓库根目录运行。
- 使用课程虚拟环境时，把 `python` 替换为 `.venv/bin/python`。
- 课堂 demo 不应依赖私有路径、隐藏测试、参考答案或网络下载。
- 若 demo 只适合白板推导，应标为 `board work`，并给出检查点。
- 每个 demo 至少记录：命令、预期输出、常见失败、备用方案。

## Demo 环境检查

```bash
python --version
python -c "import torch; print(torch.__version__)"
.venv/bin/python verify_course.py
.venv/bin/python run_assignment_tests.py
```

预期输出：

- Python 版本满足课程要求。
- PyTorch 可 import。
- `verify_course.py` 通过。
- `run_assignment_tests.py` 报告 11 个 suite 全通过。

## 20 讲 Demo 清单

| 讲次 | Demo | 命令或形式 | 预期输出 | 常见失败 | 备用方案 |
|------|------|------------|----------|----------|----------|
| L1 | BPE merge dry run | `.venv/bin/python assignments/ch01_bpe/tests.py` | BPE helper 与 tokenizer tests 通过 | 当前目录错误；starter 未完成 | 白板手算 `low/lower/newer` 的 merge |
| L2 | RoPE 相对位置验证 | `.venv/bin/python assignments/ch02_embeddings/tests.py` | RoPE norm preservation 与 Toeplitz score tests 通过 | PyTorch 未安装；维度为奇数 | 画 2D 旋转矩阵并手算点积 |
| L3 | Scaled attention 与 causal mask | `.venv/bin/python assignments/ch03_attention/tests.py` | attention 手算、mask 和 projection tests 通过 | mask shape broadcast 错 | 用 3-token logits 手算 softmax 前后 mask |
| L4 | Causal mask failure drill | board work + Ch03 failing snippet | 学生能指出未来 token 泄露 | 学生只看 heatmap 不看 logits | 用表格标出可见/不可见位置 |
| L5 | MHA/GQA cache 比较 | `.venv/bin/python assignments/ch04_multihead/tests.py` | GQA shapes、cache ratio 和 MHA tests 通过 | head/group 数不整除 | 用参数表手算 KV head savings |
| L6 | Block grad flow | `.venv/bin/python assignments/ch05_block/tests.py` | LayerNorm gradcheck、RMSNorm、block tests 通过 | dtype 不是 double；in-place 操作 | 白板画 pre-norm 残差路径 |
| L7 | GPT 参数审计 | `.venv/bin/python assignments/ch06_gpt/tests.py` | GPT config、weight tying、parameter count tests 通过 | vocab/tie weights 口径混乱 | 手算 embedding、block、lm head 参数 |
| L8 | MoE router bias | `.venv/bin/python assignments/ch06_gpt/tests.py` | router top-k 和 bias balancing tests 通过 | top-k 归一化错误 | 画 overloaded expert 的 bias 更新方向 |
| L9 | CE / AdamW 单步 | `.venv/bin/python assignments/ch07_training/tests.py` | CE、AdamW、scheduler 和 dataloader tests 通过 | ignore index 先 gather；weight decay 口径错 | 手算一个 2-class CE 和 AdamW step |
| L10 | Training capstone acceptance | `.venv/bin/python verify_course.py --training` | sample corpus audit、plan、resume acceptance 通过 | 环境慢；输出目录权限 | 只展示 `data_audit.py` 与 `plan_training.py` 输出 |
| L11 | Sampling 策略对比 | `.venv/bin/python assignments/ch08_generation/tests.py` | top-k/top-p、generator、distinct n-gram tests 通过 | top-p nucleus 没保留阈值 token | 手算排序概率和累计概率 |
| L12 | Speculative / JSON failure | `.venv/bin/python assignments/ch08_generation/tests.py` | speculative decoding budget 和 structured concepts tests 通过 | 把分布等价和系统加速混为一谈 | 白板画 draft/target 接受流程 |
| L13 | LoRA trainable params | `.venv/bin/python assignments/ch09_alignment/tests.py` | LoRA apply/merge、SFT mask tests 通过 | prompt token 计入 loss | 手算 LoRA A/B 参数量 |
| L14 | DPO/GRPO direction | `.venv/bin/python assignments/ch09_alignment/tests.py` | DPO preference direction、GRPO whitening tests 通过 | chosen/rejected 写反 | 手算 chosen/rejected log-ratio |
| L15 | Classic NLP metrics | `.venv/bin/python assignments/ch11_classic_nlp/tests.py` | UAS/LAS、BLEU、ROUGE-L、EM/F1、MLM tests 通过 | normalization 或 label 对齐错误 | 白板算一个 dependency sentence |
| L16 | Data ethics review | board work | 完成 data/ethics checklist 草稿 | 学生只列风险不列缓解 | 使用 `docs/data-ethics-review.md` 表格现场填一行 |
| L17 | KV cache / RAG | `.venv/bin/python assignments/ch10_inference/tests.py` | KV cache memory、RAG retrieval、int8 roundtrip tests 通过 | 忘记 batch size 或 K/V 两份 | 手算 `batch*layers*seq*heads*dim*dtype*2` |
| L18 | Serving benchmark / SLO | `.venv/bin/python verify_course.py --capstone` | health、eval、benchmark、SLO、capacity acceptance 通过 | 端口占用；服务未启动 | 只运行 capstone `capacity_plan.py` |
| L19 | Capstone reproducibility rehearsal | `.venv/bin/python verify_course.py --capstone --training` | 两个 capstone acceptance 都通过 | 运行时间较长 | 分组读 acceptance 输出并标注首个失败点 |
| L20 | Final report checklist | board work | 学生能映射 outcome、证据和残余风险 | 只展示成功 demo | 用 project rubric 检查一份报告目录 |

## 失败排查模板

```text
Lecture:
Demo:
Command:
Observed failure:
First failing line:
Likely category: environment / path / shape / dtype / numerical / dependency / policy
Workaround used in class:
Post-class fix owner:
Due date:
```

## 发布前 Checklist

- 每个 demo 都能映射到 lecture plan 或 slide outline 的讲次。
- 至少 15 个 demo 有可运行命令，其余 board work 有明确检查点。
- 每个命令能在 CPU 或明确说明的硬件上运行。
- demo 不泄露 reference solution、隐藏测试或学生提交。
- dry run 结果已记录到 operations log。
