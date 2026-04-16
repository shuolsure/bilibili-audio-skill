# bilibili-audio

🎵 **B站视频音频下载神器！** 支持单个视频下载和批量UP主所有视频下载，集成 Claude Code Skill 一键调用。

## ✨ 功能特性

| 特性 | 说明 |
|------|------|
| 🎯 双模式 | 单个视频下载 + 批量UP主下载 |
| 🎵 最高音质 | 自动选择最高码率 M4A |
| ⏭️ 断点续传 | 自动跳过已下载视频 |
| 📝 字幕嵌入 | 自动嵌入字幕（如可用）|
| 🛡️ 防封禁 | 批量下载5秒间隔 |
| 📁 规范命名 | 日期_标题_BV号.m4a |

## 📦 安装

### 前置要求

```bash
# 安装 BBDown（必需）
brew install BBDown

# 登录 B站账号（首次使用）
BBDown login
```

### 作为 Claude Code Skill 安装

将此目录放置在 Claude Code 的 skills 目录下：
```bash
~/.claude/skills/bilibili-audio/
```

## 🚀 使用方法

### 单个视频下载

直接提供 B站视频链接：

```bash
/bilibili-audio https://b23.tv/xxx
```

支持的链接格式：
- `https://www.bilibili.com/video/BVxxx`
- `https://b23.tv/xxx`（短链接）

### 批量UP主下载

提供 UP 主用户ID或空间链接：

```bash
# 通过用户 ID
/bilibili-audio 593926706

# 通过空间链接
/bilibili-audio https://space.bilibili.com/593926706
```

> 💡 **如何获取用户ID**：UP主空间 URL 中的数字，如 `https://space.bilibili.com/593926706` 中的 `593926706`

## 📂 目录结构

```
bilibili-audio/
├── SKILL.md                           # Claude Code Skill 定义
├── README.md                          # 使用说明
└── scripts/
    └── bilibili_space_crawler.py     # 批量下载视频列表脚本
```

## 📁 输出位置

| 模式 | 保存路径 |
|------|----------|
| 单个视频 | `~/B站音频下载/` |
| 批量下载 | `~/B站音频下载/<用户ID>/` |

## 📝 文件命名格式

```
2025-06-27_【张雪峰】理科生必看！_BV118KZzzE1Q.m4a
```

格式：`发布日期_视频标题_BV号.m4a`

## 🔧 故障排查

| 问题 | 解决方案 |
|------|----------|
| 未安装 BBDown | `brew install BBDown` |
| Cookie 过期 | `BBDown login` 重新登录 |
| 下载失败 | 检查网络或稍后重试 |
| 视频不可用 | 可能被删除或会员专享 |
| 重新下载已跳过的 | `rm -f ~/tools/BBDown.archives` |

## 📋 示例

### 下载单个视频

```
用户：帮我下载这个B站视频 https://b23.tv/my4tCDF

助手：好的，我来下载这个视频的音频...

视频标题：【张雪峰】理科生必看！全网最全理科生志愿填报详细攻略
发布时间：2025-06-27
时长：35分14秒

✅ 下载完成！文件保存在 ~/B站音频下载/
```

### 批量下载UP主

```
用户：下载UP主 593926706 的所有视频音频

助手：识别到UP主ID: 593926706，开始批量下载...

获取视频列表... 找到 128 个视频
开始下载...

进度：128/128 | 成功：125 | 失败：3

✅ 下载完成！文件保存在 ~/B站音频下载/593926706/
```

## ⚠️ 注意事项

- 批量下载有 5 秒间隔，防止被 B站封禁
- 获取视频列表时有 1 秒间隔防限流
- 会员专享视频无法下载
- 已删除的视频会自动跳过

## 📜 许可证

MIT License

## 🔗 相关链接

- [BBDown GitHub](https://github.com/nilaoda/BBDown)
- [Claude Skills 文档](https://github.com/anthropics/skills)
