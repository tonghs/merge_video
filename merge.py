# coding: utf-8

import sys
import os
# 主要是需要moviepy这个库
from moviepy.editor import VideoFileClip, concatenate_videoclips

# 定义一个数组
li = []

video_dir = './'
if len(sys.argv) > 1:
    video_dir = sys.argv[1]

# 访问 video 文件夹 (假设视频都放在这里面)
for root, dirs, files in os.walk(video_dir):
    # 按文件名排序
    files.sort()
    # 遍历所有文件
    for f in files:
        # 如果后缀名为 .mp4
        if os.path.splitext(f)[1] == '.mp4':
            # 拼接成完整路径
            filePath = os.path.join(root, f)
            # 载入视频
            video = VideoFileClip(filePath)
            # 添加到数组
            li.append(video)

if li:
    print('需要拼接的视频: ')
    for v in li:
        print(f"    {v.filename}")
    print('---> target.mp4')

    # 拼接视频
    final_clip = concatenate_videoclips(li)

    # 生成目标视频文件
    final_clip.write_videofile("./target.mp4", codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
