# Materials Candidate Triage — AI for Materials

## Artifact

一个可独立运行的 Agent Skill/科学计算模块：解析括号、非整数计量和水合物，计算摩尔质量、原子/质量分数、组成熵、过渡金属/氧/供应风险描述符，并按三个可替换目标输出逐项透明的初筛分数。

## 可复现性

- 纯 Python 标准库，无网络调用。
- 相同公式、目标与方法版本得到相同计算结果。
- 单元测试覆盖括号、非整数计量、水合物、原子/质量守恒、目标敏感性、供应风险/安全标志、未知元素和括号错误拒绝。
- 每个候选输出完整 `score_breakdown`、方法版本、原子量来源、验证级别和三条限制声明。
- 输出明确声明：启发式初筛不是性能预测，候选需用公开数据、模拟或实验验证。

## 示例

```text
python scripts/triage.py --objective battery --formula Fe2O3 LiFePO4 "Na3V2(PO4)3"
```

Web Demo 与 Python 模块共同使用 `2026.08-composition-v2` 方法口径，支持在 `battery`、`catalysis` 和 `low-supply-risk` 目标间切换，并可下载完整 JSON 证据。

## 后续科学验证

接入公开授权材料数据库，使用留出集比较初筛排序与目标属性；记录数据版本、许可、特征定义、误差、失败样本和目标敏感性。当前版本不以合成启发式分数冒充模型精度，也不推断晶体结构、氧化态或可合成性。
