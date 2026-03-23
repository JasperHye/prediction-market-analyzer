# 需求文档 (PRD): 预测市场数据查询与安全分析 Skill

## 1. 产品背景与目标
本 Skill 作为预测市场话题的常驻安全插件，为用户提供 Polymarket 和 Kalshi 平台的实时安全评估。

## 2. 核心功能描述
- **多平台支持**：支持 Polymarket 和 Kalshi。
- **参数敏感抓取**：
    - **Polymarket**: 使用 `slug` 参数。
    - **Kalshi**: 使用 `eventTicker` 参数（严格分大小写）。
- **后端代理模式**：针对 API 的 CORS 限制，所有物理请求由核心服务/脚本发起，模拟后端代理。
- **深度数据解析**：
    - 遍历返回 JSON 中的 `tags` 数组。
    - 匹配 `name` 为相关检查项（如 `liquidity`）的对象。
    - 提取并汇报其 `riskLevel` 及说明。

## 3. 技术规范
### 3.1 外部 API 及其参数
- **Polymarket**: `https://test-secwarex-api.ansuzsecurity.com/api/v1/plugin/polymarket/risk?slug={slug}`
- **Kalshi**: `https://test-secwarex-api.ansuzsecurity.com/api/v1/plugin/kalshi/risk?eventTicker={slug}`

### 3.2 提取逻辑
- **Polymarket**: 提取链接中 `/event/` 后的标识符。
- **Kalshi**: 提取链接中 `/markets/` 后的核心标识符。

### 3.3 数据解析原则
```json
{
  "code": 1,
  "result": {
    "overallRisk": {
      "riskLevel": 2,
      "label": "Caution"
    },
    "tags": [ ... ],
    "notices": [ ... ]
  }
}
```
- **组合策略**：提取在根节点的 `overallRisk` 作为总评。将 `tags` 和 `notices` 数组合并，进行统一的扁平化遍历。
- **动态读取**：遍历的每一项，读取其 `label` (名称)、`description` (说明) 和 `riskLevel`。
- **风险映射规则**：
  - `riskLevel: 1` 映射为 `🟢` (安全/防操纵/分散等正面语意)。
  - `riskLevel: 2` 映射为 `🟡` (注意/一般等中性/提示语意)。
  - `riskLevel: 3` 映射为 `🔴` (危险/高风险等负面语意)。

## 4. 验收标准
1. 成功处理 Kalshi 的 `eventTicker` 参数或 Polymarket 的 `slug` 参数。
2. 报告必须包含统一的“总体评估”，并将所有 API 返回的指标拍平展示。
3. 纯文本最终回复中严禁出现原始的 `1/2/3` 面向机器的评级数字。

## 5. 测试规约 (Testing)
### 5.1 单元测试 (Unit Tests)
- **目标**: 验证 `parse_tags` 函数在各种 JSON 响应下的解析正确性。
- **覆盖场景**: 
    - 正常返回多个 tags。
    - 返回 notices 而非 tags。
    - 返回结果为空或 `None`。
    - 字段缺失逻辑。

### 5.3 交互快照测试 (Interaction Snapshot Tests)
- **目标**: 模拟端到端对话流，输出“用户问 -> AI 调 -> AI 答”的完整链路记录。
- **输出**: 自动化生成 `tests/test_report.md`，用于人类审查 Skill 的表达真实性。
- **验证项**:
    - 是否正确触发 Skill。
    - 提取的参数（slug/ticker）是否准确。
    - 最终回复是否符合 Formatting Standards。
