# Siri AI 官方要求核对（2026-11-20）

- Apple 于 2026-11-12 更新的 [How to get Siri AI](https://support.apple.com/en-us/127893) 与 [Requirements for Siri AI](https://support.apple.com/en-mide/148218) 明确：Siri AI Beta 需要 iOS 27、支持 Apple Intelligence 的硬件、设备与 Siri 使用相同的受支持语言，以及合资格 Apple Account 地区；目前支持英语、法语、日语、韩语、葡萄牙语和西班牙语，未列中文。中国大陆区 Apple Account 当前不可用；iOS/iPadOS/watchOS 在欧盟暂不开放。入口为设置 → Siri → Try Siri AI (Beta)，高需求时可能需要候补。
- Erosion-CN README 将相机内嵌 SIRI 的 Beta 操作写为美区主 iCloud 与 en-US。该要求比当前官方列出的支持条件更窄，属于项目建议，不能表述为苹果当前只支持美国账号及美式英语。
- [Apple 的 ChatGPT 扩展指南](https://support.apple.com/en-gb/guide/iphone/iph00fd3c8c2/27/ios/27) 将 ChatGPT 扩展与 Siri AI 分别说明；ChatGPT 账号登录可选，扩展只在 ChatGPT 服务支持地区可用。普通 Siri 调用 ChatGPT 成功不证明新版 Siri AI 已启用。
- [Apple 企业网络端点文档](https://support.apple.com/en-ie/101555) 的搜索缓存确认 guzzoni.apple.com、*.smoot.apple.com、apple-relay.cloudflare.com、apple-relay.fastly-edge.com、cp4.cloudflare.com 与 apple-relay.apple.com；中继列出 TCP/UDP 443。正文访问两次返回 HTTP 429，未完整核对当前全部端点及是否新增 Siri AI 专用端点。
- Apple 官方未在以上可读取资料中保证“指定域名分流美国即可解锁”；Erosion-CN / AppleFlow 的 DIRECT、真实 IP 与美国节点分组属于项目经验配置，未在用户设备验证。域名分流不能替代硬件、系统、账号、语言及服务端资格。

未修改客户端、手机或 Git；未实机测试、抓包或执行视觉检查。
