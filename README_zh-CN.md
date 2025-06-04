# 水印移除工具

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
<!-- language -->

[English](README.md) | [简体中文](README_zh-CN.md)

如果您觉得这个工具有用，请给我一个星星支持吧！🌟  
求求留个星星呗🥺🌟

---

一个功能强大且用户友好的工具，用于从 PDF 和 Word 文档中移除水印。该应用程序提供快速移除和深度移除模式，可针对各种水印类型确保最佳效果。

我已经放出了一个可直接运行程序在[Release](https://github.com/ZingZing001/WaterMarkRemovalTool/releases)，请确保poppler可以在您的系统里运行。

注意⚠️：Windows 系统需要装Linux VM，在Linux环境下使用。（因为Poppler-Utils 现已不支持Windows）
---

## 功能

- **快速移除：** 快速从 PDF 文件中移除基于层的水印。
- **深度移除：** 结合高级图像处理技术，移除文本和图像类型的水印。
- **支持 Word 文件：** 移除 `.docx` 文件中的水印。
- **批量处理：** 一次加载多个文件并批量处理。
- **可定制模式：** 提供“快速移除”和“深度移除”两种模式选择。
- **进度跟踪：** 提供可视化进度条和预计完成时间。
- **跨平台支持：** 支持 Windows、macOS 和 Linux。

---

## 前置条件

确保您已安装 Python 3.9 或更高版本。此外，请安装 `requirements.txt` 中列出的依赖项。

---

## 安装

1. 克隆此代码仓库：
    ```bash
    git clone https://github.com/yourusername/watermark-remover.git
    cd watermark-remover
    ```

2. 安装依赖项：
    ```bash
    pip install -r requirements.txt
    ```

3. 安装 Poppler 以支持 PDF 处理：
    - **macOS:**
        ```bash
        brew install poppler
        ```
    - **Ubuntu:**
        ```bash
        sudo apt-get install poppler-utils
        ```
    - **Windows:**
        从 [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/) 下载 Poppler 二进制文件，并将 `bin` 文件夹添加到 PATH 环境变量。

---

## 使用方法

### 图形界面模式

1. 启动工具：
    ```bash
    python prod.py
    ```
2. 选择一个输出文件夹用于存储处理后的文件。
3. 从文件夹中加载要处理的文件。
4. 选择移除模式：**快速移除** 或 **深度移除**。
5. 选择需要处理的文件并点击 **执行**。

### 命令行模式（用于测试或集成）
- 您可以在代码中直接调用 `removerPdf.py` 和 `removerWord.py` 中的函数进行处理。

您也可以在没有图形界面的情况下运行 `cli.py`：

```bash
python cli.py INPUT_PATH --output OUTPUT_DIR --mode {fast/deep}
```

或简写为：

```bash
python cli.py INPUT_PATH -o OUTPUT_DIR -m {fast/deep}
```

**注意：**

- `--mode` 或 `-m` 默认采用快速移除，如需深度移除请使用 `-m deep`。
- `INPUT_PATH` 可以是单个文件，也可以是包含多个 PDF 或 Word 文档的目录。`--mode` 控制 PDF 的处理方式，默认值为 `fast`。

**测试：**

- 可以使用 `./test` 目录中的测试文件验证深度移除：

```bash
python cli.py ./test/test.pdf -o ./out --mode deep
```

---

### 函数解释：`is_text_color_rgb` 和 `is_text_color_hsv`

**注意：我在注释中添加了一些颜色和 HSV 预设，此方法可以保证移除具有特定颜色的水印；可以尝试调整这些值进行测试。**

这两个函数用于检测图像中的黑色或近黑色文本（或水印）。可以通过调整阈值来适应不同类型的水印。

#### **`is_text_color_rgb`**
该函数使用 RGB 色彩空间检测图像中的黑色或近黑色像素。

##### **工作原理：**
1. **RGB 阈值判断：**
   - 函数判断像素的三个通道（红、绿、蓝）的强度值是否均小于 `140`。
   - 满足条件的像素被认为是“深色”，可能代表文本或水印内容。

2. **适配水印：**
   - **提高阈值（`140 → 更高`）：** 用于检测浅灰色或较淡的黑色文本。
   - **降低阈值（`140 → 更低`）：** 更专注于检测纯黑色像素，排除较浅的标记。

3. **示例用例：**
   - 适用于检测纯黑色或灰色的文本水印。

##### **代码：**
```python
def is_text_color_rgb(img_array):
    # 使用 RGB 色彩空间识别黑色或近黑色像素
    mask = (
        (img_array[:, :, 0] < 140) &  # 红色通道阈值
        (img_array[:, :, 1] < 140) &  # 绿色通道阈值
        (img_array[:, :, 2] < 140)    # 蓝色通道阈值
    )
    return mask
```
#### **`is_text_color_hsv`**

该函数使用 HSV 色彩空间检测图像中类似黑色或深色的区域，能够更好地应对光照和颜色变化。

##### **工作原理：**

**1. HSV 转换：**
  - 将图像转换为 HSV 色彩空间。
  - 忽略色调（Hue, H），因为黑色不依赖特定颜色，仅分析饱和度（Saturation, S）和亮度（Value, V）。
    
**2. 阈值判断：**
  - 饱和度（`S < 40`）：确保该区域不含丰富的颜色（低饱和度意味着灰色或黑色）。
  - 亮度（`V < 160`）：确保该区域是深色（较低的值表示更暗的像素）。
    
**3. 适配水印：**
  - 提高饱和度阈值（`S < 40 → 更高`）：包含更多带色彩的水印。
  - 提高亮度阈值（`V < 160 → 更高`）：包含更浅的文本或水印。
    
**4. 示例用例：**
  - 适用于检测浅色、带色彩的深色水印。
    
##### **代码：**
```python
def is_text_color_hsv(img_array):
    # 将 RGB 图像转换为 HSV
    hsv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

    # 使用 HSV 色彩空间识别深色或黑色区域
    mask = (hsv_img[:, :, 1] < 40) & (hsv_img[:, :, 2] < 160)  # 饱和度和亮度阈值
    return mask
```

## 文件结构
  - prod.py： 主图形界面应用程序文件。
  - removerPdf.py： 用于处理和移除 PDF 文件水印的函数。
  - removerWord.py： 用于处理和移除 Word 文件水印的函数。
  - requirements.txt： 列出了所需的 Python 库。


## 依赖项

**工具依赖以下 Python 库：**

```
PyQt5==5.15.9
pikepdf==6.2.6
PyMuPDF==1.21.1
pdf2image==1.16.3
Pillow==9.4.0
opencv-python-headless==4.8.0.76
scikit-image==0.19.3
PyPDF2==3.0.1
```

**使用以下命令安装这些依赖项：**

```bash
pip install -r requirements.txt
```

## 示例

  - 处理前：
![Screenshot 2024-11-21 at 16 20 55](https://github.com/user-attachments/assets/9f95b3db-08e3-4e10-a9da-293cda385d2a)
    
  - 处理后：
![Screenshot 2024-11-21 at 16 20 57](https://github.com/user-attachments/assets/978c33b7-eb59-4de3-b71b-ddef5c4b9b24)

## 已知问题

### **内存占用：**
  - 处理较大的 PDF 文件时可能会消耗大量内存。工具会将中间处理结果保存到磁盘以缓解内存压力。

### **响应速度：**
  - 在深度移除模式下，GUI 可能会变得不太响应。

## 特别感谢

**特别感谢以下库和工具的开发者和维护者，这些开源项目为本工具的开发提供了强大的支持：**

- **[PyQt5](https://pypi.org/project/PyQt5/):** 用于创建现代化用户界面的强大工具。
- **[PyMuPDF](https://pymupdf.readthedocs.io/):** 提供了强大的 PDF 文档操作功能。
- **[pdf2image](https://pypi.org/project/pdf2image/):** 实现无缝的 PDF 到图像转换。
- **[NumPy](https://numpy.org/):** 用于高效的数组操作和数学运算。
- **[scikit-image](https://scikit-image.org/):** 提供了高级图像处理能力。
- **[Pillow](https://pillow.readthedocs.io/):** 用于多功能的图像操作。
- **[python-docx](https://python-docx.readthedocs.io/):** 用于处理 Word 文档。
- **[Poppler](https://poppler.freedesktop.org/):** 用于 PDF 渲染和转换。
- **[pikepdf](https://github.com/pikepdf/pikepdf):** 用于快速水印移除处理

**您的辛勤付出不仅使本项目得以实现，还帮助全球开发者创造了无数创新的解决方案。**

**感谢您对开源社区的无价贡献！❤️**

## 许可证

本项目基于 MIT 许可证开源。详情请见 [LICENSE](LICENSE)


