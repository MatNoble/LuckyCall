import tkinter as tk
from tkinter import ttk, messagebox
import os
from utils import get_ui_font, center_window
from random_selection import launch_main_app
from smart_attendance import launch_smart_attendance
from priority_management import manage_priority_students

def select_course():
    def confirm_selection():
        selected = course_var.get()
        mode = mode_var.get()
        if not selected:
            messagebox.showwarning("提示", "请选择一个课程班！")
            return
        root.destroy()
        if mode == "随机点名":
            launch_main_app(selected)
        else:
            launch_smart_attendance(selected)

    courses = [d for d in os.listdir("classes") if os.path.isdir(os.path.join("classes", d))]
    if not courses:
        messagebox.showerror("错误", f"请在 classes/ 下创建课程班文件夹，并放置 students.csv")
        return

    root = tk.Tk()
    root.title("选择课程班和模式")
    root.configure(bg="#f0f8ff")

    tk.Label(root, text="📚 请选择课程班：", font=get_ui_font(16), bg="#f0f8ff").pack(pady=10)

    course_var = tk.StringVar()
    course_menu = ttk.Combobox(
        root,
        textvariable=course_var,
        values=courses,
        state="readonly",
        font=get_ui_font(10, "normal"),
        width=30)

    course_menu.pack(pady=5)

    # 模式选择
    tk.Label(root, text="🎯 请选择模式：", font=get_ui_font(16), bg="#f0f8ff").pack(pady=10)

    mode_var = tk.StringVar(value="随机点名")
    mode_frame = tk.Frame(root, bg="#f0f8ff")
    mode_frame.pack(pady=5)

    ttk.Radiobutton(mode_frame, text="随机点名", variable=mode_var, value="随机点名").pack(side=tk.LEFT, padx=10)
    ttk.Radiobutton(mode_frame, text="智能考勤", variable=mode_var, value="智能考勤").pack(side=tk.LEFT, padx=10)

    # 管理重点名单按钮
    tk.Button(
        root,
        text="📝 管理重点名单",
        font=get_ui_font(12),
        bg="#ff9800",
        fg="white",
        activebackground="#f57c00",
        relief="flat",
        padx=15,
        pady=8,
        command=lambda: manage_priority_students(course_var.get())).pack(pady=5)

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
    center_window(root, 500, 380)

    root.mainloop()