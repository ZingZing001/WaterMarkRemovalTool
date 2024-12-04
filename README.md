# Watermark Remover Tool

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
<!-- language -->

[English](README.md) | [简体中文](README_zh-CN.md)

Plz leave me with a star if you think this tool is useful :)🌟
求求留个星星呗🥺🌟

A powerful and user-friendly tool for removing watermarks from PDF and Word documents. This application provides both fast and deep removal modes, ensuring optimal results for various watermark types.

NOTE: THIS TOOL ISN'T OPERATING CORRECTLY ON WINDOWS SYSTEM ATM DUE TO INSTALLATION OF POPPLER-UTILS
---

## Features

- **Fast Removal:** Quickly removes layer-based watermarks from PDF files.
- **Deep Removal:** Combines advanced image processing techniques to remove text and image-based watermarks.
- **Word Support:** Removes watermarks from `.docx` files.
- **Batch Processing:** Load multiple files and process them in bulk.
- **Customizable Modes:** Choose between "Fast Removal" and "Deep Removal."
- **Progress Tracking:** Visual progress bar and estimated completion time.
- **Cross-Platform:** Works on Windows, macOS, and Linux.

---

## Prerequisites

Ensure you have Python 3.9 or later installed. Additionally, install the dependencies listed in `requirements.txt`.

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ZingZing001/watermark-remover.git
    cd watermark-remover
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Install Poppler for PDF processing:
    - **macOS:**
        ```bash
        brew install poppler
        ```
    - **Ubuntu:**
        ```bash
        sudo apt-get install poppler-utils
        ```
    - **Windows:**
        Download Poppler binaries from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/) and add the `bin` folder to your PATH. **NOT WORKING RN**
---

## Usage

### GUI Mode

1. Launch the tool:
    ```bash
    python prod.py
    ```
    
2. Select an output folder for processed files.
3. Load files from a folder to process.
4. Choose removal mode: **Fast Removal** or **Deep Removal**.
5. Select the files to process and click **Execute**.

### Command Line Mode (for testing or integration)
- You can use the functions in `removerPdf.py` and `removerWord.py` programmatically.

### Function Explanation: `is_text_color_rgb` and `is_text_color_hsv`

These two functions are designed to detect black or near-black text (or watermarks) in an image. You can adjust the thresholds to adapt to different kinds of watermarks.

#### **`is_text_color_rgb`**
This function identifies black or near-black pixels in an image using the RGB colour space.

##### **How it works:**
1. **RGB Thresholding:** 
   - The function checks if the intensity values of all three channels (Red, Green, and Blue) are less than `140`.
   - Pixels meeting this condition are considered "dark," representing text or watermark content.

2. **Adjusting for Watermarks:**
   - **Increase the threshold (`140 → higher`)**: To detect lighter shades of gray or faint black text.
   - **Decrease the threshold (`140 → lower`)**: To focus on strictly darker pixels, excluding lighter marks.

3. **Example Use Case:**
   - Ideal for detecting solid black or grayscale text-based watermarks.

##### **Code:**
NOTE: I have added some colour and HSV preset in the comments form; this method is guaranteed to remove the watermarks with a certain colour; try to playing around with the values.
```python
def is_text_color_rgb(img_array):
    # Identify black or near-black pixels in RGB color space
    mask = (
        (img_array[:, :, 0] < 140) &  # Red channel threshold
        (img_array[:, :, 1] < 140) &  # Green channel threshold
        (img_array[:, :, 2] < 140)    # Blue channel threshold
    )
    return mask
```

#### **is_text_color_hsv**
This function identifies black-like or dark regions in the HSV (Hue, Saturation, Value) color space, which is more robust for varying lighting and color tones.

#### **How it works:**
1. **HSV Conversion:**
    - The image is converted to the HSV color space.
	- Hue (H) is ignored because black is not dependent on specific colors. Instead, Saturation (S) and Value (V) are analyzed.
2. **Thresholding:**
    - Saturation (S < 40): Ensures the region is not colorful (low saturation means grayscale or black).
    - Value (V < 160): Ensures the region is dark (lower values indicate darker pixels).
3. **Adjusting for Watermarks**:
    - Increase Saturation Threshold (S < 40 → higher): Includes slightly tinted watermarks.
    - Decrease Saturation Threshold (S < 40 → lower): Focuses strictly on grayscale or black regions.
    - Increase Value Threshold (V < 160 → higher): Includes lighter shades of text or watermark.
    - Decrease Value Threshold (V < 160 → lower): Focuses strictly on darker marks.
4. **Example Use Case:**
    - Particularly useful for detecting faintly tinted or dark watermarks.

#### **Code:**
```python
def is_text_color_hsv(img_array):
    # Convert the RGB image to HSV
    hsv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

    # Identify dark or black-like regions in HSV space
    mask = (hsv_img[:, :, 1] < 40) & (hsv_img[:, :, 2] < 160)  # Saturation and Value thresholds
    return mask
```

### Customizing for Different Watermarks

By modifying the threshold values, you can adapt the functions to detect specific types of watermarks:
1. **Light Gray Watermarks:**
    - Increase 140 in is_text_color_rgb and V < 160 in is_text_color_hsv to include lighter shades.
2. **Faint Colored Watermarks:**
    - Increase the S threshold in is_text_color_hsv to include more color.
3. **Dark and Clear Watermarks:**
    - Lower all thresholds (R/G/B < 140, S < 40, V < 160) to focus on darker and clearer watermarks.
      
---

## File Structure

- **prod.py**: Main GUI application file.
- **removerPdf.py**: Functions for processing and removing watermarks from PDF files.
- **removerWord.py**: Functions for processing and removing watermarks from Word documents.
- **requirements.txt**: List of required Python libraries.

---

## Dependencies

The tool depends on the following Python libraries:
```text
PyQt5==5.15.9
pikepdf==6.2.6
PyMuPDF==1.21.1
pdf2image==1.16.3
Pillow==9.4.0
opencv-python-headless==4.8.0.76
scikit-image==0.19.3
PyPDF2==3.0.1
```
Install these dependencies using `pip install -r requirements.txt`.
or if u prefer to have it installed in your public environment using `python -m pip install -r requirements.txt`

---

## Exampler
- Before
![Screenshot 2024-11-21 at 16 20 55](https://github.com/user-attachments/assets/9f95b3db-08e3-4e10-a9da-293cda385d2a)

- After
![Screenshot 2024-11-21 at 16 20 57](https://github.com/user-attachments/assets/978c33b7-eb59-4de3-b71b-ddef5c4b9b24)

---

## Known Issues

### Memory Usage: 
- Processing large PDFs may consume a significant amount of memory. The tool saves intermediate images to the disk to mitigate this. (SOLVED)

### Responsiveness: 
- The GUI may become unresponsive during intensive operations in Deep Removal mode.

---

## Special Thanks

A heartfelt thank you to the authors and maintainers of the following libraries and tools that made this project possible:

- **[PyQt5](https://pypi.org/project/PyQt5/):** For enabling the creation of a modern and user-friendly GUI.
- **[PyMuPDF](https://pymupdf.readthedocs.io/):** For providing robust tools to manipulate and analyze PDF documents.
- **[pdf2image](https://pypi.org/project/pdf2image/):** For seamless PDF-to-image conversion.
- **[NumPy](https://numpy.org/):** For efficient array manipulation and mathematical operations.
- **[scikit-image](https://scikit-image.org/):** For advanced image processing and manipulation capabilities.
- **[Pillow](https://pillow.readthedocs.io/):** For versatile image manipulation and saving functionalities.
- **[python-docx](https://python-docx.readthedocs.io/):** For enabling the manipulation of Word documents.
- **[Poppler](https://poppler.freedesktop.org/):** For handling PDF rendering and conversion.
- **[pikepdf](https://github.com/pikepdf/pikepdf):** For handling Fast WaterMark Removal

Your hard work and dedication have not only made this project possible but also helped countless developers worldwide to create innovative solutions. 

**Thank you for your invaluable contributions to the open-source community! ❤️**

---

## License

This project is licensed under the MIT License. See LICENSE for details.

## Credits

Developed by Zhang Johnson.
