# 当前任务进度

## 2026-10-03 拒绝微信直接 IPv6 请求

- [x] 首位增加规则；新增断言先因缺失规则失败，修改后58条规则与23组检查通过，Surge 原生检查返回 OK。
- [x] 当前 Surge 配置保存恢复点后只新增同样两行（文件末尾空行经编辑工具规范化）；重载及有效规则首位读取确认通过，两条网络 IPv6 均 Automatic。
- [ ] 微信实际回退及图片加载：重载后观察到5个微信 IPv4 直连请求收到下载数据，尚未确认拒绝规则实际命中或图片恢复。
- [x] 保存记录、归档、提交并推送；提交 `022d784 fix: reject direct WeChat IPv6 requests` 已推送至 `origin/main`，公开模板下载后与本地逐字节一致。

## 2026-10-02 微信 DIRECT 超时诊断

- [x] 读取新增截图和 Surge 本地日志，确认微信 IPv6 TCP 连接错误为 Connection timeout，经 DIRECT；QUIC 被 UDP 443 规则拒绝。
- [x] 绑定 en8 / en0 测试：微信和国内对照 IPv6 均超时，国内 IPv4 对照连接成功。未绑定接口的 VIF 握手不作为外网连通证据。
- [x] 核对 Wi-Fi / AX88179B 的 IPv6 均为“自动”，准备临时“仅本地链接”并恢复“自动”的方案。
- [x] 用户批准临时验证并恢复；两条网络已暂设为仅本地链接，IPv6 目标立即报告 No route to host，IPv4 对照仍可用。
- [x] 用户反馈“图片可以显示”；两条网络已恢复 IPv6 自动模式，恢复命令退出0并再次读取确认。模板及当前 Surge 配置不变。
- [x] 保存诊断、归档、提交并推送；提交 `f649f04 docs: record WeChat IPv6 connection diagnosis` 已推送至 `origin/main`。

## 2026-10-02 完善微信 IP 与 IPv6 分流

- [x] 阅读两份指定资料及 issue 全部4条评论；确认当前7条规则没有 IP / IPv6 覆盖。
- [x] 增加明确 IP 网段与 Surge 微信规则集，验证优先级和原设置保留；检查先因缺少网段失败，修改后通过，规则共57条。
- [x] 保存记录、归档、提交及推送；提交 `3498921 fix: extend WeChat routing with IP and Surge ruleset` 已推送至 `origin/main`。
- 后续 DIRECT 超时诊断确认所测 IPv6 直连路径超时；临时限制公网 IPv6 后用户确认图片恢复，网络设置已恢复自动。

## 2026-10-02 微信图片直连规则

- [x] 修正规则节检查，修改前因畸形节标题退出1，修改后通过标准库配置解析。
- [x] 添加7条优先直连规则，保留其后48条原规则及其他设置；55条规则检查通过。
- [x] 检查、归档、提交并推送；提交 `108b17d fix: prioritize WeChat direct routing in HappaConfig` 已推送至 `origin/main`。
- 实际图片下载缺少请求日志，尚未验证。

## 2026-10-02 HappaConfig Subconverter 模板

- [x] 核对官方外部配置示例和 Surge 生成逻辑。
- [x] 创建 HappaConfig.ini 与 HappaConfig.conf，保留23个英文分组、48条原生规则及中文注释；微信任务已清理初版混入的策略组并新增7条规则。
- [x] 本地一致性检查通过；官方0.9.0渲染两文件的结果与源文件逐字节一致，验证进程已终止。
- [ ] 实际订阅转换验证：原地址返回 HTTP 404，已请求可用订阅链接；未获得输入，不生成虚构节点。
- [x] 保存记录与归档；模板提交 `c796397 feat: add HappaConfig subconverter template` 并推送至 `origin/main`；两个公开模板地址下载后与本地逐字节一致。原 JIUWEI.conf 保留本地。

## 2026-10-02 JIUWEI.conf 英文分组名

- [x] 重新读取用户当前配置，确认9个中文分组名与相关引用；保留 Direct / Reject。
- [x] 重命名9个分组与全部引用，保留中文注释；共修改61行。
- [x] 重命名检查修改前失败、修改后通过；149行有效内容仅发生预期名称替换，归档可见会话与开发记录。
- [x] 任务记录提交 `dff897f docs: record English JIUWEI group names`，已推送至 `origin/main`；含私钥的配置本体不提交。

## 2026-10-02 JIUWEI.conf 中文注释

- [x] 读取完整配置及 Surge 官方说明，记录有效内容摘要。
- [x] 补充七个配置节的中文注释，保持有效内容完全一致。
- [x] 149 行有效内容摘要与修改前一致，行尾空白检查通过。
- [x] 保存任务日志与可见对话。
- [x] 任务记录提交 `660941b docs: record JIUWEI configuration annotations`，已推送至 `origin/main`；配置含 CA 密钥与密码，保留本地且不提交。

## 斯特朗线性代数教学进度

- [x] 找到指定 PDF，核验 520 页及实际章节书签。
- [x] 确认扫描正文无法通过 pypdf 直接提取文字。
- [x] 用 PDFKit/Vision 读取 PDF 第22–24页，确认 1.2 的行图与列图主题。
- [x] 建立并验证 43 项学习清单，全部未勾选。
- [x] 保存会话归档、开发记录；提交 `75499e3 docs(teaching): add Strang linear algebra checklist`。
- [x] 推送当前分支至已配置的 `origin/main`，远端已确认接收至 `50f49e9`。
- [ ] 等待用户对第一个诊断问题的回答；当前掌握情况为 0/43。
- 教学清单：`sessions/teaching/2026-09-30-strang-linear-algebra-4e.md`。
- 用户已有的文件修改、删除、未跟踪项目及原始 PDF 不纳入本次提交。

## 2026-10-01 drawio-skill 安装进度

- [x] 读取完整 README 和安装说明，确认技能路径及版本 3.4.0，目标目录未占用。
- [x] 使用 skill-installer 安装 3.4.0 到 `~/.codex/skills/drawio-skill/`。
- [x] 核验 SKILL.md、scripts/、references/；doctor 及 CLI 帮助均退出 0。
- [x] 保存开发记录、截至归档时的可见对话。
- [x] 安装记录与归档已提交：`8894056 docs: record drawio-skill installation`。
- [x] 已普通推送至 `origin/main`，远端确认接收至 `2569254`；已无冲突合并远端的历史图片删除提交。
- doctor：Python 3.9.6 可用；draw.io、Graphviz 未安装，原生导出及自动布局不可用；PyYAML、python-pptx、Pillow 为未安装的可选依赖。
- 用户原有的 AGENTS.md 修改、文件删除及 .DS_Store 不纳入本次提交。

## 2026-10-01 AI-Coding-Guide-Zh 教学进度

- [x] 确认本地教程目录及 README 中的四条路线、50篇教程。
- [x] 读取 CX-02 的核心模型、任务描述及 Review 部分，用于开场诊断。
- [x] 建立并核验50项教学清单；初始确认数0，50篇来源文件均存在。
- [x] 保存本次日志与可见对话；提交 `192b67a docs(teaching): add AI-Coding-Guide-Zh checklist`，已推送至 `origin/main`。
- [x] 按用户最新要求生成单份完整 vibe coding 教程，共19节；不等待逐步回答，确认数保持0/50。
- [x] 核验19节标题、代码块闭合、12项练习验收、4个资料页面及写作规则；http.server 帮助确认启动参数有效。
- [x] 教程、归档、日志及记忆提交为 `bb4cfa5 docs: add complete vibe coding tutorial`，已推送至 `origin/main`。
- 教程目标：`docs/Vibe-Coding-从零到交付完整教程.md`。
- 清单：`sessions/teaching/2026-10-01-ai-coding-guide-zh.md`。
- 正文按轮次读取；尚未核验教程所述产品版本或完成全部正文阅读。
