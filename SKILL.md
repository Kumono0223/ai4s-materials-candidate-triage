---
name: materials-candidate-triage
description: "离线材料组成证据与初筛 Skill：解析括号、非整数计量和水合物，计算组成描述符与逐项可解释多目标排序，输出可复现 JSON。"
version: 0.2.0
---

# Materials Candidate Triage

本 Skill 是 AI4S Hackathon 的可复现科学计算模块。它不声称预测真实材料性能，只做透明的组成证据计算与目标敏感初筛，便于后续接入结构数据库、实验或高保真模拟。

```text
python -m src.materials_triage.cli --objective battery --formula Fe2O3 LiFePO4 "Na3V2(PO4)3"
```

输出必须保留 `methodology_version`、`score_breakdown`、`validation_level` 和 `limitations`；下游 Agent 不得把 `triage_score` 描述为材料性能或实验成功概率。
