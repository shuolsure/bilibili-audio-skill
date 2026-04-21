#!/usr/bin/env python3
"""
B站用户空间视频列表抓取工具
合规声明：仅爬取公开内容，控制请求频率，仅供学习使用
"""

import hashlib
import time
import random
import requests
import json
import os
import sys

# WBI签名索引表
WBI_MIX_TABLE = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62,
    11, 36, 20, 34, 44, 52
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com',
    'Cookie': 'SESSDATA=91c1b163%2C1790687426%2Cd43bc*41CjBckywo8jri0K6qrfxZrrR4zBunlPbJiGe_HNjhecR3eBDtQSQa-IX-F5wuT67woWwSVlJqQ3ZCMEdLM2VDN2R6cG1hT3JPTk1JaWVxTUk2ZGE4bW5HQ20zeHJVU0dvQ0I5SDdYaGs4Yjd4RlNzOEp3Y0JNbGlnWUJEM0hPNlBGbWRfcVlTelFnIIEC'
}

def get_wbi_keys():
    """从nav接口获取img_key和sub_key"""
    url = "https://api.bilibili.com/x/web-interface/nav"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    data = resp.json()
    
    if data['code'] == 0:
        img_url = data['data']['wbi_img']['img_url']
        sub_url = data['data']['wbi_img']['sub_url']
        img_key = img_url.split('/')[-1].split('.')[0]
        sub_key = sub_url.split('/')[-1].split('.')[0]
        return img_key, sub_key
    else:
        print(f"API错误: {data.get('message', '未知')}")
    return None, None

def mix_keys(img_key, sub_key):
    """混合密钥"""
    combined = img_key + sub_key
    mixed = []
    for idx in WBI_MIX_TABLE:
        if idx < len(combined):
            mixed.append(combined[idx])
    return ''.join(mixed)[:32]

def enc_wbi(params, mix_key):
    """生成WBI签名"""
    # 添加时间戳
    params['wts'] = int(time.time())
    
    # 按key排序并拼接
    sorted_params = sorted(params.items())
    query = '&'.join([f'{k}={v}' for k, v in sorted_params if v])
    
    # URL编码特殊字符
    query = query.replace('!', '%21').replace("'", '%27').replace('(', '%28')
    query = query.replace(')', '%29').replace('*', '%2A')
    
    # 计算MD5签名
    sign = hashlib.md5((query + mix_key).encode('utf-8')).hexdigest()
    
    return sign, params['wts']

def get_user_videos(mid, page=1, page_size=30, mix_key=None):
    """获取用户投稿视频列表"""
    params = {
        'mid': mid,
        'ps': page_size,
        'pn': page,
        'tid': 0,
        'order': 'pubdate',
        'platform': 'web',
        'web_location': 1550101,
        'order_avoided': 'true'
    }
    
    if mix_key:
        w_rid, wts = enc_wbi(params.copy(), mix_key)
        params['w_rid'] = w_rid
        params['wts'] = wts
    
    url = "https://api.bilibili.com/x/space/wbi/arc/search"
    resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
    
    # 调试：检查响应状态
    if resp.status_code != 200:
        print(f"HTTP状态码: {resp.status_code}")
        print(f"响应内容: {resp.text[:500]}")
        return {'code': -1, 'message': f'HTTP {resp.status_code}'}
    
    try:
        return resp.json()
    except:
        print(f"响应不是JSON: {resp.text[:500]}")
        return {'code': -1, 'message': 'Invalid JSON'}

def main():
    if len(sys.argv) < 2:
        print("用法: python3 bilibili_space_crawler.py <用户UID> [输出文件]")
        print("示例: python3 bilibili_space_crawler.py 3546568888159133 videos.txt")
        sys.exit(1)
    
    mid = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"bilibili_{mid}_videos.csv"
    
    print(f"正在获取用户 {mid} 的视频列表...")
    print("合规声明：仅爬取公开内容，控制请求频率")
    print("-" * 50)
    
    # 获取WBI密钥
    print("正在获取签名密钥...")
    img_key, sub_key = get_wbi_keys()
    
    if not img_key:
        print("错误：无法获取签名密钥")
        sys.exit(1)
    
    mix_key = mix_keys(img_key, sub_key)
    print(f"签名密钥已获取")
    
    # 抓取视频列表
    all_videos = []
    page = 1
    page_size = 30
    
    while True:
        print(f"正在获取第 {page} 页...")
        
        try:
            data = get_user_videos(mid, page, page_size, mix_key)
            
            if data['code'] != 0:
                print(f"API错误: {data.get('message', '未知错误')}")
                break
            
            vlist = data['data']['list']['vlist']
            
            if not vlist:
                print("已获取所有视频")
                break
            
            for video in vlist:
                all_videos.append({
                    'title': video['title'],
                    'bvid': video['bvid'],
                    'url': f"https://www.bilibili.com/video/{video['bvid']}",
                    'pubdate': video['created'],
                    'play': video['play'],
                    'duration': video['length']
                })
            
            total = data['data']['page']['count']
            print(f"  已获取 {len(all_videos)}/{total} 个视频")
            
            if len(all_videos) >= total:
                break
            
            page += 1
            delay = random.uniform(2, 5)
            time.sleep(delay)
            
        except Exception as e:
            print(f"错误: {e}")
            break
    
    # 保存结果
    print("-" * 50)
    print(f"共获取 {len(all_videos)} 个视频")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("标题,BV号,链接,发布时间,播放量,时长\n")
        for v in all_videos:
            title = v['title'].replace(',', '，').replace('"', '""')
            f.write(f'"{title}",{v["bvid"]},{v["url"]},{v["pubdate"]},{v["play"]},{v["duration"]}\n')
    
    print(f"已保存到: {output_file}")
    
    # 预览前5个
    print("\n前5个视频预览:")
    for i, v in enumerate(all_videos[:5], 1):
        print(f"{i}. {v['title']}")
        print(f"   {v['url']}")

if __name__ == '__main__':
    main()
