import os
from tkinter import Tk, Label, Entry, Button, filedialog, Text, StringVar, IntVar, messagebox
from PIL import Image, ImageOps
from GifCompress import GifCompressor # 假设 GifCompressor 类在 gif_compressor.py 文件中
import threading

import json
# 读取配置文件

def load_config():
    with open('config.json', 'r', encoding='utf-8') as config_file:
        return json.load(config_file)

# 保存配置文件
def save_config(config):
    with open('config.json', 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)

config = load_config()
# 定义变量
MIN_COLOR_PALETTE = config['MIN_COLOR_PALETTE']
MAX_SIZE_MB = config['MAX_SIZE_MB']
MIN_FRAMES = config.get('MIN_FRAMES', 1)  # 假设 MIN_FRAMES 是可选的，默认值为 1
WORK_PATH = config['work_path']
OUTPUT_PATH = config['output_path']
class TKGUI:
    def __init__(self, root):


        self.root = root
        self.root.title("图片处理工具")
       # 默认参数
        self.work_path = StringVar(value=WORK_PATH)
        self.output_path = StringVar(value=OUTPUT_PATH)
        self.MAX_SIZE_MB = IntVar(value=MAX_SIZE_MB)
        self.MIN_COLOR_PALETTE = IntVar(value=MIN_COLOR_PALETTE)
        self.MIN_FRAMES = IntVar(value=MIN_FRAMES)
        self.target_size = (750, 750)  # 目标大小
        self.background_color = "white"  # 背景色
        self.gif_compressor = GifCompressor(self,log_callback=self.log)
       # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # 创建 GUI
        self.create_widgets()
     # 这个方法启动一个新的线程来处理 GIF 压缩
    def on_closing(self):
        # 更新配置文件中的路径
        config['work_path'] = self.work_path.get()
        config['output_path'] = self.output_path.get()
        save_config(config)
        self.root.destroy()

    def compress_gif_in_thread(self, gif_path, output_path):
        self.gif_compressor.compress_gif(gif_path,output_path)
        # threading.Thread(target=self.gif_compressor.compress_gif,args=(gif_path,output_path) ).start()


    # 在多线程压缩操作中调用此日志方法
    # def process_gif(self):
    #     self.gif_compressor.compress_gif()

     
    def create_widgets(self):
        # 工作路径输入
        Label(self.root, text="工作路径:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        Entry(self.root, textvariable=self.work_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        Button(self.root, text="选择路径", command=self.choose_work_path).grid(row=0, column=2, padx=5, pady=5)

        # 输出路径输入
        Label(self.root, text="输出路径:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        Entry(self.root, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        Button(self.root, text="选择路径", command=self.choose_output_path).grid(row=1, column=2, padx=5, pady=5)

        # 最大 GIF 大小设置
        Label(self.root, text="最大 GIF 大小 (MB):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        Entry(self.root, textvariable=self.MAX_SIZE_MB, width=10).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # 最大 MIN_COLOR_PALETTE 大小设置
        Label(self.root, text="最小COLOR:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        Entry(self.root, textvariable=self.MIN_COLOR_PALETTE, width=10).grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # 输出框
        self.output_text = Text(self.root, height=15, width=60)
        self.output_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        # 开始按钮
        Button(self.root, text="开始处理", command=self.process_images).grid(row=5, column=0, columnspan=3, pady=10)

    def choose_work_path(self):
        path = filedialog.askdirectory()
        if path:
            self.work_path.set(path)

    def choose_output_path(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def log(self, message):
        """
        输出日志消息。
        :param message: 日志内容
        """
        self.output_text.insert("end", message + "\n")
        self.output_text.yview("end")

    def process_image(self, file_path, output_path_full):
        """
        处理单张图片，将其转换为指定大小和背景色。
        :param file_path: 输入文件路径
        :param output_path_full: 输出文件路径
        """
        try:
            with Image.open(file_path) as img:
                img = img.convert("RGB")  # 确保是 RGB 格式
                img_with_padding = ImageOps.pad(img, self.target_size, color=self.background_color, centering=(0.5, 0.5))
                img_with_padding.save(output_path_full, "JPEG")
                self.log(f"Processed {os.path.basename(file_path)} -> {os.path.basename(output_path_full)}")
        except Exception as e:
            self.log(f"处理文件 {os.path.basename(file_path)} 时出错: {e}")

    def process_images(self):
        """
        处理文件夹中的所有图片。
        """
        self.output_text.delete(1.0, "end")  # 清空输出框
        self.log(f"Processing images from {self.work_path.get()} to {self.output_path.get()}")
        
        # 获取输入路径和输出路径
        work_path = self.work_path.get()    
        output_path = self.output_path.get()
        
        if not os.path.exists(work_path):
            messagebox.showerror("错误", "工作路径不存在！")
            return
        if not os.path.exists(output_path):
            messagebox.showerror("错误", "输出路径不存在！")
            return
        
        # 处理所有图片
        file_prefix = "processed"
        for index, file_name in enumerate(os.listdir(work_path)):
            file_path = os.path.join(work_path, file_name)
            output_file = f"{file_prefix}_{index + 1:02d}.jpg"
            output_path_full = os.path.join(output_path, output_file)

            # 判断文件类型并处理
            if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                self.process_image(file_path, output_path_full)
            elif file_name.lower().endswith(".gif"):
                output_file = f"{file_prefix}_{index + 1:02d}.gif"
                output_path_full = os.path.join(output_path, output_file)
                # 调用 GifCompressor 类处理 GIF
                self.compress_gif_in_thread(file_path, output_path_full)
            else:
                self.log(f"跳过非图片文件: {file_name}")

# 启动 GUI
if __name__ == "__main__":
    root = Tk()
    app = TKGUI(root)
    root.mainloop()
