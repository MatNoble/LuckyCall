import platform
import chardet
import os

# 跨平台字体设置
def get_ui_font(size=14, weight="bold"):
    system = platform.system()
    if system == "Windows":
        return ("Microsoft YaHei UI", size, weight)
    elif system == "Darwin":  # macOS
        return ("PingFang SC", size, weight)
    else:  # Linux / Ubuntu
        return ("fangsong ti", size, weight)

def center_window(root, width, height):
    """居中窗口"""
    # 获取屏幕宽高
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口大小和位置
    root.geometry(f"{width}x{height}+{x}+{y}")

def detect_file_encoding(file_path):
    """检测文件编码"""
    try:
        with open(file_path, 'rb') as f:
            # 读取文件前10000个字节进行检测，这通常足够了
            result = chardet.detect(f.read(10000))
            detected_encoding = result['encoding']

            # 如果检测到 GB2312，则尝试使用 GBK
            if detected_encoding and detected_encoding.upper() == 'GB2312':
                actual_encoding = 'gbk'
            else:
                actual_encoding = detected_encoding

            return actual_encoding
    except Exception as e:
        print(f"检测文件编码时出错: {e}")
        return 'utf-8'  # 默认返回utf-8

# 基础目录
BASE_DIR = "classes"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)