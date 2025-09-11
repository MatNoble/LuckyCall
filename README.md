# 幸运点 LuckyCall
> 随机点名助手
> 该分支用于厦门大学嘉庚学院

## 说明
待完成...


## 使用方法
1. 生成课程班目录
  ```bash
  .
  ├── classes
  │   ├── 线性代数(A)(23机自)(3班)
  │   │   ├── records.csv
  │   │   └── students.csv
  │   └── 线性代数(A)(24电气)(3班)
  │       ├── records.csv
  │       └── students.csv
  ├── LuckyCall
  └── LuckyCall.exe
  ```

  其中，`LuckyCall` 和 `LuckyCall.exe` 分别为 Linux 和 Windows 的可执行文件，在同级目录下放至 `classes` 文件夹，下层放至以课程班名称为名的目录，每个课程班目录下需要 `students.csv`，需要至少包含 `学号` 和 `姓名` 两列。

2. 运行程序
  - Windows
    - 双击 `LuckyCall.exe`
    - CMD 中执行 `.\LuckyCall.exe`
  - Linux
    终端中执行 `./LuckyCall`
> 注：`LuckyCall` 和 `LuckyCall.exe` 为 `pyinstaller` 的打包从产物，位于 `dist` 目录下

## 功能说明
### 已完成功能:   
1. 选择课程班
2. 随机点名功能
3. 记录问题回答情况
4. 不需要额外的 Python 环境，支持可执行文件

### 待完善功能：
1. 屏蔽选择课程班的功能
2. 教务处名单自动化转化
  导出名单
3. 自动生成考勤表

## 开发指南

### 调试
```sh
# Windows
python lucky_call.py

# Linux
python3 lucky_call.py
```

### 打包命令
```sh
# Windows
pyinstaller --onefile --windowed --icon=icon\\lucky_call.ico lucky_call.py

# Linux
pyinstaller --onefile --windowed --icon=icon/lucky_call.ico lucky_call.py
```
