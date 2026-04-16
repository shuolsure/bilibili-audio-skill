# bilibili-audio

B站视频音频下载工具，支持单个视频下载和批量下载UP主所有视频音频。

## 功能特性

- 支持单个视频下载（通过 URL）
- 支持批量下载 UP 主所有视频（通过用户 ID）
- 最高音质下载（自动选择最高码率 M4A）
- 自动跳过已下载视频
- 字幕自动嵌入（如可用）
- 断点续传支持
- 文件命名：`日期_标题_BV号.m4a`
- 批量下载有 5 秒间隔防封禁

## 前置要求

### 必需工具

1. **BBDown** - B站视频下载工具
   ```bash
   brew install BBDown
   ```

2. **Python 3** - 用于批量下载时的视频列表获取

### 批量下载额外依赖

批量下载需要 `bilibili_space_crawler.py` 脚本：
```bash
# 脚本应放置在用户主目录
~/bilibili_space_crawler.py
```

## 安装

### 作为 Claude Code Skill 使用

将此目录放置在 Claude Code 的 skills 目录下：
```
~/.claude/skills/bilibili-audio/
```

## 使用方法

### 单个视频下载

提供 B站视频链接即可：

```bash
/bilibili-audio https://www.bilibili.com/video/BVxxx
# 或短链接
/bilibili-audio https://b23.tv/xxx
```

**支持的链接格式**：
- `https://www.bilibili.com/video/BVxxx`
- `https://b23.tv/xxx`（短链接）

### 批量下载 UP 主视频

提供 UP 主的用户 ID 或空间链接：

```bash
# 通过用户 ID
/bilibili-audio 593926706

# 通过空间链接
/bilibili-audio https://space.bilibili.com/593926706
```

**如何获取用户 ID**：
- UP 主空间 URL 中的数字，如 `https://space.bilibili.com/593926706` 中的 `593926706`

## 输出位置

| 模式 | 保存路径 |
|------|----------|
| 单个视频 | `~/B站音频下载/` |
| 批量下载 | `~/B站音频下载/<用户ID>/` |

## 文件命名格式

下载的音频文件命名格式：
```
2025-06-27_【张雪峰】理科生必看！_BV118KZzzE1Q.m4a
```

格式：`发布日期_视频标题_BV号.m4a`

## 配置说明

### Cookie 登录

首次使用需要登录 B站账号：

```bash
BBDown login
```

按提示扫描二维码登录。登录状态保存在本地 cookie 中。

### 下载记录

- 下载记录保存在 `~/tools/BBDown.archives`
- 重新下载已跳过的视频：`rm -f ~/tools/BBDown.archives`

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 未安装 BBDown | `brew install BBDown` |
| Cookie 过期 | 运行 `BBDown login` 重新登录 |
| 下载失败 | 检查网络连接或稍后重试 |
| 视频不可用 | 可能被删除或会员专享 |
| 批量下载被限流 | 等待一段时间后重试 |
| 重新下载已跳过的 | `rm -f ~/tools/BBDown.archives` |

## 示例

### 示例 1：下载单个视频

```
用户：帮我下载这个B站视频 https://b23.tv/my4tCDF
助手：好的，我来下载这个视频的音频...

视频标题：【张雪峰】理科生必看！全网最全理科生志愿填报详细攻略
发布时间：2025-06-27
时长：35分14秒

下载完成！文件保存在 ~/B站音频下载/
```

### 示例 2：批量下载 UP 主

```
用户：下载UP主 593926706 的所有视频音频
助手：识别到UP主ID: 593926706，开始批量下载...

获取视频列表...
找到 128 个视频
开始下载...

进度：128/128
成功：125
失败：3

下载完成！文件保存在 ~/B站音频下载/593926706/
```

## 注意事项

- 批量下载有 5 秒间隔，防止被 B站封禁
- 获取视频列表时有 1 秒间隔防限流
- 会员专享视频无法下载
- 已删除的视频会跳过

## 许可证

MIT License

## 相关链接

- [BBDown GitHub](https://github.com/nilaoda/BBDown)
- [Claude Skills 文档](https://github.com/anthropics/skills)
