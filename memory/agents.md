# 当前协作环境

## 2026-10-09 SiriAI 规则列表

- Codex 单代理；复用 Surge RULE-SET 格式，使用本地只读条目核对与 Git。技能：using-superpowers、verification-before-completion。

## 2026-10-08 STUN 拦截

- Codex 单代理，using-superpowers、ponytail、verification-before-completion；复用官方 Subconverter 0.9.0、Python 标准库与 Surge 原生语法检查。
- 只修改共享转换模板；敏感转换输入和输出保留在已忽略的 .agent/happa-subconverter/，不重载活动配置。

## 2026-10-08 Website Cloner 安装

- Codex 单代理，using-superpowers；使用 Git、Node.js 26.5.1、npm 11.17.0 安装官方独立项目，不安装全局 skill。
- 来源提交 ee3f5a2f31fd549b9593fa4f7cf6d2955ee593bb；项目位于 ai-website-cloner-template/，从父仓库排除，移除项目上游 origin。

## 2026-10-06 Notion Browser 整理

- Codex 单代理，使用 Notion 连接器读取和更新原生内容；已读取 using-superpowers 与 ego-browser 技能。浏览器 TaskSpace 后续不可用，页面修改使用已连接 Notion 工具。

## 2026-10-06 DoT DNS

- Codex 单代理；using-superpowers、brainstorming、test-driven-development、verification-before-completion；复用官方 Subconverter 0.9.0、Python 标准库与 Surge 6.6.0 原生配置检查。
- 依据 Surge 当前加密 DNS 文档和 Cloudflare DoT 文档；只修改共享模板，不调整系统网络或活动配置。

## 2026-10-06 Claude 独立策略组

- Codex 单代理；使用 using-superpowers、verification-before-completion；复用官方 Subconverter 0.9.0 和 Surge 原生配置检查，curl 读取远程规则。

## 2026-10-06 China 默认直连

- Codex 单代理；使用 using-superpowers、verification-before-completion，执行 Python 只读配置核对与 Git 检查；仅调整 ini 中 China 首项。

## 2026-10-05 Claude 规则列表

- Codex 单代理；按 Surge 官方 RULE-SET 格式转换用户提供的9项域名，使用本地条目核对和 Git 检查。技能：using-superpowers、verification-before-completion。

## 2026-10-04 全部分流定义放入 ini

- Codex 单代理，复用 INJA local 变量、官方 Subconverter 0.9.0 与 Surge 原生检查；完整移动所有分流定义，不改变行为。

## 2026-10-04 微信分流定义直接放入 ini

- Codex 单代理，复用既有 INJA local 变量、Subconverter 0.9.0 和 Surge 原生检查；只移动规则定义位置。

## 2026-10-04 替换微信分流方法

- Codex 单代理执行，使用 brainstorming、test-driven-development 与 verification-before-completion。
- 使用官方 Subconverter 0.9.0 的实际节点转换结果和 Surge 原生配置检查；敏感输入输出仅保留于已忽略的 .agent/happa-subconverter/。
- 用户明确选择完整替换旧微信规则；不修改运行中的 Surge 配置或系统网络。

## 2026-10-04 自行车骑鹈鹕 SVG 动画

- Codex 单代理执行，参考 brainstorming、test-driven-development 与 verification-before-completion；ego-browser 验证浏览器实际行为。
- 独立 HTML 内嵌 SVG、CSS、JavaScript，按本次文字顺序表现自行车坐在鹈鹕背上；不执行截图或图像检查。

## 2026-10-04 鹈鹕骑行 SVG 动画

- 执行代理：Codex，无子代理；参考 brainstorming 与 verification-before-completion，浏览器行为验证使用 ego-browser。
- 单文件 HTML 内嵌 SVG、CSS 与 JavaScript，无外部资源；未经视觉验证授权，不截图或检查图片。

## 2026-10-03 HappaConfig 默认选择

- Emby 至 Final 的14个用途组首位新增 All Proxies，作为初始默认选项；节点组使用原筛选顺序，All Proxies 位于 Manual 与 Emby 之间。
- 官方 Subconverter 0.9.0 真实转换和 Surge 原生检查通过；tests/check_happa_defaults.py 输入为当前转换结果及新增 All Proxies 前的真实转换结果，检查默认项、原候选及节点顺序。验证服务已停止，节点材料只存已忽略目录。

## 2026-10-03 微信 IPv6 代理验证

- 用户明确授权现有 Proxy 所选节点及微信 IPv6 转发目标；ini 与活动配置 261003-2 的首位策略已改为 Proxy，系统网络未调整。
- 真实 Subconverter 转换保留19节点、23策略定义与58条规则，Surge 原生检查及有效规则读取通过；5项微信 IPv6 请求实际命中代理并收到数据，用户反馈“照片可以显示”。本地恢复点和凭据均留在已忽略目录，验证服务已停止。

## 2026-10-03 拒绝后的微信失败诊断

- 当前活动配置为 261003-2，首位拒绝规则已实际命中；用户确认图片仍失败，停止将拒绝视为可靠回退方式。
- 使用 Surge CLI 与原生 $httpClient 的 policy 选项进行真实 HEAD 对照，两项微信 IPv6 经现有 Proxy 均返回 HTTPS 响应；后续已获授权并完成代理应用与照片验证。

## 2026-10-03 ini 中的微信规则定义

- 规则定义位于 HappaConfig.ini 的 template.wechat_ipv6_rule；HappaConfig.conf 首位用 INJA 的 local 变量引用。
- 官方 Subconverter 0.9.0 已用本机实际配置转换成功：19个节点、23个策略定义（20组与3个地区直连别名）、58条原序规则；Surge 原生检查返回 OK。检查脚本位于已忽略的 .agent/happa-subconverter/，本地验证服务已停止。

## 2026-10-03 微信 IPv6 拒绝规则

- 在 HappaConfig.conf 和当前 Surge 配置 261002-3 的 Rule 节首位加入 WeChat 进程与 IPv6 地址类型的 AND 拒绝规则。
- 复用模板检查；Surge 自带 surge-cli 原生检查与重载通过，有效规则读取确认已加载。系统 IPv6 保持自动；重载后观察到5个微信 IPv4 直连请求收到下载数据，图片结果等待反馈。

## 2026-10-02 微信直连规则

- 执行代理：Codex；使用 systematic-debugging、test-driven-development 和 verification-before-completion，无子代理。
- 使用 Python 标准库 configparser 严格解析基础模板配置节；检查文件保留于 `.agent/happa-subconverter/check_template.py`。
- HappaConfig.conf 保留7条微信域名直连、已知 IP 网段与 Surge 微信规则集。已读取 Surge 6.6.0 本地日志并绑定物理网卡测试；临时限制公网 IPv6 后用户确认图片可以显示，网络设置已按授权恢复自动。实际订阅转换仍未验证。

## 2026-10-02 HappaConfig 模板

- 执行代理：Codex；使用 verification-before-completion，无子代理。
- 依据：Subconverter 官方外部配置示例、README-cn 与 Surge 导出源码；本地使用官方 darwinarm v0.9.0 二进制。
- 交付：HappaConfig.ini 与 HappaConfig.conf；保留中文注释，不包含私钥或固定订阅。
- 检查与运行文件位于已忽略的 `.agent/happa-subconverter/`；官方模板渲染检查通过，验证进程已终止。

## 2026-10-02 配置注释与英文分组

- 执行代理：Codex；使用 using-superpowers、verification-before-completion，无子代理。
- 工具：本地文件读取与编辑、Python 标准库只读摘要核验、Surge 官方手册、Git。
- 已补充 JIUWEI.conf 中文注释，并将9个中文策略组及引用改为英文；配置含 CA 密钥与密码，不上传配置本体，不执行脚本或订阅访问。

## 斯特朗线性代数教学环境

- 执行代理：Codex；本次未使用子代理。
- 教学技能：`~/.codex/skills/teach/SKILL.md`；一次一个问题，依据回答确认掌握。
- 来源：本地《斯特朗线性代数》第4版 PDF，520 页；用 bundled pypdf 读取书签，用原生 PDFKit/Vision 尝试提取扫描正文。
- 不修改或提交原始 PDF；中间文件放在已忽略的 `.agent/teach/`。

## 2026-10-01 drawio-skill 安装

- 执行代理：Codex；使用 skill-installer 和 verification-before-completion，无子代理。
- 来源：`Agents365-ai/drawio-skill` 的 `skills/drawio-skill/`，固定提交 `7aa92f73819766eb914fffac66762cf2adb5d828`。
- 安装目标：`~/.codex/skills/drawio-skill/`；安装器中间文件位于已忽略的 `.agent/drawio-install/`。

## 2026-10-01 AI-Coding-Guide-Zh 教学

- 执行代理：Codex；使用 teach 和 verification-before-completion，无子代理。
- 来源：本地 `AI-Coding-Guide-Zh/README.md` 及其四条路线的50篇教程；未找到同主题 Claude 会话，按本地材料教学。
- 仅维护教学清单与工作空间记录，不修改或提交原始教程目录。

## 2026-10-01 vibe coding 完整教程

- 执行代理：Codex；使用 human-writing、OpenAI Docs 和 verification-before-completion，无子代理。
- 教程采用本地 CX-02 的工作流材料，并核对 OpenAI 官方开发实践、AGENTS.md 和 MDN 本地存储资料。
- 交付单份 Markdown；不创建示例程序，不进行视觉检查，不改变学习确认数。
