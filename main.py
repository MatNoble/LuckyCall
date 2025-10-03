#!/usr/bin/env python3
"""
LuckyCall (幸运点) - 课堂学生随机选择和考勤管理系统
主入口文件

作者：Claude Code
用途：厦门大学漳州校区课堂随机点名和智能考勤
"""

from course_selection import select_course

def main():
    """主函数 - 启动应用程序"""
    select_course()

if __name__ == "__main__":
    main()