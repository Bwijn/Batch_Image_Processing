# gif_compressor.py
from PIL import Image, ImageSequence
import os
import json
import shutil
class GifCompressor:
    def __init__(self, tk_instance, log_callback=None):
        self.tk_instance = tk_instance
        self.log = log_callback        
    def get_original_palette_size(self, frame) -> int:
    # 获取原始调色板大小
        palette = frame.getpalette()
        unique_colors = len(set(tuple(palette[i:i+3]) for i in range(0, len(palette), 3)))
        return unique_colors
    def reduce_color_palette(self,frames, color_palette_size=64)->list:
        # 读取palette大小 然后减半
        original_palette_size = self.get_original_palette_size(frames[0])

        if original_palette_size >256:
            #报错 
            self.log(f"颜色表大小大于256，无法处理")
            return False
        original_palette_size = original_palette_size // 2
        #
        color_palette_size = self.tk_instance.MIN_COLOR_PALETTE.get()
        frames = [frame.convert("P", palette=Image.ADAPTIVE, colors=color_palette_size)   for frame in frames]
        
        return frames
    

    def reduce_frames(self,frames:list)->list:
                # 读取配置文件
        with open('config.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)

        # 定义变量
        MIN_COLOR_PALETTE = config['MIN_COLOR_PALETTE']
        MAX_SIZE_MB = config['MAX_SIZE_MB']
        MIN_FRAMES = self.tk_instance.MIN_FRAMES  # 假设 MIN_FRAMES 是可选的，默认值为 1
        if len(frames) > int(self.tk_instance.MIN_FRAMES.get()):
            frames = frames[::2]
        else:
            print("无法再删除帧，保留最小帧数。")
        return frames
    
    def compress_gif(self, gif_path:str, output_path:str):
        """
        压缩 GIF 文件至指定大小以内，同时尽量保留分辨率和视觉质量。
        
        :param input_path: 输入 GIF 文件路径
        :param output_path: 输出 GIF 文件路径
        """
                # 获取文件名和路径
        output_dir = os.path.dirname(output_path)
        output_file = os.path.basename(output_path)
        original_file = os.path.basename(gif_path)

        # 如果小于 self.tk_instance.MAX_SIZE_MB.get() MB，则不处理
        original_size_mb = os.path.getsize(gif_path) / (1024 * 1024)
        if original_size_mb <= self.tk_instance.MAX_SIZE_MB.get():
                # 只做重命名保存
            shutil.copy2(gif_path, output_path)
            self.log(f"{original_file} 文件大小已符合要求，无需处理 ->{output_file}")
            return

        with Image.open(gif_path) as img:

            frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
            frame_duration = img.info.get('duration', 100)  # 帧持续时间
            loop = img.info.get('loop', 0)  # GIF 循环次数
            

            # 初始颜色表大小
            # color_palette_size = 256


            # 读取配置文件
            with open('config.json', 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)

            # 定义变量
            MIN_COLOR_PALETTE = config['MIN_COLOR_PALETTE']
            MAX_SIZE_MB = self.tk_instance.MAX_SIZE_MB.get()
            MIN_FRAMES = self.tk_instance.MIN_FRAMES.get()  # 假设 MIN_FRAMES 是可选的，默认值为 1


        # 优先减少帧数（每次减半）
            frames = self.reduce_frames(frames)

            # 然后减少颜色表大小
            frames =self. reduce_color_palette(frames)
            if not frames:
                self.log(f"{original_file} 颜色超过256 ！")
            # 保存 GIF 并检查文件大小
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                format="GIF",
                loop=loop,
                duration=frame_duration,
                optimize=True,
            )
            current_size_mb = os.path.getsize(output_path) / (1024 * 1024)

            # 如果文件大小符合要求，退出循环
            if current_size_mb <= MAX_SIZE_MB:
                self.log(f"{original_file} GIF 压缩完成, {output_file} Size：{ current_size_mb:.2f} MB ->{output_file}")
                # print(f"GIF 压缩完成：{output_path} -> {current_size_mb:.2f} MB")
                # break
            else:
                
                self.log(f"{original_file} 压缩后没有符合 {self.tk_instance.MAX_SIZE_MB.get()} MB -> 压缩后：{current_size_mb:.2f} MB ->{output_file}"
                         ,highlight=True)
                
                # print(f"当前文件大小：{current_size_mb:.2f} MB")
            # 如果无法再优化，则停止并提醒
            
            if not frames or len(frames) <= MIN_FRAMES:
                self.log(f"{original_file} 已达到优化极限，但文件仍大于 {MAX_SIZE_MB} MB ->{output_file}")
                # print(f"已达到优化限制，但文件仍大于 {MAX_SIZE_MB} MB。")

        # except Exception as e:
        #     print(f"处理 GIF 时出错: {e}")
 