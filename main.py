import cv2
import os
import argparse
from tqdm import tqdm

class JPGVideoFrameExtractor:
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    
    def extract_frames(self, video_path, output_dir, frame_interval=1, 
                      target_fps=None, max_frames=None, jpg_quality=95):
        """
        JPG格式视频分帧提取器
        
        参数:
        video_path: 视频文件路径
        output_dir: 输出目录
        frame_interval: 帧间隔
        target_fps: 目标帧率（如果设置，会覆盖frame_interval）
        max_frames: 最大提取帧数
        jpg_quality: JPG图片质量（1-100），默认95
        """
        # 检查视频文件
        if not os.path.exists(video_path):
            print(f"错误：视频文件不存在 - {video_path}")
            return False
        
        # 验证JPG质量参数
        if jpg_quality < 1 or jpg_quality > 100:
            print("警告：JPG质量参数应在1-100之间，使用默认值95")
            jpg_quality = 95
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 打开视频
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("错误：无法打开视频文件")
            return False
        
        # 获取视频信息
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"视频信息：")
        print(f"  - 分辨率: {width} x {height}")
        print(f"  - 原始帧率: {original_fps:.2f} FPS")
        print(f"  - 总帧数: {total_frames}")
        print(f"  - 时长: {total_frames/original_fps:.2f} 秒")
        print(f"  - 输出格式: JPG (质量: {jpg_quality})")
        
        # 计算实际帧间隔
        if target_fps and target_fps < original_fps:
            frame_interval = max(1, int(original_fps / target_fps))
        
        estimated_frames = total_frames // frame_interval
        if max_frames:
            estimated_frames = min(estimated_frames, max_frames)
        
        print(f"提取设置：")
        print(f"  - 帧间隔: {frame_interval}")
        print(f"  - 预计提取帧数: {estimated_frames}")
        
        # JPG压缩参数
        jpg_params = [cv2.IMWRITE_JPEG_QUALITY, jpg_quality]
        
        frame_count = 0
        saved_count = 0
        
        # 使用进度条
        pbar = tqdm(total=estimated_frames, desc="提取JPG帧")
        
        while True:
            ret, frame = cap.read()
            
            if not ret or (max_frames and saved_count >= max_frames):
                break
            
            if frame_count % frame_interval == 0:
                # 生成JPG文件名
                filename = f"frame_{saved_count:06d}.jpg"
                filepath = os.path.join(output_dir, filename)
                
                # 保存为JPG图片
                cv2.imwrite(filepath, frame, jpg_params)
                
                saved_count += 1
                pbar.update(1)
            
            frame_count += 1
        
        pbar.close()
        cap.release()
        
        print(f"\nJPG分帧完成！")
        print(f"实际保存帧数: {saved_count}")
        print(f"输出目录: {output_dir}")
        return True
    
    def extract_by_time_intervals(self, video_path, output_dir, interval_seconds=1, jpg_quality=95):
        """
        按时间间隔提取JPG帧
        
        参数:
        video_path: 视频路径
        output_dir: 输出目录
        interval_seconds: 时间间隔（秒）
        jpg_quality: JPG质量
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("错误：无法打开视频文件")
            return False
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = max(1, int(fps * interval_seconds))
        
        return self.extract_frames(video_path, output_dir, frame_interval, 
                                 jpg_quality=jpg_quality)

def main():
    parser = argparse.ArgumentParser(description='JPG格式视频分帧工具')
    parser.add_argument('video_path', help='视频文件路径')
    parser.add_argument('-o', '--output', default='jpg_frames', help='输出目录')
    parser.add_argument('-i', '--interval', type=int, default=1, help='帧间隔')
    parser.add_argument('--fps', type=float, help='目标帧率')
    parser.add_argument('--max-frames', type=int, help='最大提取帧数')
    parser.add_argument('-q', '--quality', type=int, default=95, 
                       help='JPG图片质量 (1-100，默认95)')
    
    args = parser.parse_args()
    
    extractor = JPGVideoFrameExtractor()
    extractor.extract_frames(
        video_path=args.video_path,
        output_dir=args.output,
        frame_interval=args.interval,
        target_fps=args.fps,
        max_frames=args.max_frames,
        jpg_quality=args.quality
    )

if __name__ == "__main__":
    # 创建提取器实例
    extractor = JPGVideoFrameExtractor()

    extractor.extract_frames("Video_20251103164935468.avi", "jpg_frames_limited", 
                           max_frames=17, jpg_quality=90)