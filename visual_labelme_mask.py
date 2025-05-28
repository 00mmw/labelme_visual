import os
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from PIL import Image

def visualize_labelme_json(json_file, img_file=None):
    """
    可视化LabelMe JSON文件的标注
    
    参数:
    json_file: LabelMe JSON文件路径
    img_file: 图像文件路径（如果为None，则从JSON文件中读取）
    
    返回:
    无，直接显示可视化结果
    """
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 如果没有提供图像路径，则从JSON中获取
    if img_file is None:
        img_file = os.path.join(os.path.dirname(os.path.dirname(json_file)), 
                               data.get('imagePath', '').replace('..\\', ''))
    
    # 确保图像文件存在
    if not os.path.exists(img_file):
        print(f"错误：找不到图像文件 {img_file}")
        return
    
    # 读取图像
    img = cv2.imread(img_file)
    if img is None:
        print(f"错误：无法读取图像 {img_file}")
        return
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 创建与原图相同大小的空白掩码图像
    height, width = img.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # 处理shapes数组中的标注
    has_mask = False
    shapes = data.get('shapes', [])
    if shapes:
        print(f"处理 {len(shapes)} 个标注形状...")
        for shape in shapes:
            label = shape.get('label', 'unknown')
            shape_type = shape.get('shape_type', '')
            
            if shape_type == 'polygon':
                points = np.array(shape.get('points', []), dtype=np.int32)
                cv2.fillPoly(mask, [points], 255)
                has_mask = True
            
            elif shape_type == 'rectangle':
                points = np.array(shape.get('points', []), dtype=np.int32)
                pt1, pt2 = points
                cv2.rectangle(mask, tuple(pt1.astype(int)), tuple(pt2.astype(int)), 255, -1)
                has_mask = True
            
            elif shape_type == 'mask':
                # 处理mask类型的标注
                if 'mask' in shape:
                    try:
                        # 解码base64数据
                        mask_data = base64.b64decode(shape['mask'])
                        mask_img = Image.open(BytesIO(mask_data))
                        shape_mask = np.array(mask_img)
                        
                        # 如果掩码是RGB格式，转换为灰度
                        if len(shape_mask.shape) == 3:
                            shape_mask = cv2.cvtColor(shape_mask, cv2.COLOR_RGB2GRAY)
                        
                        # 确保掩码是二值的
                        shape_mask = (shape_mask > 0).astype(np.uint8) * 255
                        
                        # 获取标注的位置信息
                        points = shape.get('points', [])
                        if len(points) == 2:
                            x1, y1 = map(int, points[0])
                            x2, y2 = map(int, points[1])
                            
                            # 调整形状以适应mask尺寸
                            mask_h, mask_w = shape_mask.shape[:2]
                            
                            # 在原始mask中放置shape_mask
                            # 确保坐标在有效范围内
                            x1 = max(0, x1)
                            y1 = max(0, y1)
                            x2 = min(width, x2)
                            y2 = min(height, y2)
                            
                            # 调整mask尺寸以适应目标区域
                            target_h = y2 - y1
                            target_w = x2 - x1
                            
                            if target_h > 0 and target_w > 0:
                                resized_mask = cv2.resize(shape_mask, (target_w, target_h))
                                mask[y1:y2, x1:x2] = np.maximum(mask[y1:y2, x1:x2], resized_mask)
                                has_mask = True
                        else:
                            print(f"警告：mask类型标注的points数量不正确：{len(points)}")
                    except Exception as e:
                        print(f"解码mask数据时出错: {str(e)}")
    
    # 检查是否成功生成了掩码
    if not has_mask:
        print("警告：未能生成掩码。JSON文件可能没有有效的标注数据。")
    else:
        print(f"成功生成掩码，掩码中的最大值为: {np.max(mask)}")
    
    # 创建彩色掩码用于可视化
    color_mask = np.zeros((height, width, 3), dtype=np.uint8)
    color_mask[mask > 0] = [255, 0, 0]  # 红色掩码
    
    # 将掩码叠加到原图上
    alpha = 0.5
    overlay = cv2.addWeighted(img, 1, color_mask, alpha, 0)
    
    # 显示结果
    plt.figure(figsize=(15, 5))
    
    plt.subplot(131)
    plt.title('原始图像')
    plt.imshow(img)
    plt.axis('off')
    
    plt.subplot(132)
    plt.title('掩码')
    plt.imshow(mask, cmap='gray')
    plt.axis('off')
    
    plt.subplot(133)
    plt.title('叠加结果')
    plt.imshow(overlay)
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print(f"可视化完成: {json_file}")

def list_json_files(directory):
    """列出目录中的所有JSON文件"""
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

if __name__ == "__main__":
    # 使用示例
    json_file = r"E:\waxberry\img\mask_json\IMG_20250527_090401.json"
    img_file = r"E:\waxberry\img\IMG_20250527_090401.jpg"
    
    # 检查文件是否存在
    if not os.path.exists(json_file):
        print(f"错误：JSON文件 {json_file} 不存在")
        
        # 尝试在mask_json目录中查找其他JSON文件
        mask_dir = r"E:\waxberry\img\mask_json"
        if os.path.exists(mask_dir):
            json_files = list_json_files(mask_dir)
            if json_files:
                print(f"在 {mask_dir} 中找到了 {len(json_files)} 个JSON文件:")
                for i, f in enumerate(json_files):
                    print(f"{i+1}. {os.path.basename(f)}")
                print("请修改代码中的文件路径以使用其中一个文件")
            else:
                print(f"在 {mask_dir} 中没有找到JSON文件")
    else:
        # 检查图像文件是否存在
        if not os.path.exists(img_file):
            print(f"错误：图像文件 {img_file} 不存在")
        else:
            visualize_labelme_json(json_file, img_file)
