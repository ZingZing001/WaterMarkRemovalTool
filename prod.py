import os
import threading
import time
from functools import partial
from PyQt5 import QtWidgets, QtCore
from removerWord import remove_watermark_from_word
from removerPdf import remove_layer_watermarks, remove_watermark_from_pdf


class WatermarkRemoverApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.output_folder_path = ""
        self.file_paths = []
        self.init_ui()

    def init_ui(self):
        # Create layout and widgets
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Select a folder to load files for processing")
        layout.addWidget(self.label)

        self.select_output_folder_button = QtWidgets.QPushButton("Select Output Folder")
        self.select_output_folder_button.clicked.connect(self.select_output_folder)
        layout.addWidget(self.select_output_folder_button)

        self.load_files_button = QtWidgets.QPushButton("Load Files from Folder")
        self.load_files_button.clicked.connect(self.load_files)
        layout.addWidget(self.load_files_button)

        self.file_list_widget = QtWidgets.QListWidget()
        self.file_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        layout.addWidget(self.file_list_widget)

        self.select_all_button = QtWidgets.QPushButton("Select All Files")
        self.select_all_button.clicked.connect(self.select_all_files)
        layout.addWidget(self.select_all_button)

        self.unselect_all_button = QtWidgets.QPushButton("Unselect All Files")
        self.unselect_all_button.clicked.connect(self.unselect_all_files)
        layout.addWidget(self.unselect_all_button)

        self.removal_mode_dropdown = QtWidgets.QComboBox()
        self.removal_mode_dropdown.addItems(["Fast Removal", "Deep Removal"])
        layout.addWidget(self.removal_mode_dropdown)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.estimated_time_label = QtWidgets.QLabel("Estimated Time: N/A")
        layout.addWidget(self.estimated_time_label)

        self.execute_button = QtWidgets.QPushButton("Execute")
        self.execute_button.clicked.connect(self.execute_removal)
        layout.addWidget(self.execute_button)

        self.setLayout(layout)
        self.setWindowTitle("Watermark Remover Tool")
        self.resize(400, 500)

    def select_output_folder(self):
        self.output_folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if self.output_folder_path:
            print(f"Selected output folder: {self.output_folder_path}")

    def load_files(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder to Load Files")
        if folder_path:
            self.file_paths.clear()
            self.file_list_widget.clear()
            files = os.listdir(folder_path)
            sorted_files = sorted(files)  # Sort files alphabetically
            for file_name in sorted_files:
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and (file_name.endswith(".pdf") or file_name.endswith(".docx")):
                    self.file_paths.append(file_path)
                    item = QtWidgets.QListWidgetItem(file_name)
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self.file_list_widget.addItem(item)
            print(f"Loaded {len(self.file_paths)} files.")

    def select_all_files(self):
        for i in range(self.file_list_widget.count()):
            self.file_list_widget.item(i).setCheckState(QtCore.Qt.Checked)

    def unselect_all_files(self):
        for i in range(self.file_list_widget.count()):
            self.file_list_widget.item(i).setCheckState(QtCore.Qt.Unchecked)

    def execute_removal(self):
        selected_files = []
        for i in range(self.file_list_widget.count()):
            item = self.file_list_widget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                selected_files.append(self.file_paths[i])

        if not selected_files:
            QtWidgets.QMessageBox.warning(self, "No Files Selected", "Please select files to process.")
            return

        # Disable buttons during processing
        self.toggle_buttons(False)

        removal_mode = self.removal_mode_dropdown.currentText()
        print(f"Starting removal in {removal_mode} mode for {len(selected_files)} files.")

        # Estimate the processing time based on removal mode
        avg_time_per_file = 5 if removal_mode == "Fast Removal" else 15  # 5 seconds for Fast, 15 seconds for Deep
        estimated_time = len(selected_files) * avg_time_per_file
        self.estimated_time_label.setText(f"Estimated Time: ~{estimated_time} seconds")
        self.progress_bar.setMaximum(len(selected_files))
        self.progress_bar.setValue(0)

        threading.Thread(target=self.process_files, args=(selected_files, removal_mode)).start()

    def process_files(self, selected_files, removal_mode):
        try:
            processed_count = 0
            for file_path in selected_files:
                file_name = os.path.basename(file_path)
                output_path = os.path.join(
                    self.output_folder_path,
                    file_name.replace(".docx", "_no_watermark.docx").replace(".pdf", "_no_watermark.pdf")
                )
                try:
                    if file_path.endswith(".pdf"):
                        if removal_mode == "Fast Removal":
                            print(f"Fast Removal: {file_name}")
                            result_path = remove_layer_watermarks(file_path)
                        else:
                            print(f"Deep Removal: {file_name}")
                            result_path = remove_watermark_from_pdf(file_path)

                        if result_path:
                            os.rename(result_path, output_path)
                            self.update_file_status(file_name, "Done")
                        else:
                            self.update_file_status(file_name, "Failed")
                    elif file_path.endswith(".docx"):
                        print(f"Processing Word file: {file_name}")
                        result_path = remove_watermark_from_word(file_path)
                        if result_path:
                            os.rename(result_path, output_path)
                            self.update_file_status(file_name, "Done")
                        else:
                            self.update_file_status(file_name, "Failed")
                except Exception as e:
                    print(f"Error processing {file_name}: {e}")
                    self.update_file_status(file_name, "Failed")

                processed_count += 1
                QtCore.QTimer.singleShot(0, partial(self.progress_bar.setValue, processed_count))

            QtCore.QTimer.singleShot(0, partial(self.show_message, "Processing Complete", "All selected files have been processed."))
        except Exception as e:
            QtCore.QTimer.singleShot(0, partial(self.show_message, "Error", f"An error occurred: {e}"))
        finally:
            QtCore.QTimer.singleShot(0, partial(self.toggle_buttons, True))  # Re-enable buttons after processing

    def update_file_status(self, file_name, status):
        for i in range(self.file_list_widget.count()):
            item = self.file_list_widget.item(i)
            if item.text().startswith(file_name):
                item.setText(f"{file_name} - {status}")
                break

    def toggle_buttons(self, enable):
        self.select_output_folder_button.setEnabled(enable)
        self.load_files_button.setEnabled(enable)
        self.select_all_button.setEnabled(enable)
        self.unselect_all_button.setEnabled(enable)
        self.removal_mode_dropdown.setEnabled(enable)
        self.execute_button.setEnabled(enable)

    def show_message(self, title, message):
        QtWidgets.QMessageBox.information(self, title, message)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = WatermarkRemoverApp()
    window.show()
    app.exec()