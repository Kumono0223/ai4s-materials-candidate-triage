---
name: materials-candidate-triage
description: "离线材料候选初筛 Skill：解析化学式，计算元素质量分数与可解释的候选排序指标，输出可复现 JSON。"
version: 0.1.0
---

# Materials Candidate Triage

本 Skill 是 AI4S Hackathon 的可复现科学计算模块示例。它不声称预测真实材料性能，只做透明的组成初筛，便于后续接入实验或高保真模拟。

```text
python -m src.materials_triage.cli --formula Fe2O3 Al2O3 LiFePO4
```

