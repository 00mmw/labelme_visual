import os
import cv2
import glob
from pathlib import Path

def extract_frames(video_path, output_dir, frame_interval=1):
    """
    从视频中提取帧并保存为JPG图像
    
    参数:
        video_path: 视频文件路径
        output_dir: 输出图像的目录
        frame_interval: 每隔多少帧提取一次，默认为1（提取所有帧）
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取视频文件名（不含扩展名）
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"错误: 无法打开视频 {video_path}")
        return
    
    # 获取视频的总帧数
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 获取视频宽高
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"处理视频: {video_path}")
    print(f"总帧数: {total_frames}")
    print(f"视频尺寸: {width}x{height}")
    
    # 读取并保存帧
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            # 根据从截图中看到的情况，强制将横向图像旋转为竖向
            # 检查当前帧的宽高比
            frame_height, frame_width = frame.shape[:2]
            
            # 如果是横向图像(宽>高)，需要旋转为竖向
            if frame_width > frame_height:
                # 逆时针旋转90度
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                print(f"帧 {frame_count}: 旋转图像从横向到竖向") if frame_count == 0 else None
            
            # 生成带有6位数字的文件名，例如: VID_20250527_090504_000001.jpg
            output_filename = f"{video_name}_{saved_count:06d}.jpg"
            output_path = os.path.join(output_dir, output_filename)
            
            # 保存图像
            cv2.imwrite(output_path, frame)
            saved_count += 1
            
            # 打印进度
            if saved_count % 100 == 0:
                print(f"已保存 {saved_count} 张图像...")
        
        frame_count += 1
    
    # 释放资源
    cap.release()
    print(f"完成! 共保存了 {saved_count} 张图像")

def process_all_videos(video_dir, output_dir, frame_interval=1):
    """
    处理指定目录中的所有视频文件
    
    参数:
        video_dir: 视频文件所在的目录
        output_dir: 输出图像的目录
        frame_interval: 每隔多少帧提取一次
    """
    # 支持的视频格式
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.MOV']
    
    # 获取所有视频文件
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(video_dir, f"*{ext}")))
    
    if not video_files:
        print(f"在 {video_dir} 中没有找到视频文件")
        return
    
    print(f"找到 {len(video_files)} 个视频文件")
    
    # 处理每个视频文件
    for video_path in video_files:
        extract_frames(video_path, output_dir, frame_interval)

if __name__ == "__main__":
    # 定义视频目录和输出目录
    video_directory = r"E:\waxberry\try"
    output_directory = r"E:\waxberry\img_vedio"
    
    # 每3帧提取一帧，可以根据需要调整
    frame_interval = 1
    
    # 处理所有视频
    process_all_videos(video_directory, output_directory, frame_interval)