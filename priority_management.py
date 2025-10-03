import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime
from utils import get_ui_font, center_window, detect_file_encoding, BASE_DIR

def manage_priority_students(course_name):
    if not course_name:
        messagebox.showwarning("提示", "请先选择一个课程班！")
        return

    course_dir = os.path.join(BASE_DIR, course_name)
    priority_file = os.path.join(course_dir, "priority_students.csv")
    students_file = os.path.join(course_dir, "students.csv")

    # 读取学生数据
    try:
        actual_encoding = detect_file_encoding(students_file)
        students_df = pd.read_csv(students_file, encoding=actual_encoding)
    except Exception as e:
        messagebox.showerror("错误", f"读取学生数据失败: {e}")
        return

    # 初始化重点名单文件
    if not os.path.exists(priority_file):
        pd.DataFrame(columns=["学号", "姓名", "原因", "添加时间"]).to_csv(priority_file, index=False, encoding="utf-8-sig")

    # 读取现有重点名单
    priority_df = pd.read_csv(priority_file)

    # 创建管理界面
    root = tk.Tk()
    root.title(f"📝 重点名单管理 - {course_name}")
    root.configure(bg="#f0f8ff")

    # 标题
    tk.Label(root, text=f"📝 重点名单管理", font=get_ui_font(18), bg="#f0f8ff", fg="#333").pack(pady=10)
    tk.Label(root, text=f"课程班: {course_name}", font=get_ui_font(12), bg="#f0f8ff", fg="#666").pack()

    # 搜索和添加区域
    search_frame = tk.Frame(root, bg="#f0f8ff")
    search_frame.pack(pady=10, padx=20)

    tk.Label(search_frame, text="🔍 搜索学生:", font=get_ui_font(11), bg="#f0f8ff").pack(side=tk.LEFT, padx=5)
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=get_ui_font(11), width=20)
    search_entry.pack(side=tk.LEFT, padx=5)

    # 学生列表框架
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
    selected_students = set(priority_df["学号"].astype(str).tolist())
    reason_vars = {}

    def update_student_list():
        # 清空现有列表
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # 获取搜索关键词
        search_term = search_var.get().lower()

        # 创建表头
        header_frame = tk.Frame(scrollable_frame, bg="#e3f2fd", relief=tk.RAISED, bd=1)
        header_frame.pack(fill=tk.X, pady=2)

        tk.Label(header_frame, text="选择", font=get_ui_font(11, "bold"), bg="#e3f2fd", width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="学号", font=get_ui_font(11, "bold"), bg="#e3f2fd", width=12).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="姓名", font=get_ui_font(11, "bold"), bg="#e3f2fd", width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="原因", font=get_ui_font(11, "bold"), bg="#e3f2fd", width=20).pack(side=tk.LEFT, padx=5)

        # 显示学生列表
        for _, student in students_df.iterrows():
            student_id = str(student["学号"])
            student_name = str(student["姓名"])

            # 搜索过滤
            if search_term and search_term not in student_id.lower() and search_term not in student_name.lower():
                continue

            student_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
            student_frame.pack(fill=tk.X, pady=1)

            # 选择复选框
            var = tk.BooleanVar(value=student_id in selected_students)
            tk.Checkbutton(student_frame, variable=var,
                          command=lambda sid=student_id, v=var: toggle_student(sid, v),
                          bg="white").pack(side=tk.LEFT, padx=5)

            tk.Label(student_frame, text=student_id, font=get_ui_font(10), bg="white", width=12).pack(side=tk.LEFT, padx=5)
            tk.Label(student_frame, text=student_name, font=get_ui_font(10), bg="white", width=10).pack(side=tk.LEFT, padx=5)

            # 原因输入框
            if student_id not in reason_vars:
                existing_reason = ""
                if student_id in priority_df["学号"].astype(str).values:
                    existing_reason = priority_df[priority_df["学号"].astype(str) == student_id]["原因"].iloc[0]
                reason_vars[student_id] = tk.StringVar(value=existing_reason)

            reason_entry = tk.Entry(student_frame, textvariable=reason_vars[student_id],
                                  font=get_ui_font(10, "normal"), width=25)
            reason_entry.pack(side=tk.LEFT, padx=5)

    def toggle_student(student_id, var):
        if var.get():
            selected_students.add(student_id)
        else:
            selected_students.discard(student_id)

    def save_priority_list():
        # 准备数据
        priority_data = []
        for student_id in selected_students:
            student_name = students_df[students_df["学号"] == int(student_id)]["姓名"].iloc[0]
            reason = reason_vars.get(student_id, tk.StringVar()).get()
            priority_data.append({
                "学号": student_id,
                "姓名": student_name,
                "原因": reason,
                "添加时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        # 保存到文件
        new_df = pd.DataFrame(priority_data)
        new_df.to_csv(priority_file, index=False, encoding="utf-8-sig")

        messagebox.showinfo("保存成功", f"重点名单已保存！共 {len(selected_students)} 名学生")
        root.destroy()

    # 按钮区域
    button_frame = tk.Frame(root, bg="#f0f8ff")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="💾 保存", font=get_ui_font(12), bg="#4caf50", fg="white",
              command=save_priority_list).pack(side=tk.LEFT, padx=5)

    tk.Button(button_frame, text="🔄 刷新", font=get_ui_font(12), bg="#2196f3", fg="white",
              command=update_student_list).pack(side=tk.LEFT, padx=5)

    # 绑定搜索功能
    search_var.trace("w", lambda *args: update_student_list())

    # 打包Canvas和滚动条
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 初始化学生列表
    update_student_list()

    # 调用居中函数
    center_window(root, 700, 500)

    root.mainloop()