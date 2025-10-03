import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import random
import os
from datetime import datetime
from utils import get_ui_font, center_window, detect_file_encoding, BASE_DIR

def launch_smart_attendance(course_name):
    course_dir = os.path.join(BASE_DIR, course_name)
    students_file = os.path.join(course_dir, "students.csv")
    priority_file = os.path.join(course_dir, "priority_students.csv")
    attendance_records_file = os.path.join(course_dir, "attendance_records.csv")

    # 读取学生数据
    try:
        actual_encoding = detect_file_encoding(students_file)
        students_df = pd.read_csv(students_file, encoding=actual_encoding)
    except Exception as e:
        messagebox.showerror("错误", f"读取学生数据失败: {e}")
        return

    # 读取重点名单
    priority_students = set()
    if os.path.exists(priority_file):
        priority_df = pd.read_csv(priority_file)
        priority_students = set(priority_df["学号"].astype(str).tolist())

    # 初始化考勤记录文件
    if not os.path.exists(attendance_records_file):
        pd.DataFrame(columns=["考勤时间", "学号", "姓名", "出勤状态", "考勤类型"]).to_csv(attendance_records_file, index=False, encoding="utf-8-sig")

    # 创建考勤界面
    root = tk.Tk()
    root.title(f"🎯 智能考勤 - {course_name}")
    root.configure(bg="#f0f8ff")

    # 当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 标题区域
    title_frame = tk.Frame(root, bg="#f0f8ff")
    title_frame.pack(pady=10)

    tk.Label(title_frame, text=f"🎯 智能考勤", font=get_ui_font(20), bg="#f0f8ff", fg="#333").pack()
    tk.Label(title_frame, text=f"课程班: {course_name} | 时间: {current_time}", font=get_ui_font(12), bg="#f0f8ff", fg="#666").pack()

    # 配置区域
    config_frame = tk.Frame(root, bg="#f0f8ff")
    config_frame.pack(pady=10)

    tk.Label(config_frame, text="抽样比例:", font=get_ui_font(11), bg="#f0f8ff").pack(side=tk.LEFT, padx=5)
    sample_ratio_var = tk.StringVar(value="30%")
    sample_ratio_menu = ttk.Combobox(config_frame, textvariable=sample_ratio_var,
                                    values=["20%", "25%", "30%", "35%", "40%", "50%"],
                                    state="readonly", font=get_ui_font(10), width=8)
    sample_ratio_menu.pack(side=tk.LEFT, padx=5)

    # 考勤列表区域
    list_frame = tk.Frame(root, bg="#f0f8ff")
    list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # 创建Canvas和滚动条
    canvas = tk.Canvas(list_frame, bg="#f0f8ff", highlightthickness=0)
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f8ff")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 存储变量
    attendance_vars = {}
    current_attendance_list = []

    def generate_attendance_list():
        nonlocal current_attendance_list

        # 清空当前列表
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        attendance_vars.clear()

        # 获取抽样比例
        ratio_str = sample_ratio_var.get()
        ratio = int(ratio_str.replace("%", "")) / 100

        # 分离重点学生和普通学生
        priority_list = []
        normal_list = []

        for _, student in students_df.iterrows():
            student_id = str(student["学号"])
            student_name = str(student["姓名"])
            student_info = {"学号": student_id, "姓名": student_name}

            if student_id in priority_students:
                priority_list.append(student_info)
            else:
                normal_list.append(student_info)

        # 抽样普通学生
        sample_size = max(1, int(len(students_df) * ratio))
        priority_count = len(priority_list)
        normal_sample_size = max(0, sample_size - priority_count)

        # 确保重点学生全部包含，再从普通学生中抽样
        sampled_normal = random.sample(normal_list, min(normal_sample_size, len(normal_list)))
        current_attendance_list = priority_list + sampled_normal

        # 随机排序
        random.shuffle(current_attendance_list)

        # 创建表头
        header_frame = tk.Frame(scrollable_frame, bg="#e3f2fd", relief=tk.RAISED, bd=1)
        header_frame.pack(fill=tk.X, pady=2)

        tk.Label(header_frame, text="序号", font=get_ui_font(11, "bold"), bg="#e3f2fd", width=5).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="学号", font=get_ui_font(11, "bold"), bg="#e3f2fd", width=12).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="姓名", font=get_ui_font(11, "bold"), bg="#e3f2fd", width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="类型", font=get_ui_font(11, "bold"), bg="#e3f2fd", width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="出勤状态", font=get_ui_font(11, "bold"), bg="#e3f2fd", width=12).pack(side=tk.LEFT, padx=5)

        # 显示学生列表
        for i, student in enumerate(current_attendance_list, 1):
            student_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
            student_frame.pack(fill=tk.X, pady=1)

            tk.Label(student_frame, text=str(i), font=get_ui_font(10), bg="white", width=5).pack(side=tk.LEFT, padx=5)
            tk.Label(student_frame, text=student["学号"], font=get_ui_font(10), bg="white", width=12).pack(side=tk.LEFT, padx=5)
            tk.Label(student_frame, text=student["姓名"], font=get_ui_font(10), bg="white", width=10).pack(side=tk.LEFT, padx=5)

            # 类型标识
            student_type = "重点" if student["学号"] in priority_students else "抽样"
            type_color = "#ff5722" if student["学号"] in priority_students else "#4caf50"
            tk.Label(student_frame, text=student_type, font=get_ui_font(10, "bold"),
                    bg="white", fg=type_color, width=8).pack(side=tk.LEFT, padx=5)

            # 出勤状态选择
            attendance_vars[student["学号"]] = tk.StringVar(value="出勤")
            status_menu = ttk.Combobox(
                student_frame,
                textvariable=attendance_vars[student["学号"]],
                values=["出勤", "缺勤", "迟到", "请假"],
                state="readonly",
                font=get_ui_font(10, "normal"),
                width=8
            )
            status_menu.pack(side=tk.LEFT, padx=5)

    def save_attendance():
        if not current_attendance_list:
            messagebox.showwarning("提示", "请先生成考勤名单！")
            return

        # 准备考勤数据
        attendance_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attendance_data = []

        for student in current_attendance_list:
            student_id = student["学号"]
            student_name = student["姓名"]
            status = attendance_vars[student_id].get()
            attendance_type = "重点" if student_id in priority_students else "抽样"

            attendance_data.append({
                "考勤时间": attendance_time,
                "学号": student_id,
                "姓名": student_name,
                "出勤状态": status,
                "考勤类型": attendance_type
            })

        # 读取现有记录并添加新记录
        try:
            if os.path.exists(attendance_records_file):
                existing_df = pd.read_csv(attendance_records_file)
                combined_df = pd.concat([existing_df, pd.DataFrame(attendance_data)], ignore_index=True)
            else:
                combined_df = pd.DataFrame(attendance_data)

            combined_df.to_csv(attendance_records_file, index=False, encoding="utf-8-sig")

            # 统计信息
            total_count = len(attendance_data)
            absence_count = sum(1 for data in attendance_data if data["出勤状态"] == "缺勤")

            messagebox.showinfo("保存成功",
                              f"考勤数据已保存！\n"
                              f"本次考勤: {total_count}人\n"
                              f"缺勤: {absence_count}人\n"
                              f"到课率: {((total_count-absence_count)/total_count*100):.1f}%")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存考勤数据时出错: {e}")

    # 按钮区域
    button_frame = tk.Frame(root, bg="#f0f8ff")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="🎲 生成考勤名单", font=get_ui_font(12), bg="#2196f3", fg="white",
              command=generate_attendance_list).pack(side=tk.LEFT, padx=5)

    tk.Button(button_frame, text="💾 保存考勤结果", font=get_ui_font(12), bg="#4caf50", fg="white",
              command=save_attendance).pack(side=tk.LEFT, padx=5)

    # 打包Canvas和滚动条
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 初始提示
    tk.Label(scrollable_frame, text="点击下方按钮生成考勤名单", font=get_ui_font(12),
             bg="#f0f8ff", fg="#666").pack(pady=50)

    # 调用居中函数
    center_window(root, 800, 600)

    root.mainloop()