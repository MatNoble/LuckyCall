import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import random
import os
from datetime import datetime
from PIL import Image, ImageTk
from utils import get_ui_font, center_window, detect_file_encoding, BASE_DIR

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
        actual_encoding = detect_file_encoding(students_file)
        students_df = pd.read_csv(students_file, encoding=actual_encoding)
        print("文件读取成功。")

    except FileNotFoundError:
        print(f"错误：文件 '{students_file}' 未找到。")
        return
    except UnicodeDecodeError as e:
        print(f"读取文件失败，请检查编码。错误信息: {e}")
        return
    except Exception as e:
        print(f"读取文件时发生未知错误: {e}")
        return

    # 初始化记录文件
    if not os.path.exists(records_file):
        pd.DataFrame(columns=["时间", "学号", "姓名", "缺勤", "评语"]).to_csv(records_file, index=False, encoding="utf-8-sig")

    # GUI 主窗口
    root = tk.Tk()
    root.title(f"🎯 幸运点 LuckyCall")
    root.configure(bg="#f0f8ff")

    # 加载并显示 Logo
    logo_path = "./icon/school_logo.png"
    logo_image_tk = None
    if os.path.exists(logo_path):
        try:
            logo_image_pil = Image.open(logo_path)
            logo_image_pil = logo_image_pil.resize((150, 150), Image.Resampling.LANCZOS)
            logo_image_tk = ImageTk.PhotoImage(logo_image_pil)
            logo_label = tk.Label(root, image=logo_image_tk, bg="#f0f8ff")
            logo_label.image = logo_image_tk
            logo_label.place(x=40, y=20)
        except Exception as e:
            print(f"无法加载 Logo 图片: {e}")

    # 课程名称标签
    title_label = tk.Label(root, text=f"{course_name}", font=get_ui_font(20), fg="#1e90ff", bg="#f0f8ff")
    title_label.pack(pady=(80 if logo_image_tk else 40, 20))

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

        # 根据缺勤状态决定评语字段
        attendance_status = attendance_var.get()
        if attendance_status == "是":
            final_remark = ""
        else:
            final_remark = remark_var.get()

        record = {
            "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "学号": current_student["data"]["学号"],
            "姓名": current_student["data"]["姓名"],
            "缺勤": attendance_status,
            "评语": final_remark
        }
        df = pd.read_csv(records_file)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        df.to_csv(records_file, index=False, encoding="utf-8-sig")
        messagebox.showinfo("保存成功", f"{current_student['data']['姓名']} 的记录已保存！")
        update_stats()

    # 控制评语控件可见性的函数
    def toggle_remark_widgets():
        if attendance_var.get() == "是":
            remark_label.grid_remove()
            remark_menu.grid_remove()
        else:
            remark_label.grid()
            remark_menu.grid()

    # 创建单选按钮，并绑定到同一个变量和同一个回调函数
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

    # 统计信息
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