# 🎬 MeiamSubtitles (Fork)

> **Fork 自 [91270/MeiamSubtitles](https://github.com/91270/MeiamSubtitles)**  
> 本分支包含对 Shooter 字幕搜索的修复优化。

---

**MeiamSubtitles** 是一款专为 **Emby** 和 **Jellyfin** 媒体服务器打造的中文字幕下载插件。它集成了 **迅雷影音** 与 **射手网** 的强大搜索能力，支持精准的视频哈希（Hash）匹配，让您的媒体库自动补全高质量字幕。

## 🔧 Fork 修改内容 (v1.0.14.1)

### 修复：Shooter 搜索无结果

当文件名包含编码/画质标签时（如 `Focus 2015 2160p UHD Blu ray Remux HEVC DV DTS HD MA 7 1 W32.mkv`），Shooter API 无法匹配，返回空结果。

| 修改 | 说明 |
|------|------|
| **清理 pathinfo** | 新增 `CleanPathInfo()` 方法，自动提取"标题.年份"格式发送给 API |
| **放宽 Content-Type** | 同时接受 `application/json` 和 `application/octet-stream` 响应 |

**效果**：带有复杂编码标签的文件名现在能正常搜索到射手网字幕。

### 修改文件
- `Jellyfin.MeiamSub.Shooter/ShooterProvider.cs` ([diff](https://github.com/91270/MeiamSubtitles/compare/master...firexbox:MeiamSubtitles:master))

---

<p align="left">
  <img src="https://img.shields.io/badge/.NET-Standard%202.1%20%7C%209.0-blueviolet.svg" alt=".NET Status">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Win%20%7C%20OSX-brightgreen.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-Apache%202-blue" alt="LICENSE">
  <a href="https://github.com/91270/Emby.MeiamSub"><img src="https://img.shields.io/github/stars/91270/Emby.MeiamSub?label=Star%20this%20repo" alt="Star"></a>
</p>

## ✨ 核心特性

- **🚀 精准匹配**: 支持迅雷看看 (CID) 和射手网 (Hash) 双重校验逻辑，确保字幕与视频内容完美同步。
- **⚡ 极致性能**: 核心采样算法全面采用**异步 I/O (Async/Await)** 模式，在大规模媒体库扫描时不会阻塞服务器线程。
- **🌐 广泛兼容**: 深度适配 **Jellyfin 10.11+** 及 **Emby v4.9+**，支持 `zho`、`chi` 等多种国际化语言代码映射。
- **🛡️ 稳定可靠**: 针对射手网 API 的老化问题增加了防御性校验，能有效处理乱码返回，保证系统长效稳定。
- **📝 详尽日志**: 记录哈希计算耗时与接口原始响应，让问题排查不再是黑盒。

## 📦 项目组件说明

| 组件名称 | 适用平台 | 目标框架 | 说明 |
| :--- | :--- | :--- | :--- |
| **Emby.MeiamSub.Thunder** | Emby | .NET Standard 2.1 | 迅雷看看字幕插件 |
| **Emby.MeiamSub.Shooter** | Emby | .NET Standard 2.1 | 射手影音字幕插件 |
| **Jellyfin.MeiamSub.Thunder** | Jellyfin | .NET 9.0 | 迅雷看看字幕插件 (现代 DI 架构) |
| **Jellyfin.MeiamSub.Shooter** | Jellyfin | .NET 9.0 | 射手影音字幕插件 (现代 DI 架构) ⭐ 本 Fork 修复 |
| **Emby.MeiamSub.DevTool** | 开发调试 | .NET 8.0 | 哈希算法测试与 API 模拟工具 |

---

## 🚀 快速安装

### 第一步：获取插件
前往 [GitHub Releases](https://github.com/firexbox/MeiamSubtitles/releases) 下载最新版本的发布包。

> **🔔 推荐建议**：在媒体库设置中**不勾选**本插件作为默认自动下载器。建议仅在手动"搜索字幕"时使用，以获得更精准的人工筛选体验。

### 第二步：部署插件

#### 🔹 方式 A：Jellyfin 存储库安装
Jellyfin 用户可直接添加存储库：
1. 控制台 -> **插件** -> **存储库** -> 点击"添加"。
2. 输入名称 `MeiamSub-Fork` 和 URL：  
   `https://raw.githubusercontent.com/firexbox/MeiamSubtitles/refs/heads/master/Plugin/manifest-stable.json`
3. 在"目录"中找到插件并安装，重启服务即可。

#### 🔹 方式 B：手动安装
将下载的 `.dll` 文件（Jellyfin 用户请下载 `.zip` 并解压完整目录）放入服务器的 `plugins` 文件夹：

- **Linux/Docker**: `/config/plugins`
- **Windows**: `AppData\Local\jellyfin\plugins`
- **群晖/威联通**: 对应套件安装目录下的 `plugins` 文件夹

---

## ❓ 常见问题排查 (FAQ)

<details>
<summary><b>1. 为什么在 Jellyfin 10.11+ 中搜不到字幕？</b></summary>
新版 Jellyfin 采用了三位字母的语言代码（如 <code>zho</code>）。请确保您已升级至本插件的 <b>v1.0.13.0</b> 或更高版本，该版本已完美解决语言映射兼容性。
</details>

<details>
<summary><b>2. 射手网搜索无结果（含编码标签的文件名）？</b></summary>
<b>v1.0.14.1 已修复</b>。如果仍有问题，请提交 Issue 附带日志中的 <code>Target</code> 文件名和 <code>FileHash</code>。
</details>

<details>
<summary><b>3. 安装本插件后会影响 Open Subtitles 吗？</b></summary>
不会。本插件已将优先级 (Order) 调整为 100（低优先级），并在代码层面优化了并发逻辑，确保官方插件能优先获取请求机会。
</details>

---

## 🤝 贡献与感谢

欢迎通过提交 Issue 或 Pull Request 来完善本项目。

- **上游仓库**: [91270/MeiamSubtitles](https://github.com/91270/MeiamSubtitles)
- **致谢**: 感谢 [Emby.Subtitle.Subscene](https://github.com/nRafinia/Emby.Subtitle.Subscene) 提供的灵感与参考。

---

*Forked from [91270/MeiamSubtitles](https://github.com/91270/MeiamSubtitles) — Powered by Meiam*
