# 开发记录

## [2026-09-21 13:08] 移除导航中的两个百度条目

- **需求/问题描述**：
  > 移除“百度一下”和“百度汉语”两个导航条目，并推送到远端仓库。

- **实际实现的功能与改动**：
  - 从 WebStack-Hugo 的“其他”分组移除两个链接，并在导入规则中排除它们，避免重新导入旧数据库时回流。
  - 将迁移后链接数更新为 42，新增真实数据断言以验证两项排除规则。
  - [测试/验证]：真实数据测试 2 项通过；Hugo `v0.166.0+extended` 构建成功，静态页面不含两个已移除链接的 URL。

- **涉及文件**：
  - `blt-Launchpad/webstack-hugo/data/webstack.yml`
  - `blt-Launchpad/webstack-hugo/tools/import_wordpress.py`
  - `blt-Launchpad/webstack-hugo/tools/test_import_wordpress.py`
  - `blt-Launchpad/webstack-hugo/README.md`
  - `blt-Launchpad/webstack-hugo/docs/CHANGELOG.md`
  - `docs/CHANGELOG.md`

- **Git 提交**：网站项目：`fe536fb fix: remove unwanted navigation links`、`4a10991 docs: record navigation cleanup`。

---

## [2026-09-21 12:58] 迁移 WordPress 导航站为 WebStack-Hugo

- **需求/问题描述**：
  > 从 `blt-Launchpad/` 的旧 WordPress 数据库提取导航数据，整理为可部署的 WebStack-Hugo 项目，并提供 Cloudflare Pages 部署指南；不代为操作 Cloudflare。

- **实际实现的功能与改动**：
  - 在 `blt-Launchpad/webstack-hugo/` 建立独立 Hugo 项目，使用 SQL 解析器从真实备份迁移 44 条链接、12 个原始分类和 3 条归入“其他”的无分类链接。
  - 保留标题、URL、描述及排序；转换 4 个与主题不兼容的旧版图标，关闭无 key 的天气外链组件，并移除会自动更新子模块并推送的上游发布工作流。
  - 提供本地预览、数据重导入与手动 Cloudflare Pages 部署说明；项目不包含数据库备份、用户数据、媒体上传文件或密钥。
  - [测试/验证]：真实 SQL 数据的 2 项转换测试通过；Hugo `v0.166.0+extended` 构建成功，页面包含迁移链接与 4 个兼容图标，且不加载天气组件。上游主题使用已弃用的 `.Site.Data`，当前构建仅输出兼容性警告。

- **涉及文件**：
  - `blt-Launchpad/webstack-hugo/config.toml`
  - `blt-Launchpad/webstack-hugo/data/webstack.yml`
  - `blt-Launchpad/webstack-hugo/tools/import_wordpress.py`
  - `blt-Launchpad/webstack-hugo/tools/test_import_wordpress.py`
  - `blt-Launchpad/webstack-hugo/README.md`
  - `blt-Launchpad/webstack-hugo/.github/workflows/HugoAction.yml`（删除）
  - `docs/superpowers/specs/2026-09-21-wordpress-webstack-hugo-migration-design.md`
  - `docs/superpowers/plans/2026-09-21-wordpress-webstack-hugo-migration.md`
  - `docs/CHANGELOG.md`

- **Git 提交**：网站项目：`809eeca chore: initialize webstack hugo site`、`00ba95e feat: import wordpress navigation data`、`b457e81 docs: add site deployment guide`、`2872c1b fix: configure current hugo build`、`feb830b fix: harden migrated site configuration`、`d8abf8c chore: remove upstream deployment workflow`、`b8641c6 docs: clarify deployment setup`。

---

## [2026-09-17 12:47] 合并代理工作规则

- **需求/问题描述**：
  > 将 AGENT.md 与 TXAGENT.md 合并。

- **实际实现的功能与改动**：
  - 新增中文 `AGENTS.md`，按职责、沟通、规划、代码、验证、工具和 Git 工作流程整理两份规则并合并重复内容。
  - 明确完整设计与分步执行、视觉功能授权、依赖选择、错误处理和纠正记录的适用条件。
  - 纳入用户明确要求的自动提交、自动推送、开发记录与题目输出规范。
  - 保留两份来源文件。
  - [测试/验证]：核对规则覆盖、Markdown 结构和来源文件完整性；本次为文档合并，无代码运行测试。

- **涉及文件**：
  - `AGENTS.md`（新增）
  - `docs/CHANGELOG.md`（新增）

- **Git 提交**：未执行；当前目录没有 Git 仓库，无法提交或推送。

---

## [2026-09-19 13:18] 新增题目讲解 Agent 规则

- **需求/问题描述**：
  > 生成题目讲解 agent.md，规定教师式解析和 Notion 公式格式，将题图中的题目及解析保存为时间命名的 Markdown 并上传 Notion 数据库，原图保存到工作目录的 photo/。

- **实际实现的功能与改动**：
  - 新增独立的题目讲解规则文件，覆盖题目辨识、前提检查、逐步讲解、减少计算、公式格式及交付流程。
  - 规定时间文件名、同名冲突处理、原图保存与关联、Notion 数据库字段读取、同步核验和失败重试。
  - 为尚未指定的 Notion 数据库保留配置位置，初始化本次任务的简明协作记录。
  - [测试/验证]：文档要求与公式示例检查通过；本次文档差异无空白错误。全目录差异检查发现用户已有 `AGENTS.md` 的行尾空白，未修改该文件。本次只生成规则文档，未提供题图及目标数据库，不执行实际题目处理或 Notion 上传。

- **涉及文件**：
  - `题目讲解/agent.md`（新增）
  - `memory/agents.md`、`memory/plan.md`、`memory/progress.md`、`memory/verify.md`、`memory/gotchas.md`（新增）
  - `docs/CHANGELOG.md`（追加）

- **Git 提交**：`0d02025 docs: add problem explanation agent instructions`，已推送至 `origin/main`。

---

## [2026-09-19 13:42] 添加回答前的称呼规则

- **需求/问题描述**：
  > 在 AGENTS.md 中增加每次回答前称呼用户为“妹妹”的要求。

- **实际实现的功能与改动**：
  - 在“语言与输出”中明确每次回答先称呼用户为“妹妹”，再回复正文。
  - [测试/验证]：规则内容核对及 `git diff --check` 通过；本次仅修改文档，无需运行代码测试。

- **涉及文件**：
  - `AGENTS.md`
  - `docs/CHANGELOG.md`

- **Git 提交**：`611ec5c docs: address user as 妹妹 before every response`。

---

## [2026-09-19 13:47] 补全 AGENTS.md 中遗漏的要求

- **需求/问题描述**：
  > 补全对照 AGENT.md 发现的遗漏，保留自动推送、授权范围内直接执行及额外结构调整先取得授权的规则。

- **实际实现的功能与改动**：
  - 明确依据原始报错和命令输出排查，错误报告缺少输出时向用户索取。
  - 明确同一修复连续失败两次后，再次尝试前向用户说明错误假设。
  - 明确视觉证据使用 Markdown 记录，并将视觉正确性纳入独立验证要求。
  - 保留自动推送、结构调整授权边界及视觉验证需用户明确要求的规则。
  - [测试/验证]：补全内容及保留规则核对通过，`git diff --check` 通过；本次仅修改文档，无需运行代码测试。

- **涉及文件**：
  - `AGENTS.md`
  - `docs/CHANGELOG.md`

- **Git 提交**：`09400c2 docs: restore missing agent requirements`。

---

## [2026-09-21 07:30] 记录工作空间清理与日志保留规则

- **需求/问题描述**：
  > 工作空间中用过的文件会由用户手动删除，后续任务不处理这些历史文件的缺失，保留日志并上传 GitHub，将规则写入 Agent.md。

- **实际实现的功能与改动**：
  - 在现有 `AGENT.md` 中追加规则，明确历史任务文件删除属于正常清理，不恢复、不追查、不反复确认，不阻塞新任务。
  - 明确保留开发日志并自动提交、推送 GitHub，无关删除不混入当前提交。
  - 保留用户已有的文档修改及文件删除状态，仅提交本次追加的规则和日志。
  - [测试/验证]：规则覆盖及暂存范围核对通过，`git diff --cached --check` 通过；仅修改 Markdown 文档，无需运行代码测试。

- **涉及文件**：
  - `AGENT.md`（追加规则）
  - `docs/CHANGELOG.md`（追加记录）

- **Git 提交**：`87639e3 docs: respect workspace cleanup and retain task logs`。

---

## [2026-09-23 20:53] 归档当前对话并写入持续规则

- **需求/问题描述**：
  > 将对话转换成 `.md` 文件，放入以时间戳命名的文件夹，并把此规则写入 `agent.md`。

- **实际实现的功能与改动**：
  - 将本次会话截至归档时的用户与助手可见消息写入时间戳目录，并注明归档范围。
  - 在根目录 `AGENT.md` 中加入后续任务结束前归档当前会话的规则。
  - [测试/验证]：核对归档文件内容；本次仅修改 Markdown 文档，无需运行代码测试。

- **涉及文件**：
  - `context/2026-09-23_20-51-28/对话.md`（新增）
  - `AGENT.md`（追加规则）
  - `docs/CHANGELOG.md`（追加记录）

- **Git 提交**：`ab9a79f docs: archive conversation and add archive rule`。

---

## [2026-09-23 20:58] 改用年、月、日、时间目录归档对话

- **需求/问题描述**：
  > 将对话归档的时间戳目录改为“年/月/日/时间”层级。

- **实际实现的功能与改动**：
  - 将现有对话归档迁移至 `context/2026/09/23/20-57-42/`，并补入本次后续可见消息。
  - 更新 `AGENT.md` 中的归档路径规则为 `context/YYYY/MM/DD/HH-mm-ss/对话.md`。
  - [测试/验证]：核对归档路径、内容和暂存差异；仅修改 Markdown 文档，无需运行代码测试。

- **涉及文件**：
  - `AGENT.md`（更新归档规则）
  - `context/2026/09/23/20-57-42/对话.md`（从原时间戳目录迁移并补充消息）
  - `docs/CHANGELOG.md`（追加记录）

- **Git 提交**：待提交。

---
