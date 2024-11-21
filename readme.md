# Watermark Remover Tool

A powerful and user-friendly tool for removing watermarks from PDF and Word documents. This application provides both fast and deep removal modes, ensuring optimal results for various watermark types.

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
    git clone https://github.com/yourusername/watermark-remover.git
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
        Download Poppler binaries from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/) and add the `bin` folder to your PATH.

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
PyQt5
pymupdf
pdf2image
numpy
scikit-image
Pillow
python-docx
```
Install these dependencies using `pip install -r requirements.txt`.

---

## Known Issues

### Memory Usage: 
- Processing large PDFs may consume a significant amount of memory. The tool saves intermediate images to the disk to mitigate this.

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

Your hard work and dedication have not only made this project possible but also helped countless developers worldwide to create innovative solutions. 

**Thank you for your invaluable contributions to the open-source community! ❤️**

---

## License

This project is licensed under the MIT License. See LICENSE for details.

## Credits

Developed by Zhang Johnson.
