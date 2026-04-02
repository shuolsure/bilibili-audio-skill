# bilibili-audio - 批量下载B站UP主音频

批量下载B站指定UP主的所有投稿视频音频文件。

## 使用方法

```
/bilibili-audio <用户ID>
```

示例：
```
/bilibili-audio 593926706
```

用户ID获取：UP主空间URL中的数字，如 `https://space.bilibili.com/593926706`

## 功能

- 最高音质下载（128kbps+ M4A）
- 5秒间隔防封禁
- 自动跳过已下载视频
- 文件命名：`日期_标题_BV号.m4a`
- 保存路径：`~/B站音频下载/<用户ID>/`

## 执行步骤

1. 获取UP主视频列表（WBI签名+1秒间隔防限流）：
   ```bash
   python3 ~/bilibili_space_crawler.py <用户ID> ~/bilibili_<用户ID>_videos.csv
   ```

2. 从CSV提取URL并保存为txt：
   ```bash
   tail -n +2 ~/bilibili_<用户ID>_videos.csv | cut -d',' -f3 > ~/bilibili_<用户ID>_videos.txt
   ```

3. 创建下载目录：
   ```bash
   mkdir -p ~/B站音频下载/<用户ID>
   ```

4. 循环下载音频（5秒间隔）：
   ```bash
   while read url; do
     echo "=== 下载: $url ==="
     BBDown --audio-only --save-archives-to-file \
       --work-dir ~/B站音频下载/<用户ID> \
       -F '<publishDate>_<videoTitle>_<bvid>' "$url"
     sleep 5
   done < ~/bilibili_<用户ID>_videos.txt
   ```

5. 打开下载目录：
   ```bash
   open ~/B站音频下载/<用户ID>/
   ```

6. 统计结果

## 注意事项

- 获取视频列表时有1秒间隔防限流
- 下载时有5秒间隔防封禁
- 下载记录保存在 `~/tools/BBDown.archives`
- 重新下载已跳过的视频：`rm -f ~/tools/BBDown.archives`