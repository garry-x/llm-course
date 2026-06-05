# Academic Integrity Case Process

本流程把 [课程政策](course-policies.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Autograder 与隐藏测试设计指南](autograder-hidden-tests.md) 和 [Grading Calibration Guide](grading-calibration.md) 中的学术诚信规则转化为可执行的取证、沟通、复核和记录步骤。它适用于正式选课、Credit / No Credit、旁听参与课程平台、自学者使用公开材料、项目 mentor 和 teaching staff；身份与访问边界见 [Enrollment, Audit, and Public Use Policy](enrollment-audit-public-use-policy.md)，沟通隐私见 [Course Communication and Announcement Policy](course-communication-policy.md)。

## 适用范围

| 范围 | 覆盖对象 | 典型证据 | 处理边界 |
|------|----------|----------|----------|
| 编程作业 | `student_solution.py`、运行日志、公开测试和 hidden tests 反馈 | 提交快照、测试输出、diff、导入路径、随机种子 | 保留原始提交，不用修改后文件替代证据 |
| 书面题 | 推导、shape 说明、复杂度、引用 | PDF/Markdown、版本记录、引用清单 | starter 或课堂公式可相同，非平凡推理必须独立 |
| Capstone / final project | proposal、milestone、poster、report、代码、日志和贡献声明 | commit、实验表、artifact manifest、贡献表、mentor 记录 | 与 [Project Team and Mentor Policy](project-team-mentor-policy.md)、[Project Submission Dossier](project-submission-dossier.md) 和 [Data and Ethics Review](data-ethics-review.md) 一起判断 |
| 讨论区 / peer review | 公开讨论、私密答疑、互评反馈 | 公开帖、私密消息摘要、review 表 | 不公开学生代码、hidden tests、评分脚本或个人情况 |

## 允许 / 禁止 / 必须披露

| 类别 | 示例 | 提交要求 |
|------|------|----------|
| 允许 | 讨论概念、论文、shape、debug 假设；阅读公开文档；用 AI 工具解释报错；使用作业允许的第三方库 | 最终代码、推导和报告必须由学生审阅并能解释 |
| 必须披露 | AI 工具使用、外部协作者、同伴 pair debugging、复用旧项目、开源代码片段、模型/API/库版本 | 在 `honor_statement.txt`、报告 Contributions 或项目 disclosure 中写清使用位置 |
| 禁止 | 复制他人代码或报告、提交 `reference_solution.py` 改名版本、读取 hidden tests、硬编码公开测试输入、伪造日志、泄露 private LMS / Ed post | 进入 Manual Review Flow；必要时按学校正式 honor code 处理 |

## Signals and Triage

| signal_type | 触发信号 | 初步处理 |
|-------------|----------|----------|
| similarity cluster | 多份提交有高度相似结构、变量命名、错误路径或报告段落 | 先剔除 starter、公共模板和课堂 demo，再比较非平凡实现 |
| identical nontrivial bug | 多份提交在同一边界条件下出现相同罕见错误 | 收集最小 diff、失败输入类别和解释差异 |
| reference_solution.py access | 提交代码导入、读取或复制 `reference_solution.py` | 冻结提交、检查路径访问和构建发布包是否泄漏 |
| hidden test leakage | 代码针对 hidden tests 输入、输出、seed 或评分脚本细节做特殊分支 | 检查公开材料、讨论区和 release manifest；必要时轮换隐藏测试 |
| AI disclosure mismatch | 报告声明未使用 AI，但代码、注释或解释能力与提交不一致 | 要求学生说明实现来源、提示词类别和人工审阅证据 |
| project contribution mismatch | 团队成员贡献表、commit、日志和答辩解释明显不一致 | 按团队贡献政策要求补充个人说明或单独问答 |

信号不是裁决。similarity report、隐藏测试异常或 AI 痕迹只能启动复核，不能单独证明违规。

## Automated Checks

| check | 检查内容 | 输出 |
|-------|----------|------|
| `reference_solution.py` | 学生提交、导入链、压缩包和运行路径是否接触参考答案 | 命中文件、行号或路径摘要 |
| tests.py modification | 学生是否修改公开 `tests.py` 或把修改后测试当成评分依据 | diff 摘要与原始公开测试 hash |
| network access | 运行时是否依赖网络下载、远程 API 或隐藏环境变量 | 命令、失败摘要和允许例外说明 |
| public input hardcoding | 是否只针对公开样例、公开 seed 或公开断言返回固定答案 | 公开样例变体和 hidden tests 类别反馈 |
| module rename / shape / seed | 是否破坏 starter API、硬编码 shape、忽略随机种子或改模块名绕过测试 | API contract、shape trace 和 seed 复现记录 |
| similarity report | 与同批提交、历史提交、公开代码和报告文本的相似性摘要 | similarity cluster id、被剔除模板范围和人工复核建议 |

自动检查结果应进入 [Course Operations and Improvement Log](course-operations-log.md) 的聚合记录；学生个人信息和其他学生代码不进入公开仓库。

## Manual Review Flow

1. collect evidence：收集原始提交、日志、rubric 项、自动检查摘要和相关政策，不在公开讨论区指控学生。
2. freeze original submission：冻结原始提交、时间戳、运行环境、测试版本和 release manifest。
3. compare allowed collaboration：对照本流程、课程政策、作业 handout、AI 披露和允许协作边界，剔除 starter、公共模板和课堂 demo。
4. student_response：通过私密渠道让学生书面说明或参加短会，说明实现来源、协作对象、AI 工具使用、调试过程和无法解释之处。
5. policy_mapping：把证据映射到具体规则，例如复制答案、未披露外部代码、hidden test leakage、伪造日志或贡献不实。
6. decision：由主讲教师或学校指定流程裁决；相似性高但证据不足时，可要求补充解释、口头问答或重新提交等比例替代任务。
7. grade_action：记录成绩动作、补救要求、是否上报学校正式流程和是否需要更新测试、rubric 或公告。
8. follow_up：必要时更新 [Grading Calibration Guide](grading-calibration.md)、[Autograder 与隐藏测试设计指南](autograder-hidden-tests.md)、[Course Communication and Announcement Policy](course-communication-policy.md) 或 release 流程。

## Student Rights and Privacy

- 不在公开讨论区、公开仓库、lecture 或公告中点名学生或展示其他学生代码。
- 学生有机会查看与自己提交相关的证据摘要，并给出 student_response。
- staff 不把 similarity report 当作唯一证据；必须解释 starter、模板和公共代码为何不足以解释相似性。
- 涉及健康、便利安排、身份安全或其他个人情况时，只通过私密渠道处理，并只共享必要信息。
- 若学校有正式 honor code、申诉、听证或记录保留流程，本课程流程服从学校规则。

## AI Tools Review

| 判断点 | 可接受 | 高风险 |
|--------|--------|--------|
| 学习辅助 | 用 AI 解释公式、报错、PyTorch API 或报告措辞 | 让 AI 直接生成完整解答并提交 |
| 调试辅助 | 提供最小失败样例，让 AI 提出排查假设，学生自行验证 | 让 AI 根据公开测试输出反推固定答案 |
| 披露 | 写明工具类别、使用环节、修改范围和人工审阅 | 声明未使用 AI，但无法解释关键函数、推导或实验日志 |
| 来源 | AI 输出中的外部代码、库和论文继续按引用规则处理 | 把 AI 生成的伪引用、伪日志或不可复现结果写入报告 |

学生不能提交自己无法解释的代码、推导、实验结果或项目贡献说明。AI 工具争议按 Manual Review Flow 处理，而不是自动按零分处理。

## Similarity Report Interpretation

| 检查维度 | 解释原则 |
|----------|----------|
| starter overlap | starter、公开测试、课堂 demo 和 handout 模板应从相似性判断中剔除 |
| boilerplate | import、参数解析、日志模板和常见 PyTorch 写法通常不能单独证明违规 |
| nontrivial structure | 罕见控制流、相同 bug、相同错误注释、相同无关变量更值得复核 |
| written answers | 相同公式结论可能正常；相同文字组织、错误推导和未引用段落需要人工检查 |
| historical code | 与公开 GitHub、往年提交或 archived project 相似时，检查许可证、引用和本轮作业变更 |

similarity report 的作用是排序复核优先级；最终结论必须结合提交时间、解释能力、披露记录、项目贡献和作业允许资源。

## Project Integrity

项目材料同时检查结果是否好、来源是否清楚、贡献是否真实：

| 项目风险 | 复核证据 |
|----------|----------|
| external collaborators 未披露 | proposal、Contributions、mentor 记录、commit 和致谢 |
| shared project 边界不清 | 是否与其他课程、实验室或开源项目共享代码、数据或报告 |
| contribution mismatch | 成员贡献表、commit、日志、答辩问答和同伴 review 是否一致 |
| artifact/report mismatch | 报告指标、日志、checkpoint、API 输出和复现命令是否互相支持 |
| data or privacy violation | 数据许可证、PII、模型/API 条款和 [Data and Ethics Review](data-ethics-review.md) 是否完成 |

项目复核可能导致个人分数调整、补充口头问答、修改公开归档范围或按学校流程处理。

## Case Record Template

| field | 内容 |
|-------|------|
| case_id | 课程内部编号，不使用公开姓名 |
| assignment_or_project | 作业、书面题、capstone 或 peer review 名称 |
| signal_type | similarity cluster、hidden test leakage、AI disclosure mismatch 等 |
| evidence_summary | 原始提交、日志、测试版本、相似性摘要和关键行号 |
| student_response | 学生书面说明或会谈摘要 |
| policy_mapping | 对应课程政策、作业 handout、AI 披露或学校 honor code 条款 |
| decision | 无违规、需要补充解释、成绩动作、上报学校流程等 |
| grade_action | 无调整、重评、扣分、替代任务或学校流程结果 |
| privacy_scope | 哪些 staff 可见，是否含敏感信息，是否允许进入聚合记录 |
| follow_up | 测试、rubric、handout、FAQ 或公告需要更新的动作 |

## Staff Checklist

- 使用学生版发布包，确认不发布 `reference_solution.py`、hidden tests、评分脚本或 instructor-only 文档。
- 每次作业发布前记录公开测试 hash、release manifest、hidden tests 类别和 rubric 映射。
- 对 similarity report 先剔除 starter、公共模板、课堂 demo 和允许引用资源。
- 所有学生沟通走私密渠道，并保留 student_response 与 policy_mapping。
- 只在必要 staff 范围内共享证据，不展示其他学生代码。
- 个案结束后只把聚合改进写入 operations log，不公开个人细节。

## 发布前 Checklist

- README、syllabus、course policies 和 assignment submission guide 均链接本流程。
- CS224N crosswalk 和 current snapshot 明确 honor code、AI tools policy 与本流程的对应关系。
- `scripts/build_course_site_release.py` 把本文件列入学生安全文档。
- `.venv/bin/python verify_course.py` 通过。
- `.venv/bin/python verify_course.py --capstone --training` 在发布或期末前通过。
