import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import chardet
import random
import os
import platform
from datetime import datetime
from PIL import Image, ImageTk

# 跨平台字体设置
def get_ui_font(size=14, weight="bold"):
    system = platform.system()
    if system == "Windows":
        return ("Microsoft YaHei UI", size, weight)
    elif system == "Darwin":  # macOS
        return ("PingFang SC", size, weight)
    else:  # Linux / Ubuntu
        return ("fangsong ti", size, weight)

# 基础目录
BASE_DIR = "classes"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)
    
def center_window(root, width, height):
    # 获取屏幕宽高
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口大小和位置
    root.geometry(f"{width}x{height}+{x}+{y}")

# ---------- 第一步：课程选择界面 ----------
def select_course():
    def confirm_selection():
        selected = course_var.get()
        if not selected:
            messagebox.showwarning("提示", "请选择一个课程班！")
            return
        root.destroy()
        launch_main_app(selected)

    courses = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]
    if not courses:
        messagebox.showerror("错误", f"请在 {BASE_DIR}/ 下创建课程班文件夹，并放置 students.csv")
        return

    root = tk.Tk()
    root.title("选择课程班")
    root.configure(bg="#f0f8ff")

    tk.Label(root, text="📚 请选择课程班：", font=get_ui_font(16), bg="#f0f8ff").pack(pady=20)

    course_var = tk.StringVar()
    course_menu = ttk.Combobox(
        root,
        textvariable=course_var,
        values=courses,
        state="readonly",
        font=get_ui_font(10, "normal"),
        width=30)
    
    course_menu.pack(pady=10)

    tk.Button(
        root,
        text="确认",
        font=get_ui_font(14),
        bg="#4caf50",
        fg="white",
        activebackground="#388e3c",
        relief="flat",
        padx=20,
        pady=10,
        command=confirm_selection).pack(pady=10)
    
    # 调用居中函数
    center_window(root, 500, 309)

    root.mainloop()

# ---------- 第二步：主程序 ----------
def launch_main_app(course_name):
    course_dir = os.path.join(BASE_DIR, course_name)
    students_file = os.path.join(course_dir, "students.csv")
    records_file = os.path.join(course_dir, "records.csv")

    # 初始化学生数据
    if not os.path.exists(students_file):
        messagebox.showerror("错误", f"{course_name} 缺少 students.csv 文件")
        return
    
    # 使用 chardet 检测文件编码
    try:
        with open(students_file, 'rb') as f:
            # 读取文件前10000个字节进行检测，这通常足够了
            result = chardet.detect(f.read(10000))
            detected_encoding = result['encoding']
            print(f"检测到的文件编码为: {detected_encoding}")
    
        # 如果检测到 GB2312，则尝试使用 GBK
        if detected_encoding and detected_encoding.upper() == 'GB2312':
            actual_encoding = 'gbk'
        else:
            actual_encoding = detected_encoding
    
        # 使用最终确定的编码读取文件
        students_df = pd.read_csv(students_file, encoding=actual_encoding)
        print("文件读取成功。")
    
    except FileNotFoundError:
        print(f"错误：文件 '{students_file}' 未找到。")
    except UnicodeDecodeError as e:
        print(f"读取文件失败，请检查编码。错误信息: {e}")
    except Exception as e:
        print(f"读取文件时发生未知错误: {e}")

    # 初始化记录文件
    if not os.path.exists(records_file):
        pd.DataFrame(columns=["时间", "学号", "姓名", "缺勤", "评语"]).to_csv(records_file, index=False, encoding="utf-8-sig")

    # GUI 主窗口
    root = tk.Tk()
    root.title(f"🎯 幸运点 LuckyCall")
    root.configure(bg="#f0f8ff")

    # 加载并显示 Logo
    logo_path = "./icon/school_logo.png"  # 请确保这个文件和你的脚本在同一个目录下
    logo_image_tk = None # 初始化为 None
    if os.path.exists(logo_path):
        try:
            # 打开图片并调整大小
            logo_image_pil = Image.open(logo_path)
            logo_image_pil = logo_image_pil.resize((150, 150), Image.Resampling.LANCZOS)
            # 转换为 Tkinter 格式
            logo_image_tk = ImageTk.PhotoImage(logo_image_pil)
            # 创建一个 Label 控件来显示图片
            logo_label = tk.Label(root, image=logo_image_tk, bg="#f0f8ff")
            logo_label.image = logo_image_tk  # 保持对图片的引用
            # 使用 place 布局，固定在左上角
            logo_label.place(x=40, y=20) # 这里的 x 和 y 是像素坐标，可以根据需要调整
        except Exception as e:
            print(f"无法加载 Logo 图片: {e}")
            
    # 课程名称标签
    title_label = tk.Label(root, text=f"{course_name}", font=get_ui_font(20), fg="#1e90ff", bg="#f0f8ff")
    title_label.pack(pady=(80 if logo_image_tk else 40, 20)) # 根据是否有logo调整上边距

    # 显示选中学生
    student_var = tk.StringVar(value="谁会是幸运儿呢？")
    student_label = tk.Label(root, textvariable=student_var, font=get_ui_font(18), fg="#333", bg="#f0f8ff")
    student_label.pack(pady=20)

    # 状态选择
    status_frame = tk.Frame(root, bg="#f0f8ff")
    status_frame.pack(pady=10)
    status_label = tk.Label(status_frame, text="缺勤情况：", font=get_ui_font(12), bg="#f0f8ff")
    status_label.grid(row=0, column=0, padx=5)
    attendance_var = tk.StringVar(value="否")

    # 评语选择
    remark_frame = tk.Frame(root, bg="#f0f8ff")
    remark_frame.pack(pady=10)
    remark_label = tk.Label(remark_frame, text="评语：", font=get_ui_font(12), bg="#f0f8ff")
    remark_label.grid(row=0, column=0, padx=5)
    remark_var = tk.StringVar(value="合格")
    remarks = ["优秀", "良好", "合格", "需努力"]
    remark_menu = ttk.Combobox(remark_frame, textvariable=remark_var, values=remarks, state="readonly")
    remark_menu.grid(row=0, column=1, padx=5)

    # 随机点名逻辑
    current_student = {"data": None}
    rolling = {"active": False, "speed": 100, "stopping": False}
    recent_students = []  # 最近点过的学生，避免重复
    RECENT_LIMIT = 5      # 限制缓冲区大小，可调整

    def roll_names():
        if rolling["active"]:
            # 选人时避免重复
            idx = random.randint(0, len(students_df) - 1)
            candidate = students_df.iloc[idx]
            # 如果这个学生在最近列表中，重新抽
            while candidate["学号"] in recent_students and len(recent_students) < len(students_df):
                idx = random.randint(0, len(students_df) - 1)
                candidate = students_df.iloc[idx]

            current_student["data"] = candidate
            student_var.set(f"{candidate['学号']} - {candidate['姓名']}")

            # 控制速度
            delay = rolling["speed"]
            root.after(delay, roll_names)

            # 如果在停止阶段，逐渐加大 delay（速度变慢）
            if rolling["stopping"]:
                rolling["speed"] += 80  # 每次慢一点
                if rolling["speed"] > 800:  # 超过阈值就真正停止
                    rolling["active"] = False
                    rolling["stopping"] = False
                    rolling["speed"] = 100
                    # 加入最近点过的名单
                    recent_students.append(candidate["学号"])
                    if len(recent_students) > RECENT_LIMIT:
                        recent_students.pop(0)
                    # 弹窗结果
                    # messagebox.showinfo("结果", f"🎉 恭喜 {candidate['姓名']} 被选中！")
                    # 重置状态
                    attendance_var.set("否")
                    remark_var.set("合格")
                    toggle_remark_widgets()

    def start_roll():
        if not rolling["active"]:
            rolling["active"] = True
            rolling["stopping"] = False
            rolling["speed"] = 100
            roll_names()

    def stop_roll():
        if rolling["active"] and not rolling["stopping"]:
            rolling["stopping"] = True

    def save_record():
        if current_student["data"] is None:
            messagebox.showwarning("提示", "请先随机点名！")
            return
        
        # --- 修改点 2: 根据缺勤状态决定评语字段 ---
        attendance_status = attendance_var.get()
        if attendance_status == "是":
            # 如果缺勤，评语设为None或空字符串
            final_remark = ""
        else:
            final_remark = remark_var.get()

        record = {
            "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "学号": current_student["data"]["学号"],
            "姓名": current_student["data"]["姓名"],
            "缺勤": attendance_status,
            "评语": final_remark # 使用处理后的评语
        }
        df = pd.read_csv(records_file)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        # 将空值保存为NaN，再to_csv时会处理为空字符串
        df.to_csv(records_file, index=False, encoding="utf-8-sig")
        messagebox.showinfo("保存成功", f"{current_student['data']['姓名']} 的记录已保存！")
        update_stats()  # <<< 更新统计 & 进度条

    # 控制评语控件可见性的函数
    def toggle_remark_widgets():
        if attendance_var.get() == "是":
            # 如果缺勤，则隐藏评语标签和下拉框
            remark_label.grid_remove()
            remark_menu.grid_remove()
        else:
            # 否则显示
            remark_label.grid()
            remark_menu.grid()

    # 创建单选按钮，并绑定到同一个变量和同一个回调函数
    # 使用command参数，当单选按钮状态改变时，会调用toggle_remark_widgets函数
    ttk.Radiobutton(status_frame, text="否", variable=attendance_var, value="否", command=toggle_remark_widgets).grid(row=0, column=1, padx=5)
    ttk.Radiobutton(status_frame, text="是", variable=attendance_var, value="是", command=toggle_remark_widgets).grid(row=0, column=2, padx=5)
    
    # 按钮区
    btn_frame = tk.Frame(root, bg="#f0f8ff")
    btn_frame.pack(pady=20)

    start_button = tk.Button(btn_frame, text="▶ 开始", font=get_ui_font(14), bg="#4cafef", fg="white",
                             activebackground="#2196f3", relief="flat", padx=20, pady=10, command=start_roll)
    start_button.grid(row=0, column=0, padx=10)

    stop_button = tk.Button(btn_frame, text="⏹ 停止", font=get_ui_font(14), bg="#e91e63", fg="white",
                            activebackground="#c2185b", relief="flat", padx=20, pady=10, command=stop_roll)
    stop_button.grid(row=0, column=1, padx=10)

    save_button = tk.Button(btn_frame, text="💾 保存", font=get_ui_font(14), bg="#4caf50", fg="white",
                            activebackground="#388e3c", relief="flat", padx=20, pady=10, command=save_record)
    save_button.grid(row=0, column=2, padx=10)

    # --- 统计信息 ---
    stats_var = tk.StringVar()

    def update_stats():
        total_students = len(students_df)  # 总人数
        if os.path.exists(records_file):
            df = pd.read_csv(records_file)
            unique_called = df["学号"].nunique()  # 已点过人数
        else:
            unique_called = 0

        stats_var.set(f"📊 总人数: {total_students} | 已点过: {unique_called}")

        # 更新进度条
        progress_var.set(unique_called)
        progress_bar["maximum"] = total_students

    stats_label = tk.Label(root, textvariable=stats_var, font=get_ui_font(12), fg="#444", bg="#f0f8ff")
    stats_label.pack(pady=(10, 5))

    # 进度条
    progress_var = tk.IntVar(value=0)
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=1, length=300, mode="determinate")
    progress_bar.pack(pady=(0, 10))

    # 初始化时刷新一次
    update_stats()
    
    # 调用居中函数
    center_window(root, 900, 549)

    root.mainloop()

# ---------- 程序入口 ----------
if __name__ == "__main__":
    select_course()