# Enrollment, Audit, and Public Use Policy

本政策用于区分正式选课学生、Credit / No Credit 学生、旁听者、自学者 / public learner、teaching staff / mentor 的材料访问、评分资格、沟通渠道和项目资源边界。它补充 [课程 Syllabus](syllabus.md)、[Course Communication and Announcement Policy](course-communication-policy.md)、[Material Versioning and Archive Policy](material-versioning-archive-policy.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Course Policies](course-policies.md)、[Project Team and Mentor Policy](project-team-mentor-policy.md)、[Compute Resource and Cost Guide](compute-resource-guide.md) 和 [Accessibility and Student Support Guide](accessibility-student-support.md)。

高校课程可以公开材料，但公开材料不等于正式注册、正式评分或学校学分。本仓库提供可复现课程内容和学生发布包；official transcript、course credit 和 certificate 只能由开课学校或正式教学机构按其注册系统授予。

## 身份与权限

| 身份 | 材料访问 | 评分资格 | 支持与资源 | 核心边界 |
|------|----------|----------|------------|----------|
| 正式选课 / enrolled for credit | current 学生材料、LMS / Gradescope 发布包、课堂与讨论区 | 有正式成绩、隐藏测试、人工复核、迟交和 regrade 流程 | Office Hours、项目 mentor、课程公告、必要时可获得 compute credits | 必须遵守提交、引用、协作、AI 工具和隐私政策 |
| Credit / No Credit | 与正式选课相同 | 按学校 Credit / No Credit 或 pass/fail 规则折算 | 与正式选课相同 | 作业提交、隐藏测试、项目贡献和学术诚信规则不降低 |
| 旁听 / auditor | 课堂、公开站点、学生可见 handout；是否进入校内平台由学校决定 | 无正式成绩、无 official transcript 记录，除非学校另有书面规则 | 可参加公开讨论；mentor、compute credits 和私密反馈不保证 | 不得索取 hidden tests、reference_solution.py、评分脚本或私人学生信息 |
| 自学者 / public learner | 公开仓库、学生站点发布包、assignment release、公开章节 | 无正式成绩、无 course credit、无 certificate | 可本地运行公开测试和验证命令；无 staff 响应承诺 | public tests passing does not imply course credit |
| Teaching staff / mentor | 按职责访问 instructor-only 材料、隐藏测试、评分校准和项目材料 | 不适用 | 负责答疑、复核、项目指导和材料维护 | 必须保护学生数据、hidden tests、reference_solution.py 和 staff-only 文档 |

## 成绩与证书边界

- 只有在学校正式注册系统中完成选课，并在 LMS / Gradescope 等平台进入本轮课程 roster 的学生，才默认具有正式评分、迟交、复核和成绩记录资格。
- public tests passing does not imply course credit。公开测试通过只能说明学生实现满足公开接口；正式评分还可能包含 hidden tests、书面推导、项目报告、同伴 review、来源审计和人工复核。
- 本仓库不颁发 official transcript、certificate、学分证明或雇主背书。任何证书、学分或成绩单都必须来自开课学校或授权教学机构。
- archived 或 retired 材料可以作为历史参考，但不得作为本轮作业、quiz、项目或评分依据；正式依据以 current syllabus、assignment release 和课程公告为准。
- Credit / No Credit、pass/fail、旁听转正式选课等规则由学校注册政策决定；课程仓库只定义材料和评分边界。

## 平台与访问控制

| 资源 | 默认开放对象 | 访问规则 |
|------|--------------|----------|
| 公开章节与学生站点 | 所有人 | 由 `scripts/build_course_site_release.py` 构建，必须剥离内嵌参考解答和教师内部链接 |
| assignment release | 所有人或正式学生 | 由 `scripts/build_assignment_release.py` 构建，只包含 `README.md`、`starter.py`、`tests.py` 和 `RELEASE_MANIFEST.json` |
| LMS / Gradescope | 正式选课学生和授权 staff | 用于正式提交、成绩、regrade、隐藏测试反馈和课程公告 |
| hidden tests 与评分脚本 | 授权 staff | 不进入公开仓库、学生站点或公开讨论区 |
| `reference_solution.py` | 授权 staff 或教师维护者 | 不进入 assignment release，不作为学生提交材料 |
| compute credits | 正式选课学生优先 | 按 [Compute Resource and Cost Guide](compute-resource-guide.md) 分配；旁听和 public learner 不保证额度 |
| project mentor | 正式项目团队优先 | 按 [Project Team and Mentor Policy](project-team-mentor-policy.md) 匹配；旁听和 public learner 不保证 mentor |
| 私密沟通渠道 | 正式学生、授权旁听和 staff | 按 [Course Communication and Announcement Policy](course-communication-policy.md) 处理隐私、便利安排、迟交和成绩争议 |

## 旁听与公开学习规则

旁听者和 public learner 可以使用公开材料进行学习、复现和非商业教学改编，但需要遵守：

- 不把公开仓库完成度、公开测试通过或本地报告称为本课程正式成绩。
- 不在公开讨论区发布完整作业答案、hidden tests、reference_solution.py、评分脚本、其他学生代码或私密反馈。
- 引用课程材料时标明仓库、章节或文档路径，并区分 current、archived 和 retired 版本。
- 使用自有算力或公开可用环境复现；不要假定课程组提供 compute credits、账号、API key 或 GPU 队列。
- 若学校允许旁听进入课堂或讨论区，旁听者仍需遵守公开讨论、隐私、引用和学术诚信规则。

## Staff Checklist

| 检查项 | 通过标准 |
|--------|----------|
| Roster | LMS / Gradescope roster 与学校注册系统一致；Credit / No Credit 状态清楚 |
| 发布包 | 学生站点由 `scripts/build_course_site_release.py` 生成，作业包由 `scripts/build_assignment_release.py` 生成 |
| 内部材料 | hidden tests、`reference_solution.py`、grading calibration 和 staff-only 文档不进入公开发布包 |
| 成绩边界 | syllabus、公告和作业 handout 明确 public tests passing does not imply course credit |
| 旁听边界 | auditor 是否可进入课堂、讨论区、LMS 或 Office Hours 有本地学校规则 |
| 资源边界 | compute credits、project mentor、私密反馈和 regrade 资格优先授予正式选课学生 |
| 版本边界 | archived / retired 材料不作为本轮评分依据 |

## 发布前 Checklist

- [Course Materials Index](course-materials-index.md) 指向 current 学生材料。
- [Material Versioning and Archive Policy](material-versioning-archive-policy.md) 标清 archived、retired 和 instructor-only 边界。
- [Assignment Submission and Release Guide](assignment-submission-guide.md) 的学生发布包不含 `reference_solution.py`。
- [Course Communication and Announcement Policy](course-communication-policy.md) 明确 LMS / Gradescope、公开讨论区、私密渠道和 Office Hours 的用途。
- [Course Policies](course-policies.md) 明确协作、引用、AI 工具和隐私要求。
- 运行 `.venv/bin/python verify_course.py`；正式期末发布或项目验收前运行 `.venv/bin/python verify_course.py --capstone --training`。
