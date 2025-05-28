#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图片旋转程序：将 E:\waxberry\img_shikuang 目录中的所有图片顺时针旋转180度
"""

import os
from PIL import Image

def rotate_images(source_dir):
    """
    将指定目录中的所有图片顺时针旋转180度并保存
    
    Args:
        source_dir: 源图片目录路径
    """
    # 确保目录存在
    if not os.path.exists(source_dir):
        print(f"错误：目录 {source_dir} 不存在！")
        return
    
    # 获取目录中的所有文件
    file_list = os.listdir(source_dir)
    image_count = 0
    error_count = 0
    
    print(f"开始处理 {source_dir} 中的图片...")
    
    # 遍历所有文件
    for filename in file_list:
        file_path = os.path.join(source_dir, filename)
        
        # 检查文件是否为图片（通过扩展名简单判断）
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            try:
                # 打开图片
                with Image.open(file_path) as img:
                    # 顺时针旋转180度
                    rotated_img = img.rotate(180)
                    
                    # 保存旋转后的图片（覆盖原图片）
                    rotated_img.save(file_path)
                    
                    image_count += 1
                    print(f"已处理: {filename}")
            except Exception as e:
                print(f"处理 {filename} 时出错: {str(e)}")
                error_count += 1
    
    print(f"\n处理完成！共处理 {image_count} 张图片，失败 {error_count} 张。")

if __name__ == "__main__":
    # 指定图片所在目录
    image_dir = r"E:\waxberry\img_vedio"
    
    # 执行旋转操作
    rotate_images(image_dir)