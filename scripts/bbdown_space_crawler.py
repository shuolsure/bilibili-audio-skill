#!/usr/bin/env python3
"""
从 BBDown debug 输出中提取 UP主视频列表
使用 BBDown 的内置能力获取视频列表，无需硬爬 API
"""

import subprocess
import re
import sys
import os

def get_video_list_from_bbdown(uid, cookie=None):
    """
    使用 BBDown 的 debug 模式获取 UP主视频列表
    
    参数:
        uid: UP主用户ID
        cookie: 可选的 Cookie 字符串
    
    返回:
        视频列表 [{'bvid': 'BVxxx', 'title': '标题', 'url': 'https://...'}, ...]
    """
    cmd = f'BBDown'
    if cookie:
        cmd += f' -c "{cookie}"'
    cmd += f' --debug "https://space.bilibili.com/{uid}"'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr
    
    videos = []
    pattern = r'"bvid":"(BV[^"]+)".*?"title":"([^"]+)"'
    
    matches = re.findall(pattern, output)
    
    seen = set()
    for bvid, title in matches:
        if bvid not in seen:
            seen.add(bvid)
            videos.append({
                'bvid': bvid,
                'title': title,
                'url': f'https://www.bilibili.com/video/{bvid}'
            })
    
    return videos

def main():
    if len(sys.argv) < 2:
        print("用法: python3 bbdown_space_crawler.py <用户UID> [输出文件]")
        print("示例: python3 bbdown_space_crawler.py 3546568888159133 videos.csv")
        sys.exit(1)
    
    uid = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"bilibili_{uid}_videos.csv"
    
    cookie_file = os.path.expanduser("~/tools/BBDown.data")
    cookie = None
    if os.path.exists(cookie_file):
        with open(cookie_file, 'r') as f:
            cookie = f.read().strip()
    
    print(f"正在使用 BBDown 获取用户 {uid} 的视频列表...")
    print("-" * 50)
    
    videos = get_video_list_from_bbdown(uid, cookie)
    
    print("-" * 50)
    print(f"共获取 {len(videos)} 个视频")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("标题,BV号,链接\n")
        for v in videos:
            title = v['title'].replace(',', '，').replace('"', '""')
            f.write(f'"{title}",{v["bvid"]},{v["url"]}\n')
    
    print(f"已保存到: {output_file}")
    
    print("\n前5个视频预览:")
    for i, v in enumerate(videos[:5], 1):
        print(f"{i}. {v['title']}")
        print(f"   {v['url']}")

if __name__ == '__main__':
    main()
