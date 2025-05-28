import os
import cv2
import numpy as np
from tqdm import tqdm

def adjust_brightness_saturation(image, brightness_factor=1.1, saturation_factor=1.2):
    """
    调整图像的亮度和饱和度
    
    参数:
    image: 输入图像 (OpenCV 格式, BGR)
    brightness_factor: 亮度调整因子，大于1增加亮度，小于1降低亮度
    saturation_factor: 饱和度调整因子，大于1增加饱和度，小于1降低饱和度
    
    返回:
    调整后的图像
    """
    # 转换为 HSV 色彩空间，更容易调整亮度和饱和度
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    
    # 调整亮度 (V 通道)
    hsv[:, :, 2] = hsv[:, :, 2] * brightness_factor
    hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
    
    # 调整饱和度 (S 通道)
    hsv[:, :, 1] = hsv[:, :, 1] * saturation_factor
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    
    # 转回 BGR 色彩空间
    adjusted_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    return adjusted_image

def process_images(input_folder, brightness_factor=1, saturation_factor=1.4):
    """
    处理文件夹中的所有图片
    
    参数:
    input_folder: 输入图片文件夹路径
    brightness_factor: 亮度调整因子
    saturation_factor: 饱和度调整因子
    """
    # 创建输出文件夹（在输入文件夹下创建一个enhanced子文件夹）
    output_folder = 'E:/waxberry/img_video_lw_en'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 获取所有图片文件
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"找到 {len(image_files)} 个图片文件在 {input_folder}")
    print(f"开始处理图片，亮度系数: {brightness_factor}, 饱和度系数: {saturation_factor}")
    
    # 使用tqdm显示进度条
    for image_file in tqdm(image_files):
        # 跳过enhanced文件夹内的文件
        if os.path.dirname(image_file) == output_folder:
            continue
            
        input_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, image_file)
        
        try:
            # 读取图片
            image = cv2.imread(input_path)
            
            if image is None:
                print(f"无法读取图片: {input_path}")
                continue
                
            # 调整亮度和饱和度
            adjusted_image = adjust_brightness_saturation(
                image, 
                brightness_factor=brightness_factor, 
                saturation_factor=saturation_factor
            )
            
            # 保存处理后的图片
            cv2.imwrite(output_path, adjusted_image)
            
        except Exception as e:
            print(f"处理 {image_file} 时出错: {str(e)}")
    
    print(f"处理完成! 增强后的图片已保存到: {output_folder}")

if __name__ == "__main__":
    # 设置输入文件夹路径
    input_folder = r"E:\waxberry\img_video_lw"
    
    # 处理图片，亮度为原来的1.1倍，饱和度为原来的1.2倍
    process_images(input_folder, brightness_factor=1, saturation_factor=1.4)