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
  "code": 0,
  "data": {
    "tags": [
      {
        "name": "liquidity",
        "riskLevel": 1,
        "description": "..."
      }
    ]
  }
}
```
- 严禁直接读取扁平属性，必须通过 `tags` 数组检索。

## 4. 验收标准
1. 成功处理 Kalshi 的 `eventTicker` 参数。
2. 报告能正确展示 `tags` 数组中的多项指标及其风险等级（1-安全，2-注意，3-危险）。
