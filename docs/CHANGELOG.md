# CHANGELOG

## [2026-03-20]
### Added
- 初始化项目结构（基于 template-skill）。
- [Project] 完成 1-5 阶段生命周期治理架构调整。
- [Skill] 开始建立自动化测试框架，规划单元测试与集成测试内容。
- [Skill] 优化简报排版：提取 `overallRisk` 作总评，将 `tags` 与 `notices` 合并为单层扁平列表，增加 `绿黄红` 动态状态映射，剔除数字评级。

### Changed
- 修正物理目录结构以对齐官方规范（SKILL.md 移至根目录，tools 命名为 scripts）。
- 细化 PRD：加入 Polymarket & Kalshi API 接口规范、参数提取逻辑及重试机制。
- 进一步完善 PRD：放宽触发条件（泛预测市场话题触发）、支持多语言报告、优化条件化错误报告逻辑。
- **技术逻辑修正**：根据用户提供的核心 Tips，修正了 Kalshi 的参数名（eventTicker）、明确了必须通过后端/代理请求、以及 `tags` 数组的解析逻辑。

### Fixed
- 根据最新 PRD 启动技术实现逻辑。
