# 五个仓库安装记录

安装时间为2026-10-21，平台为macOS、Codex。源码与资源目录位于 `/Users/oyamahappa/Documents/Agent/Codex/`，这些目录不推送至协作文档仓库。

| 仓库 | 实际安装 | 来源提交 |
| --- | --- | --- |
| anthropics/knowledge-work-plugins | Codex原生市场及README列出的11个官方插件，均已启用 | bc8f6922cfeea215a202cdcc9f0d299a990889a8 |
| uiverse-io/galaxy | 本地 `galaxy/`，3802份非空HTML组件 | adbd2adde0a299a3956ea288fb444ec01891ca41 |
| greensock/gsap-skills | `~/.codex/skills/gsap-*`，8个技能 | aed9cfd3277740755f6bfc1155c7aa645403b760 |
| Graphify-Labs/graphify | Graphify 0.9.93及Codex技能 | b90b9df7949bd04a15b40a1624af85d0a9cfdf04 |
| HKUDS/CLI-Anything | cli-anything、cli-hub-meta-skill两个技能及CLI-Hub 0.4.1 | 34f519533bc175d2fe287ab8316b0dd99bb9cc43 |

Anthropic插件为 productivity、sales、customer-support、product-management、marketing、legal、finance、data、enterprise-search、bio-research、cowork-plugin-management。市场来源已注册为GitHub，安装缓存位于 `~/.codex/plugins/cache/knowledge-work-plugins/`。未批量安装第三方市场条目；外部服务按需另行登录授权。

GSAP技能为 gsap-core、gsap-timeline、gsap-scrolltrigger、gsap-plugins、gsap-utils、gsap-react、gsap-performance、gsap-frameworks。下一轮对话可加载新技能；插件若尚未出现在界面中，重新打开Codex。

Graphify和CLI-Hub各自使用独立Python 3.12环境，分别位于 `~/.local/share/graphify/venv/` 和 `~/.local/share/cli-anything-hub/venv/`。`graphify`、`cli-hub`入口位于已有PATH目录 `~/.local/bin/`，不依赖工作区源码。Graphify仅注册技能，未启用常驻守卫或修改项目AGENTS.md。

可在Codex中指定 `$graphify` 分析目标代码，或使用CLI-Anything生成目标软件的CLI。CLI-Hub可通过 `cli-hub list --json` 查询工具目录；具体应用及其后端按任务需要安装。CLI-Hub上游默认启用匿名使用统计，本次联网检查使用 `CLI_HUB_NO_ANALYTICS=1` 禁用；后续需要禁用时保留此环境变量。

验证结果：

- 五个仓库Git完整性、父仓库忽略规则通过；11个插件的233个缓存文件与来源一致，原生CLI确认installed/enabled。
- GSAP技能、CLI-Hub元技能与Graphify技能及8份配套参考文件逐字节比较通过。
- CLI-Anything官方安装器测试通过，覆盖资源同步、拒绝覆盖和脚本编译；Graphify、CLI-Hub的pip check均通过。
- Graphify以 `GRAPHIFY_BACKEND=none` 解析GSAP官方示例的14个真实代码文件，输出87节点、90关系；explain查询成功。未调用模型或生成视觉预览。
- CLI-Hub实际获取103项工具目录。未安装全部应用后端，也未验证外部账号工作流和文档语义分析。

本地验证脚本与结果位于 `.agent/five-repo-install/`，不推送。清理工作区源码不影响已安装的技能与两个工具；Galaxy组件库需要保留或另行备份。
