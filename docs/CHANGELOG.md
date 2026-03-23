# CHANGELOG

## [2026-03-20]
### Added
- 初始化项目结构（基于 template-skill）。
- 编写初始 PRD 需求文档。

### Changed
- 修正物理目录结构以对齐官方规范（SKILL.md 移至根目录，tools 命名为 scripts）。
- 细化 PRD：加入 Polymarket & Kalshi API 接口规范、参数提取逻辑及重试机制。
- 进一步完善 PRD：放宽触发条件（泛预测市场话题触发）、支持多语言报告、优化条件化错误报告逻辑。
- **技术逻辑修正**：根据用户提供的核心 Tips，修正了 Kalshi 的参数名（eventTicker）、明确了必须通过后端/代理请求、以及 `tags` 数组的解析逻辑。

### Fixed
- 根据最新 PRD 启动技术实现逻辑。
