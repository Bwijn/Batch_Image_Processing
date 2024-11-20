import os
import json
from GifCompress import GifCompressor

# 读取配置文件
def load_config():
    with open('config.json', 'r', encoding='utf-8') as config_file:
        return json.load(config_file)

# 测试函数
def test_gif_compressor():
    config = load_config()

    # 定义变量
    MIN_COLOR_PALETTE = config['MIN_COLOR_PALETTE']
    MAX_SIZE_MB = config['MAX_SIZE_MB']
    MIN_FRAMES = config.get('MIN_FRAMES', 1)  # 假设 MIN_FRAMES 是可选的，默认值为 1
    WORK_PATH = config['work_path']
    OUTPUT_PATH = config['output_path']

    # 打印路径以检查它们是否正确
    print(f"工作路径: {WORK_PATH}")
    print(f"输出路径: {OUTPUT_PATH}")

    with Image.open(f"C:\Users\bwijn\Downloads\ImageAssistant_Batch_Image_Downloader\qunnes-shop.com\独立站\10005.gif") as img:

        return

    # 初始化 GifCompressor
    compressor = GifCompressor(WORK_PATH, OUTPUT_PATH)

    # 调用 compress_gif 方法
    compressor.compress_gif(MIN_COLOR_PALETTE, MAX_SIZE_MB, MIN_FRAMES)

if __name__ == "__main__":
    test_gif_compressor()