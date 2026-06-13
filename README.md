# 🎬 MeiamSubtitles (Fork)

> **Fork 自 [91270/MeiamSubtitles](https://github.com/91270/MeiamSubtitles)**  
> 本分支修复了 Jellyfin 环境下 Shooter 字幕搜索的三个关键问题。

---

**MeiamSubtitles** 是一款专为 **Emby** 和 **Jellyfin** 媒体服务器打造的中文字幕下载插件。它集成了 **迅雷影音** 与 **射手网** 的强大搜索能力，支持精准的视频哈希（Hash）匹配。

## 🔧 Fork 修改内容 (v1.0.14.1)

### 问题背景

安装 MeiamSubtitles 后 Jellyfin 搜不到 Shooter 字幕。排查发现三个叠加问题：

| # | 问题 | 症状 | 修复 |
|---|------|------|------|
| 1 | **Jellyfin 版本不匹配** | `Failed to load assembly ... incompatible version` | 升级 Jellyfin 到 ≥10.11.11 |
| 2 | **Zip 解压路径损坏** | DLL 锁在反斜杠目录名里 `Jellyfin.MeiamSub.Shooter_1.0.14.0\` | `publish.ps1` 修复 + 新增 `publish.py` |
| 3 | **pathinfo 太复杂** | Shooter API 返回 `0xFF`（0 结果） | 新增 `CleanPathInfo()` + 放宽 Content-Type |

### 修改文件

| 文件 | 修复 | 说明 |
|------|------|------|
| `Jellyfin.MeiamSub.Shooter/ShooterProvider.cs` | #3 | 新增 `CleanPathInfo()` 提取标题+年份；放宽 Content-Type 检查 |
| `publish.ps1` | #2 | 新增 `Fix-ZipPaths()` 将 zip 内反斜杠转为正斜杠 |
| `publish.py` | #2 | Linux/macOS 原生打包脚本，不需要 PowerShell |
| `README.md` | — | Fork 声明 + 完整问题记录 |

### 修复效果

- **修复前**：`Focus 2015 2160p UHD Blu ray Remux HEVC DV DTS HD MA 7 1 W32.mkv` → 0 条结果
- **修复后**：自动提取 `Focus.2015.mkv` → 3 条 Shooter 字幕

---

## 📦 项目组件说明

| 组件名称 | 适用平台 | 目标框架 | 说明 |
| :--- | :--- | :--- | :--- |
| **Jellyfin.MeiamSub.Shooter** | Jellyfin | .NET 9.0 | 射手影音字幕插件 ⭐ 本 Fork 修复 |
| **Jellyfin.MeiamSub.Thunder** | Jellyfin | .NET 9.0 | 迅雷看看字幕插件 |
| **Emby.MeiamSub.Shooter** | Emby | .NET Standard 2.1 | 射手影音字幕插件 |
| **Emby.MeiamSub.Thunder** | Emby | .NET Standard 2.1 | 迅雷看看字幕插件 |

**依赖**：Jellyfin ≥ 10.11.11

---

## 🚀 快速安装

### 第一步：获取插件
前往 [GitHub Releases](https://github.com/firexbox/MeiamSubtitles/releases) 下载最新版本的发布包。

### 第二步：部署插件

#### 🔹 方式 A：Jellyfin 存储库安装
1. 控制台 -> **插件** -> **存储库** -> 点击"添加"
2. 输入名称 `MeiamSub-Fork` 和 URL：  
   `https://raw.githubusercontent.com/firexbox/MeiamSubtitles/refs/heads/master/Plugin/manifest-stable.json`
3. 在"目录"中找到插件并安装，重启服务

#### 🔹 方式 B：手动安装
将下载的 `.dll` 放入 Jellyfin 的 `plugins` 目录：

- **Linux/Docker**：`/config/plugins`
- **Windows**：`AppData\Local\jellyfin\plugins`

> **注意**：确保 Jellyfin 版本 ≥ 10.11.11，否则插件无法加载。

---

## ❓ 常见问题

<details>
<summary><b>1. 射手网搜索无结果（含编码标签的文件名）？</b></summary>
<b>v1.0.14.1 已修复</b>。插件现在会自动清理文件名中的编码标签（2160p、HEVC、DTS 等），提取标题+年份发送给 Shooter API。
</details>

<details>
<summary><b>2. 安装后 Jellyfin 日志显示 "Failed to load assembly"？</b></summary>
Jellyfin 版本过低。本插件编译时引用 <code>MediaBrowser.Common 10.11.11</code>，需要 Jellyfin ≥ 10.11.11。<br>
Docker 用户执行：<code>docker pull jellyfin/jellyfin:latest && docker stop jellyfin && docker rm jellyfin && docker run ...</code>
</details>

<details>
<summary><b>3. Zip 解压后找不到 DLL？</b></summary>
<b>v1.0.14.1 已修复</b>。之前的 zip 在 Windows 打包时路径使用反斜杠，Linux 解压后 Dll 锁在带 <code>\</code> 的目录名中。Release 中附带单独 DLL 可直接覆盖使用。
</details>

---

## 🤝 贡献

欢迎通过提交 Issue 或 Pull Request 来完善本项目。

- **上游仓库**：[91270/MeiamSubtitles](https://github.com/91270/MeiamSubtitles)
- [完整对比 diff](https://github.com/91270/MeiamSubtitles/compare/master...firexbox:MeiamSubtitles:master)

---

*Forked from [91270/MeiamSubtitles](https://github.com/91270/MeiamSubtitles) — Powered by Meiam*
