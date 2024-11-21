# 水印去除工具

## 项目简介

本项目是一个基于 Python 和 PyQt5 的水印去除工具，可以处理 PDF 和 Word 文件中的水印。支持快速和深度两种模式，用户可以通过直观的图形用户界面（GUI）选择文件并执行水印去除操作。

---

## 功能特点

- **支持文件类型：**
  - PDF 文件
  - Word 文件（.docx 格式）
  
- **水印去除模式：**
  - **快速去除**：针对简单水印，处理速度快。
  - **深度去除**：针对复杂水印，处理较为全面。

- **批量处理：**
  - 一次加载多个文件
  - 支持多文件并行处理

- **易用的界面：**
  - 文件选择、全选/取消全选功能
  - 文件状态实时更新
  - 进度条显示处理进度
  - 提示处理预计完成时间

---

## 安装步骤

### 系统要求

- 操作系统：macOS 或 Windows
- Python 版本：3.9 或以上

### 安装依赖

1. 确保已安装 Python 和 pip。
2. 使用以下命令安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 运行程序

在终端中运行以下命令：

```bash
python prod.py
```

## 项目结构
.
├── prod.py                # 主程序
├── removerPdf.py          # PDF 文件水印去除逻辑
├── removerWord.py         # Word 文件水印去除逻辑
├── requirements.txt       # 项目依赖文件
└── README.md              # 项目说明文件

---

## 特别鸣谢

在此特别感谢以下开源库的作者和贡献者：

- [PyPDF2](https://pypdf2.readthedocs.io/en/latest/)
- [python-docx](https://python-docx.readthedocs.io/en/latest/)
- [pdf2image](https://github.com/Belval/pdf2image)
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
- [PyQt5](https://riverbankcomputing.com/software/pyqt/intro)
- [NumPy](https://numpy.org/)
- [OpenCV](https://opencv.org/)
- [Pillow](https://python-pillow.org/)
- [scikit-image](https://scikit-image.org/)

---

## 联系我们

如有问题或建议，请随时提交 [Issue](https://github.com/ZingZing001/WaterMarkRemoverTool/issues) 或通过邮箱与我们联系：

- 邮箱：runjiazhang.nz@gmail.com