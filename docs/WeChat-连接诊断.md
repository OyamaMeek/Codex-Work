# 微信图片连接诊断

更新时间：2026-10-03 09:48（本地时间）。

Surge 6.6.0 的本地日志确认：截图中的微信 HTTPS 请求经 DIRECT 连接 `240e:971:4001:3:1b::` 时发生 `Connection timeout`。同一请求的 QUIC 被模板中的通用 UDP 443 拒绝规则阻止；HTTPS 连接超时需要单独处理。

绑定物理接口进行 TCP 443 测试，排除仅连接到 Surge 虚拟网卡的假成功。下表是实际测试结果，超时限额为4秒：

| 目标 | 有线网络 en8 | Wi-Fi en0 |
| --- | --- | --- |
| 微信 IPv6 `240e:971:4001:3:1b::` | 超时 | 超时 |
| 国内 IPv6 对照 `2400:3200::1` | 超时 | 超时 |
| 国内 IPv4 对照 `223.5.5.5` | 约7毫秒连接成功 | 约14毫秒连接成功 |

物理接口测试与下面的实际图片对照共同支持：所测公网 IPv6 直连路径异常是本次图片加载故障的关键因素。尚不能定位到路由器、运营商或本机过滤的具体环节。

## 临时对照验证

用户批准临时验证并恢复。修改前确认 Wi-Fi 和 AX88179B 的 IPv6 均为“自动”；临时设为“仅本地链接”后，网络状态不包含可用 IPv6 状态，微信 IPv6 目标测试由4秒超时变为立即报告 No route to host，国内 IPv4 对照仍能连接。用户随后明确反馈“图片可以显示”。

验证后已恢复 Wi-Fi 和 AX88179B 的 IPv6“自动”模式，恢复命令均退出0，分别读取设置确认两者均为 Automatic。临时设置没有保留；恢复后是否复发尚未测试。

手动路径：系统设置 → 网络 → Wi-Fi / AX88179B → 详细信息 → TCP/IP → 配置 IPv6 → 仅本地链接。恢复时在相同位置选“自动”。[Apple 官方说明](https://support.apple.com/zh-cn/guide/mac-help/mh14129/mac)

仅修改 Surge 的 `ipv6 = false` 不能保证阻止微信直接使用 IPv6 地址；官方说明此参数关闭后仍可通过 IPv6 地址访问。[Surge 官方说明](https://manual.nssurge.com/profile/general.html)

长期采用“仅本地链接”可以作为经本次对照验证的绕过方式，会限制两条网络上所有应用的公网 IPv6 通信，需要用户另行确认。恢复 IPv6 自动模式前应先排查并修复网络的 IPv6 连通性。

上述网络对照完成时未修改模板与运行配置；诊断脚本保留于本地已忽略的 `.agent/happa-subconverter/probe_connections.py`。

## 当前微信 IPv6 拒绝规则

规则在 HappaConfig.ini 的 template 节中定义：

```ini
[template]
wechat_ipv6_rule=AND,((PROCESS-NAME,WeChat),(HOSTNAME-TYPE,IPv6)),REJECT-NO-DROP
```

此规则仅用于 Surge Mac，匹配 WeChat 进程直接访问 IPv6 地址的请求；域名解析后使用 IPv6 的请求不由 HOSTNAME-TYPE 保证拦截。[进程规则](https://manual.nssurge.com/rules/process.html)、[地址类型规则](https://manual.nssurge.com/rules/protocol-and-network.html)。REJECT-NO-DROP 避免频繁拒绝时自动升级为静默丢弃；它不会把 IPv6 地址转换为 IPv4，实际回退取决于微信。[拒绝策略](https://manual.nssurge.com/policies/reject.html)。

HappaConfig.conf 的 Rule 节首位通过 `{{ local.wechat_ipv6_rule }}` 引用该定义，按 [Subconverter 官方模板功能](https://github.com/tindy2013/subconverter/blob/master/README-cn.md#模板功能) 在转换时展开。官方0.9.0使用本机真实节点配置转换后，首位规则正确，58条规则的内容与顺序保持不变；19个节点和23个策略定义有效（20个组与3个地区直连别名），Surge 原生检查返回 OK。

当前 Surge 配置 261002-3 已加载展开后的首位拒绝规则，Wi-Fi 与 AX88179B 的 IPv6 保持 Automatic；本次移动定义无需改变运行规则或系统网络。恢复点保存于本地已忽略的 `.agent/happa-subconverter/261002-3-before-ipv6.conf`，其中含用户配置材料，不上传。

已请求重新打开微信并加载图片；重载后观察到5个微信 IPv4 直连请求收到315至1262字节下载数据。尚未确认新增拒绝规则的实际命中、回退因果或图片恢复，图片结果等待反馈。
