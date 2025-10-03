# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LuckyCall (幸运点) is a Python-based desktop application for classroom student random selection and attendance management, designed specifically for teachers at Xiamen University Tan Kah Kee College. The application uses Tkinter for GUI and provides two main modes: random student selection and attendance tracking, all without requiring student participation.

## Development Commands

### Running the Application
```bash
# Windows
python lucky_call.py

# Linux/macOS
python3 lucky_call.py
```

### Building Executables
```bash
# Windows (creates lucky_call.exe)
pyinstaller --onefile --windowed --icon=icon\\lucky_call.ico lucky_call.py

# Linux/macOS (creates lucky_call executable)
pyinstaller --onefile --windowed --icon=icon/lucky_call.ico lucky_call.py

# Alternative: Use the spec file
pyinstaller lucky_call.spec
```

### Testing
No automated tests are present. Manual testing involves:
1. Creating test class directories in `classes/` with `students.csv` files
2. Running the application and testing both random selection and attendance functionality
3. Verifying `records.csv` and `attendance.csv` generation

## Architecture Overview

### Single-File Application Structure
The entire application is contained in `lucky_call.py` with three main modes:

1. **Course Selection Phase** (`select_course()` function)
   - Scans `classes/` directory for subdirectories
   - Presents dropdown menu for class selection
   - Offers mode selection: "随机点名" (Random Selection) or "智能考勤" (Smart Attendance)
   - Provides access to priority student management
   - Validates that `students.csv` exists in selected class folder

2. **Random Selection Mode** (`launch_main_app()` function)
   - Loads student data from `classes/{class_name}/students.csv`
   - Creates GUI with random selection controls
   - Manages attendance tracking and performance recording
   - Writes records to `classes/{class_name}/records.csv`

3. **Smart Attendance Mode** (`launch_smart_attendance()` function)
   - Implements intelligent layered attendance system
   - Priority students (重点) are always included in attendance checks
   - Random sampling of regular students at configurable ratios (20-50%)
   - Saves detailed attendance records with timestamps and types
   - Supports flexible attendance timing (anytime during class)

### Data Flow Architecture
```
classes/
├── 班级一/
│   ├── students.csv (input: 学号, 姓名 columns)
│   ├── records.csv (output: random selection records)
│   ├── priority_students.csv (output: priority student list with reasons)
│   └── attendance_records.csv (output: smart attendance historical records)
└── 班级二/
    ├── students.csv (input)
    ├── records.csv (output)
    ├── priority_students.csv (output)
    └── attendance_records.csv (output)
```

### Key Features

#### Random Selection Mode
- Random student picker with start/stop controls
- Attendance tracking during selection (缺勤/出勤)
- Performance recording with remarks
- Statistics and progress tracking
- Recent selection history to avoid frequent repeats

#### Smart Attendance Mode
- Intelligent layered attendance system with priority students
- Priority students (重点) are always checked, regular students are randomly sampled
- Configurable sampling ratios (20%, 25%, 30%, 35%, 40%, 50%)
- Priority student management interface with CRUD operations
- Historical attendance records saved with timestamps and attendance types
- Real-time attendance statistics and completion tracking
- Flexible timing - can be initiated anytime during class
- Search functionality for priority student management
- Visual distinction between priority (red) and sampled (green) students

### Key Dependencies
- **tkinter**: GUI framework (Python standard library)
- **pandas**: CSV file processing
- **chardet**: Character encoding detection for CSV files
- **PIL (Pillow)**: Image handling for icons and logos
- **PyInstaller**: Executable packaging

### Cross-Platform Font Handling
The application includes platform-specific font configuration:
- Windows: Microsoft YaHei UI
- macOS: PingFang SC
- Linux: fangsong ti

### Data Format Requirements
- **students.csv**: Must contain `学号` (Student ID) and `姓名` (Name) columns
- **records.csv**: Automatically generated with interaction records (时间, 学号, 姓名, 缺勤, 评语)
- **priority_students.csv**: Manually managed priority student list (学号, 姓名, 原因, 添加时间)
- **attendance_records.csv**: Historical smart attendance records (考勤时间, 学号, 姓名, 出勤状态, 考勤类型)
- **Encoding**: Uses chardet for automatic encoding detection

## Important Notes

1. **Branch Context**: This is the TKK branch specifically for Xiamen University Tan Kah Kee College
2. **No Package Management**: No requirements.txt - dependencies must be installed manually
3. **Executable Distribution**: Pre-built executables provided in `example/` directory
4. **Data Privacy**: Student data is stored locally in CSV files within the `classes/` directory
5. **Student-Free Design**: No student participation required - all functionality is teacher-side
6. **Dual Mode Operation**: Teachers can switch between random selection and smart attendance modes
7. **Intelligent Attendance**: Smart attendance system reduces workload from 60-80 names to 20-30 targeted checks
8. **Priority Management**: Manual priority student management with CRUD operations for targeted attention
9. **Historical Records**: All attendance activities are timestamped and saved for semester-end review
10. **Flexible Timing**: Attendance can be initiated anytime during class, not restricted to start time