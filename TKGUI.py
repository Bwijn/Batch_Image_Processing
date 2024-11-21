import os
import sys
from tkinter import END, VERTICAL, Scrollbar, Tk, Label, Entry, Button, filedialog, Text, StringVar, IntVar, messagebox,Frame
from PIL import Image, ImageOps
from GifCompress import GifCompressor # 假设 GifCompressor 类在 gif_compressor.py 文件中
import threading

import json
# 读取配置文件

# def load_config():
#     with open(config_path, 'r') as config_file:
#         return  json.load(config_file)

# 保存配置文件
def save_config(config):
    with open('config.json', 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)


# def get_resource_path(filename):
#     """
#     获取资源文件的路径。
#     - 如果是打包环境（frozen），从临时目录加载。
#     - 如果是开发环境，使用脚本的目录。
#     """
#     if getattr(sys, 'frozen', False):  # 检查是否为打包状态
#         # 打包后的临时目录
#         return os.path.join(sys._MEIPASS, filename)
#     # 开发环境，直接从脚本目录加载
#     return os.path.join(os.path.dirname(__file__), filename)

with open("config.json", 'r',encoding='utf-8') as config_file:
    config = json.load(config_file) 
# 定义变量
MIN_COLOR_PALETTE = config['MIN_COLOR_PALETTE']
MAX_SIZE_MB = config['MAX_SIZE_MB']
MIN_FRAMES = config.get('MIN_FRAMES', 1)  # 假设 MIN_FRAMES 是可选的，默认值为 1
WORK_PATH = config['work_path']
OUTPUT_PATH = config['output_path']
class TKGUI:
    def __init__(self, root):


        self.root = root
        self.root.title("河南通瑞电子商务有限公司 内部专用 资源批处理Tools V1.0")
        # self.root.iconbitmap('icon.ico')  # 设置窗口图标
       # 默认参数
        self.work_path = StringVar(value=WORK_PATH)
        self.output_path = StringVar(value=OUTPUT_PATH)
        self.MAX_SIZE_MB = IntVar(value=MAX_SIZE_MB)
        self.MIN_COLOR_PALETTE = IntVar(value=MIN_COLOR_PALETTE)
        self.MIN_FRAMES = IntVar(value=MIN_FRAMES)
        self.file_prefix = StringVar(value="processed")
        
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
        config['MAX_SIZE_MB'] = self.MAX_SIZE_MB.get()
        config['MIN_COLOR_PALETTE'] = self.MIN_COLOR_PALETTE.get()
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
        Label(self.root, text="工作路径:").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        Entry(self.root, textvariable=self.work_path,).grid(sticky="ew", row=0, column=1, padx=5, pady=5)
        Button(self.root, text="选择路径", command=self.choose_work_path).grid(sticky="ew",row=0, column=2, padx=5, pady=5)
# 设置网格列权重
        self.root.grid_columnconfigure(0, weight=0)  # Label 不需要拉伸，权重为 0
        self.root.grid_columnconfigure(1, weight=1)  # Entry 扩展占据多余空间，权重为 1
        self.root.grid_columnconfigure(2, weight=0)  # Button 固定宽度，不拉伸

        # 输出路径输入
        Label(self.root, text="输出路径:").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        Entry(self.root, textvariable=self.output_path).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        Button(self.root, text="选择路径", command=self.choose_output_path).grid(row=1, column=2, sticky="ew", padx=5, pady=5)

        # 设置网格列权重
        self.root.grid_columnconfigure(0, weight=0)  # Label 不拉伸
        self.root.grid_columnconfigure(1, weight=1)  # Entry 占据多余空间
        self.root.grid_columnconfigure(2, weight=0)  # Button 固定宽度

        # 最大 GIF 大小设置
        Label(self.root, text="最大 GIF 大小 (MB):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        Entry(self.root, textvariable=self.MAX_SIZE_MB, width=10).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        # 最大 MIN_COLOR_PALETTE 大小设置
# 最小颜色调色板输入
        color_frame = Frame(self.root)
        color_frame.grid(row=3, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        Label(color_frame, text="GIF 调色板:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        Entry(color_frame, textvariable=self.MIN_COLOR_PALETTE, width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        Label(color_frame, text="必须 < 255 推荐64以下").grid(row=0, column=2, sticky="w", padx=5, pady=5)

        frame = Frame(self.root)
        frame.grid(row=4, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        Label(frame, text="文件前缀:").pack(side="left", padx=(0, 5))
        Entry(frame, textvariable=self.file_prefix, width=18).pack(side="left", padx=(0, 5))
        Label(frame, text="例如: hd2170  生成后为[ hd2170_(自动编号).(文件格式) ]").pack(side="left")



 # 输出框
        self.output_text = Text(self.root, height=15)
        self.output_text.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
   # 添加标签样式
        self.output_text.tag_configure("highlight", foreground="red", background="yellow")
        scrollbar = Scrollbar(self.root, command=self.output_text.yview, orient=VERTICAL)
        scrollbar.grid(row=5, column=3, sticky="ns")
        self.output_text.config(yscrollcommand=scrollbar.set)
        # 设置网格行和列权重
        self.root.grid_rowconfigure(5, weight=1)  # 第 5 行的 Text 控件随窗口垂直扩展
        # self.root.grid_columnconfigure(0, weight=1)  # 第 0 列的 Text 控件随窗口水平扩展
        # self.root.grid_columnconfigure(1, weight=1)  # 保证多列布局一致
        # self.root.grid_columnconfigure(2, weight=1)  # 同上


        # 开始按钮
        Button(self.root, text="开始处理", command=self.process_images).grid(row=6, column=0, columnspan=3, pady=10)

    def choose_work_path(self):
        path = filedialog.askdirectory()
        if path:
            self.work_path.set(path)

    def choose_output_path(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def log(self, message, highlight=False):
        if highlight:
            self.output_text.insert(END, message + "\n", "highlight")
        else:
            self.output_text.insert(END, message + "\n")
        self.output_text.see(END)

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
        #动态获取文件前缀from self.file_prefix
        file_prefix = self.file_prefix.get()
        for index, file_name in enumerate(os.listdir(work_path)):
            file_path = os.path.join(work_path, file_name)
            output_file = f"{file_prefix}_{index + 1:02d}.jpg"
            output_path_full = os.path.join(output_path, output_file)

            # 判断文件类型并处理
            if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                self.process_image(file_path, output_path_full)
            elif file_name.lower().endswith(".gif"):
                output_file = f"{file_prefix}_{index + 1:02d}.gif"
                output_path_full = os.path.join(output_path, output_file)
                # 调用 GifCompressor 类处理 GIF
                self.compress_gif_in_thread(file_path, output_path_full)
            else:
                self.log(f"跳过非图片文件: {file_name}")

def center_window(root, width=800, height=600):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')

# 启动 GUI
if __name__ == "__main__":
    root = Tk()
    center_window(root, 800, 600)  # 调用 center_window 函数将窗口居中
    app = TKGUI(root)
    root.mainloop()
