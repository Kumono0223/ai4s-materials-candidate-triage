# Materials Candidate Triage

一个无网络、无模型依赖的材料化学式初筛 Skill。输入候选化学式，输出规范化公式、摩尔质量、元素质量分数、解释性标签和可复现排序分数。

## 为什么适合 AI4S

- 可独立运行、可被 SDK/Agent 调用。
- 全部计算口径在代码中显式定义，任何人可复现。
- 不把启发式分数包装成实验事实；结果只用于候选初筛，下一步应接入公开数据库或实验验证。

## 运行与验证

```powershell
python -m unittest discover -s tests -v
python -m src.materials_triage.cli --formula Fe2O3 Al2O3 LiFePO4
```

无需后端的交互式演示位于 `web/index.html`，可直接在浏览器打开；它与 Python 模块使用同一套透明评分规则，并明确展示适用边界。

## 输出字段

`formula`、`molar_mass_g_mol`、`mass_fractions`、`tags`、`triage_score`、`limitations`。
