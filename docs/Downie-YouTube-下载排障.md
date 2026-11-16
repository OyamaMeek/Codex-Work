# Downie 下载 YouTube 时提示 GVS PO Token 无效

截图中的 4K AV1 下载需要通过 YouTube 的 PO Token 校验，Downie 报告它提供的令牌无效。PO Token 是 YouTube 用于检测自动化请求的令牌。Downie 从 4.9.1 起默认自动生成，4.9.3 移除了开关。[Downie 的 YouTube 帮助](https://software.charliemonroe.net/help/downie/?article=youtube#warning) · [版本说明](https://software.charliemonroe.net/trial/downie/v4/rnotes.html)

1. **先更新 Downie，再重新添加原视频链接。** 本机安装的是 4.12.11。截至 2026 年 11 月 16 日，官网发布记录首列 4.13.4，安装要求为 macOS 13 或更新版本。4.13.3 的更新记录列出 YouTube 兼容性改进。[官方下载](https://software.charliemonroe.net/downie/) · [版本说明](https://software.charliemonroe.net/trial/downie/v4/rnotes.html)
2. **若同样失败，试用「用户引导提取」。** 在菜单栏选择 `Browser > User-Guided Extraction…`，粘贴原视频链接并播放。若右侧检测到视频流，点击该项旁的 `+`。如果可以接受较低画质，也可在「设置 → 通用」选择每次询问，重新添加链接后选取可用的 1080p 或 720p 流。[用户引导提取](https://software.charliemonroe.net/help/downie/?article=uge) · [画质选择](https://software.charliemonroe.net/help/downie/?article=quality)
3. **若仍报错，通过应用内支持报告。** 点击主窗口右下角的支持按钮，选择 `Report a Link`，用英文附上原视频完整链接和报错。[Downie 故障排查](https://software.charliemonroe.net/help/downie/?article=reporting)

已核对官方文档和本机安装版本。该视频的下载结果仍需重试确认。
