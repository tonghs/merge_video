# coding: utf-8

import sys
import os
# 主要是需要moviepy这个库
from moviepy.editor import VideoFileClip, concatenate_videoclips
import shutil


def clip(video, path, start=0):
    # 需要裁剪文件，先备份
    print('... 备份中')
    filename = video.filename

    bak_path = os.path.join(path, 'bak')
    if not os.path.exists(bak_path):
        os.makedirs(bak_path)

    shutil.copyfile(filename, os.path.join(bak_path, filename.split('/')[-1]))

    print('... 开始裁切')
    tmp_name = filename.split('.')
    new_filename = tmp_name[0] + '_clip.' + tmp_name[1]

    result = video.subclip(start, None)
    result.write_videofile(os.path.join(path, new_filename), codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
    video.reader.close()

    # 删除原文件
    if os.path.exists(filename):
        # 删除文件，可使用以下两种方法。
        os.remove(filename)

    return new_filename


def get_video_list(path):
    li = []
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

    return li


def merge(li, path, start=0):
    if not li:
        return

    if start:
        print('需要裁切视频，开始时间:', start, li[0].filename)
        li[0] = clip(li[0], path, start)

    print('需要拼接的视频: ')
    for v in li:
        print(f"    {v.filename}")
    print('---> target.mp4')

    # 拼接视频
    final_clip = concatenate_videoclips(li)

    # 生成目标视频文件
    final_clip.write_videofile("./target.mp4", codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)


if __name__ == '__main__':
    """
    Usage: python merge.py ~/Desktop/video '00:09:04'
    """
    video_dir = './'
    clip_start = 0

    if len(sys.argv) > 1:
        video_dir = sys.argv[1]

        if len(sys.argv) > 2:
            clip_start = sys.argv[2]

        li = get_video_list(video_dir)

        merge(li, video_dir, clip_start)
    else:
        print("Usage: python merge.py ~/Desktop/video '00:09:04'")
