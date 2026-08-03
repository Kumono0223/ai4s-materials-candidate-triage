# Materials Candidate Triage

一个无网络、无模型依赖的材料组成证据与初筛 Skill。输入候选化学式和透明目标配置，输出规范式、摩尔质量、原子/质量分数、组成描述符、逐项评分证据、供应风险关注项、安全复核标志和可复现排序。

## 为什么适合 AI4S

- 可独立运行、可被 SDK/Agent 调用。
- 支持括号/方括号、非整数化学计量和中点水合物，例如 `Ca3(PO4)2`、`LiNi0.8Mn0.1Co0.1O2`、`CuSO4·5H2O`。
- 全部计算口径、原子量表版本、关注元素集合和评分分解在代码中显式定义，任何人可复现或替换。
- 提供 `battery`、`catalysis`、`low-supply-risk` 三个组成层目标；相同候选可比较目标敏感性。
- 不把启发式分数包装成实验事实；结果只用于候选初筛，下一步应接入公开数据库或实验验证。

## 运行与验证

```powershell
python -m unittest discover -s tests -v
python -m src.materials_triage.cli --objective battery --formula Fe2O3 LiFePO4 "Na3V2(PO4)3"
```

无需后端的交互式演示位于 `web/index.html`，可直接在浏览器打开；它与 Python 模块使用同一套透明评分规则，并明确展示适用边界。

## 输出字段

关键字段包括：

- `canonical_formula`、`composition`、`molar_mass_g_mol`、`atomic_fractions`、`mass_fractions`；
- `normalised_mixing_entropy`、过渡金属/氧/供应风险关注表原子分数；
- `objective`、`triage_score`、`priority_band`、`score_breakdown`；
- `supply_watchlist_elements`、`safety_review_elements`、`validation_level`、`limitations`。

## 科学边界与数据版本

- 方法版本：`2026.08-composition-v2`。
- 内嵌原子量表为 CIAAW 标准原子量的舍入值，来源入口：<https://ciaaw.org/atomic-weights.htm>，访问日期 2026-08-03。
- 供应风险关注表是可替换的工程审查配置，不声称对所有国家、时期或应用普遍有效。
- 评分没有使用晶体结构、氧化态、相图、工艺、成本或目标属性标签，因此不得解释为性能、稳定性、毒性或可合成性预测。
