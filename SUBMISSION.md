# Materials Candidate Triage — AI for Materials

## Artifact

一个可独立运行的 Agent Skill/科学计算模块：解析材料化学式，计算摩尔质量、元素质量分数、组成标签和透明的初筛分数。

## 可复现性

- 纯 Python 标准库，无网络调用。
- 相同公式得到相同 JSON。
- 单元测试覆盖公式解析、质量守恒、标签和未知元素拒绝。
- 输出明确声明：启发式初筛不是性能预测，候选需用公开数据、模拟或实验验证。

## 示例

```text
python scripts/triage.py --formula Fe2O3 Al2O3 LiFePO4
```

## 后续科学验证

接入公开授权材料数据库，使用留出集比较初筛排序与目标属性；记录数据版本、许可、特征定义和误差。当前版本不以合成启发式分数冒充模型精度。

