# LLM Capstone Project Template

Copy this directory before starting a course project. It is a learner-owned workspace: replace every `[REPLACE: ...]` field with project evidence, do not put credentials or private source text in the repository, and keep raw sensitive data outside version control.

```bash
cp -R capstone-template my-capstone
cd my-capstone

mv data_manifest.template.jsonl data_manifest.jsonl
mv eval/cases.template.jsonl eval/cases.jsonl
mv safety/drills.template.jsonl safety/drills.jsonl
mv runs/baseline.template.json runs/baseline.json
mv runs/variant.template.json runs/variant.json
mv reports/decision-report.template.md reports/decision.md

# Replace all [REPLACE: ...] fields, then validate the evidence package.
python3 scripts/validate_capstone_evidence.py --project .
```

The validator checks that the project has a contract, versioned data/interface records, a frozen evaluation set, safety drills, one baseline and one variant run record, and a release decision. It deliberately does not judge whether a metric value is good enough for every product; that threshold belongs in `project_contract.md` and `reports/decision.md`.

See the [End-to-End LLM Capstone Guide](../docs/capstone-project-guide.html) for scope choices, milestone criteria, evidence definitions, and the grading rubric. The Chinese guide is at [docs/capstone-project-guide.zh.html](../docs/capstone-project-guide.zh.html).

## 中文说明

将本目录复制为自己的项目目录后，按上面的命令重命名模板文件，并替换所有 `[REPLACE: ...]` 字段。校验器要求项目至少具备：项目契约、数据与接口版本记录、冻结评估集、安全演练、基线和变体运行记录，以及明确的发布/回滚结论。

校验器不会替代工程判断：何种质量、安全、延迟或成本指标可接受，必须在 `project_contract.md` 和 `reports/decision.md` 中根据任务写清。请不要把密钥、个人数据或受限原文放入项目仓库。
