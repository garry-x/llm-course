# Lecture Media Access Policy

本政策用于管理课程直播、录播、公开历史视频、字幕、文字稿、课堂照片、demo 录屏和学生可见媒体链接。它补充 [Course Materials Index](course-materials-index.md)、[Lecture Notes Index](lecture-notes-index.md)、[Lecture Slide Outline](lecture-slide-outline.md)、[Classroom Demo Runbook](demo-runbook.md)、[Enrollment, Audit, and Public Use Policy](enrollment-audit-public-use-policy.md)、[Course Communication and Announcement Policy](course-communication-policy.md)、[Accessibility and Student Support Guide](accessibility-student-support.md) 和 [Material Versioning and Archive Policy](material-versioning-archive-policy.md)。

参照 CS224N Winter 2026 公开页的媒体边界：当前课程 lecture videos 面向 enrolled students 发布在 Canvas/Panopto，non enrolled students 不能访问当前录播；历史公开课程视频通过 YouTube playlist 等公开入口提供。本课程采用同类原则，但不依赖特定平台。

## 媒体类型与访问边界

| 媒体 | 默认访问对象 | 发布时间 | 必备替代材料 | 禁止事项 |
|------|--------------|----------|--------------|----------|
| live stream | enrolled students 和授权 auditor | 课堂开始前 | lecture notes 或 slide outline | 不公开学生姓名、聊天记录、私密提问或临时 access link |
| current lecture recording | enrolled students | 课后 24-72 小时 | transcript 或 structured summary | 不发布到公开站点，除非完成隐私剪辑和版权审查 |
| public historical video | public learner | 每轮课程前复核 | 对应 current notes 的差异说明 | 不把旧视频当作本轮评分依据 |
| demo screencast | enrolled students 或 public learner | demo 稳定后 | runnable command、expected output、fallback | 不录入 API key、私有路径、学生提交或隐藏测试 |
| caption / transcript | 与对应视频相同或更开放 | 视频发布同时或 5 个工作日内 | 可搜索文字稿或讲义段落 | 不包含学生个人敏感信息 |
| classroom photo / board capture | enrolled students 或 staff | 课后按需 | board derivation notes | 不拍摄可识别学生、成绩、私密问题或签到信息 |

## 发布与替代材料

- 每讲至少应有一种可离线阅读的替代材料：HTML 章节、lecture notes、slide outline、board derivation notes 或 structured summary。
- 如果录播或直播内容进入评分要求，必须提供 caption / transcript 或等价文字材料；不能只靠视频出题。
- current lecture recording 默认放在 LMS、Canvas、Panopto 或学校授权平台；公开站点只链接 public historical video 或已完成审查的公开录屏。
- public historical video 可以帮助自学者，但 archived / retired 视频不得作为本轮作业、quiz、项目或评分依据。
- demo screencast 必须能对应到 [Classroom Demo Runbook](demo-runbook.md) 的命令、预期输出和 fallback。

## 隐私、版权与剪辑规则

发布前必须检查：

- 是否包含学生姓名、头像、声音、聊天、成绩、邮箱、私密问题、健康或便利安排信息。
- 是否展示 hidden tests、`reference_solution.py`、未发布 rubric、private Ed/LMS post、API key、私有数据或私有路径。
- 是否包含第三方受版权限制材料；若只允许课堂内使用，不进入公开站点。
- 是否需要剪掉课前闲聊、学生问答、breakout room、屏幕通知或浏览器个人信息。
- 是否明确区分 current、archived、retired 和 public historical video。

## 可访问性要求

| 要求 | 通过标准 |
|------|----------|
| caption / transcript | 视频用于正式评分时，字幕、文字稿或 structured summary 可访问 |
| visual alternative | 板书、图表和 demo 有文字说明或 notes 链接 |
| async access | 缺课、时区、网络或便利安排学生能用替代材料完成同等学习目标 |
| media quality | 音频可辨、代码字号可读、关键命令和输出可在文字材料中找到 |
| correction path | 视频中发现错误时，发布勘误并更新 notes 或 summary |

## 平台与链接记录

每个媒体条目至少记录：

| 字段 | 说明 |
|------|------|
| lecture_id | 例如 `L03` |
| media_type | live stream / current lecture recording / public historical video / demo screencast / transcript |
| audience | enrolled students / auditor / public learner / staff |
| platform | LMS / Canvas / Panopto / YouTube / local release / institution archive |
| current_or_archived | current / archived / retired |
| accessibility_asset | caption、transcript、summary、notes 或 board derivation |
| privacy_review | checked / needs edit / staff only |
| linked_materials | 对应章节、notes、slides、demo 或 assignment |

## Staff Checklist

| 时间 | 动作 |
|------|------|
| 开课前 | 确认 live stream、current lecture recording、public historical video 和 transcript 的访问边界 |
| 每讲前 | 在 [Course Materials Index](course-materials-index.md) 中确认 notes、slides、demo 和媒体状态 |
| 每讲后 24-72 小时 | 向 enrolled students 发布 current lecture recording 或 structured summary |
| 每周 | 抽查 caption / transcript、代码可读性、隐私剪辑和链接有效性 |
| 每轮课程结束 | 把公开视频、历史链接和 retired 媒体写入 [Material Versioning and Archive Policy](material-versioning-archive-policy.md) 或 operations log |

## 发布前 Checklist

- [Course Materials Index](course-materials-index.md) 的 Slides / Notes / Recording 规则指向本政策。
- [Enrollment, Audit, and Public Use Policy](enrollment-audit-public-use-policy.md) 明确 enrolled students、auditor 和 public learner 的访问差异。
- [Accessibility and Student Support Guide](accessibility-student-support.md) 覆盖 caption / transcript、替代任务和 async access。
- [Course Communication and Announcement Policy](course-communication-policy.md) 说明录播、勘误或访问故障如何公告。
- 学生站点由 `scripts/build_course_site_release.py` 构建，只保留 public learner 可见媒体链接。
- 运行 `.venv/bin/python verify_course.py`；正式期末发布或站点大改版前运行 `.venv/bin/python verify_course.py --capstone --training`。
