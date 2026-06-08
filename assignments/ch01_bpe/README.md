# Ch01 BPE Tokenizer 作业测试

本目录把第 1 章的编程练习整理成可自动验收的作业入口。目标不是替代章节讲解，而是给学生一个类似高校课程作业的提交标准。

## 文件说明

| 文件 | 用途 |
|------|------|
| `starter.py` | 学生起始代码，包含需要实现的 TODO |
| `reference_solution.py` | 教师参考实现，用于验证测试本身 |
| `tests.py` | `unittest` 测试，覆盖 `_get_stats`、`_merge`、`train`、`encode`、`decode`、BPE merge trace、tokenizer 统计报告和分组 token 成本比较 |

## 学生运行方式

```bash
cp assignments/ch01_bpe/starter.py assignments/ch01_bpe/student_solution.py
# 编辑 student_solution.py 完成 TODO
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch01_bpe/tests.py
```

也可以直接让测试加载 `starter.py`：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch01_bpe/tests.py
```

也可以直接验证课程内置参考实现：

```bash
.venv/bin/python assignments/ch01_bpe/tests.py
```

## Conceptual Handout

Tokenizer 是 LLM 训练和推理系统的第一层工程决策。它决定同一段文本会变成多少 token，进而影响 embedding 参数量、context window 可容纳信息、训练 token budget、KV Cache 和 API 计费。这个作业要求你把 byte-level BPE 写成可运行实现，并用报告解释它的压缩收益和失败边界。

### 1. Byte-level BPE 为什么可逆

本作业从 UTF-8 bytes 开始，初始词表是 0-255 共 256 个 byte token。任意 Unicode 文本先编码成 bytes，再在 byte 序列上做 merge。只要每个新 token 的 `vocab[new_id]` 保存为两个旧 token bytes 的拼接，decode 时把 token id 映射回 bytes 并执行 UTF-8 decode，就能得到原字符串。

这个设计的好处是没有 OOV：即使训练集中没见过某个 emoji、中文词或代码符号，也能退回到 byte 序列表示。代价是未被训练语料覆盖的语言或领域文本可能被切成更多 token，推理成本更高。

### 2. BPE merge 是局部压缩启发式

BPE 每一步统计相邻 pair 频率，选择最高频 pair，替换所有非重叠出现：

```text
ids = [1, 2, 1, 2, 3]
pair = (1, 2), new_id = 99
merged = [99, 99, 3]
```

注意“非重叠”很重要。对 `[1, 1, 1]` 合并 `(1, 1)` 时，结果应是 `[new_id, 1]`，不是两个重叠 merge。一次 merge 的 token savings 可以写成：

```text
tokens_saved = before_length - after_length
```

`bpe_training_trace` 要记录每一步 pair、count、new_id、before/after length 和 token text。这个 trace 让你能解释词表为什么长成当前样子，而不是只交最终 encode 结果。

### 3. Tie-breaking 和词表大小会影响模型行为

真实 tokenizer 训练中经常有多个 pair 频率相同。不同 tie-breaking 会得到不同 merge 顺序，导致 token id、切分结果和下游模型输入不同。本课程测试会固定行为，但报告中应说明：

- `vocab_size` 越大，平均 token 数通常越少，但 embedding matrix 参数量是 `vocab_size * d_model`。
- 过小词表会让常见词被拆成许多 token，增加 context 和 KV Cache 压力。
- 过大词表会增加 embedding/LM head 参数，并可能把低频片段记成不稳定 token。
- 对代码、中文、emoji、医学/法律等领域文本，通用语料训练出的 merge 可能不公平或低效。

### 4. Tokenizer report 应连接到系统成本

`tokenizer_report` 不只是统计平均长度。至少要解释：

- `total_tokens` / `avg_tokens`：同一数据集会消耗多少训练 token。
- `p95_tokens`：长尾输入会不会挤占 context window 或触发截断。
- `tokens_per_character`：不同语言和领域的单位文本成本。
- `round_trip_success_rate`：encode/decode 是否保持原文本。
- `embedding_params = vocab_size * d_model`：词表选择如何改变参数量。

`tokenizer_group_report` 要比较不同 group 的 token 成本。例如英文、中文、emoji 和代码的 `tokens_per_character` 可能差异很大。若某组成本显著更高，模型训练时等量字符会消耗更多 token，推理时同样长度的用户输入也会更贵。

### 5. 报告应包含失败案例

一个合格报告至少包含两个边界案例，并解释原因：

- 未见过的新词或 emoji：能 round-trip，但 token 数可能高。
- 代码符号和空格：merge 可能把常见缩进或操作符学成 token，也可能造成格式成本偏高。
- 多语言文本：某些语言每字符 token 成本高，说明训练语料或 merge 规则存在偏置。
- 特殊 token：真实系统需要 `<bos>`、`<eos>`、`<pad>`、chat template token；本作业的最小 tokenizer 没有完整覆盖，需要在报告里说明限制。

最终结论不能只写“测试通过”。你应说明当前训练语料、词表大小和文本分组下，BPE 的压缩收益、可逆性、成本差异和不能外推到真实生产 tokenizer 的部分。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 30 | 解释 byte-level BPE 可逆性、每步 merge 的 token savings、频率合并的压缩启发式、tie-breaking 对词表的影响、词表大小与序列长度/嵌入参数量/多语言和领域文本成本的权衡 |
| Programming parts | 60 | 实现 `_get_stats`、`_merge`、`train`、`encode`、`decode`、`bpe_training_trace`、`tokenizer_report` 和 `tokenizer_group_report`，通过中英文、emoji、多字节 UTF-8 round trip、merge trace 与分组 token 成本统计 |
| Analysis / style | 10 | 报告至少 2 个 tokenizer 失败或边界案例，并比较压缩率、可逆性、特殊 token 和领域文本切分 |
