# 课程政策：协作、引用与 AI 工具

本政策用于把课程作业和项目从“自学练习”提升为可评分课程交付物。教师可以按学校规则调整细节，但不应删除协作边界、引用要求、复现要求和学生支持边界。正式选课、Credit / No Credit、旁听、自学者、公开材料使用、成绩和证书边界见 [Enrollment, Audit, and Public Use Policy](enrollment-audit-public-use-policy.md)；成绩册、LMS、late-day 账本和复核状态见 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md)；可及性与学术便利安排见 [Accessibility and Student Support Guide](accessibility-student-support.md)；疑似抄袭、AI 工具争议、hidden tests 泄漏和相似性检测个案按 [Academic Integrity Case Process](academic-integrity-case-process.md) 处理。

## 协作边界

允许：

- 讨论论文、公式、调试思路、测试失败原因和工程取舍。
- 结对阅读章节或论文，并各自独立完成最终代码与书面答案。
- 在报告中引用同伴 review 的建议。

不允许：

- 复制他人的代码、推导、实验报告或 benchmark 输出。
- 把参考解答改名为学生提交。
- 共享隐藏测试、评分脚本或项目评审意见。
- 伪造训练日志、评测结果、成本估算或硬件环境。

## AI 工具使用

允许使用 AI 工具解释概念、生成调试假设、改写实验报告草稿或辅助定位错误。最终提交必须满足以下要求：

- 学生能口头解释每个提交函数的输入、输出、shape、复杂度和边界条件。
- 代码中关键实现必须由学生审阅并通过本课程测试。
- 报告中要列出 AI 工具参与的环节，例如“用于解释 RoPE 公式”或“用于定位 top-p mask bug”。
- 不得提交 AI 生成但自己无法解释的推导或代码。

AI 工具披露不完整、解释能力与提交不一致或 similarity report 命中高风险模式时，课程组按 [Academic Integrity Case Process](academic-integrity-case-process.md) 进行私密复核。

## 引用与来源

论文、博客、官方文档、模型卡、第三方库文档都需要在报告中引用。引用至少包含：

- 作者或机构。
- 标题。
- 链接。
- 访问日期。
- 使用位置，例如“用于 KV Cache 显存公式”。

前沿模型规格必须优先引用官方技术报告、模型卡或发布说明。非官方解读只能作为辅助来源，不能作为唯一证据。

## 复现要求

所有项目提交必须包含：

- 运行命令。
- Python/PyTorch/依赖版本。
- 随机种子。
- 数据来源或样本构造方法。
- 训练或压测日志。
- 失败案例与已知限制。

如果结果依赖 GPU 型号、batch size、上下文长度或量化格式，报告中必须显式写出这些条件。

## 评分复核

学生可以请求复核，但必须指出具体评分项、提交文件和认为错误的理由。复核可能提高或降低分数，因为助教会重新检查相关评分项。

复核请求、`regrade_status`、`regrade_decision_id`、late-day 调整和批量修正应按 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 留痕；若复核暴露 rubric 含糊，则同步更新 [Grading Calibration Guide](grading-calibration.md)。

## 学生支持与隐私

涉及学术便利安排、健康、家庭、身份安全或其他个人困难的问题，应通过私密消息或课程邮箱处理，不要求学生在公开讨论区披露。课程团队只在执行便利安排、评分复核或安全支持所需范围内共享必要信息。

合理便利安排可以调整访问方式，例如延长时间、替代展示形式、辅助技术或可访问格式材料；但不改变核心评分目标，例如学生仍需能解释代码、推导、实验日志、引用来源和项目贡献。
