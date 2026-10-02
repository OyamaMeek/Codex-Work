# 当前协作环境

## 2026-10-02 配置注释

- 执行代理：Codex；使用 using-superpowers、verification-before-completion，无子代理。
- 工具：本地文件读取与编辑、Python 标准库只读摘要核验、Surge 官方手册、Git。
- 仅修改 JIUWEI.conf 注释；配置含 CA 密钥与密码，不上传配置本体，不执行脚本或订阅访问。

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
