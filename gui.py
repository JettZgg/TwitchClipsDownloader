from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog
)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QTextCharFormat
import sys
import os
from pathlib import Path
from typing import Optional
from downloader.downloader import download_clips
from downloader.clip_loader import load_clips_info
from utils.logger import setup_logger, GUILogHandler

class DownloadThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, clips_info, output_dir, logger):
        super().__init__()
        self.clips_info = clips_info
        self.output_dir = output_dir
        self.logger = logger

    def run(self):
        try:
            download_clips(self.clips_info, self.output_dir, logger=self.logger)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class TwitchClipDownloaderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twitch Clip Downloader")
        self.setGeometry(100, 100, 600, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.setup_ui()
        self.set_dark_mode_styles()

        # Set default output directory
        default_download_path = str(Path.home() / "Downloads")
        self.default_output_dir = os.path.join(default_download_path, "clips")
        if not os.path.exists(self.default_output_dir):
            os.makedirs(self.default_output_dir)
        self.output_entry.setText(self.default_output_dir)

        self.gui_log_handler = GUILogHandler()
        self.gui_log_handler.new_log.connect(self.update_log)
        self.logger = setup_logger(gui_handler=self.gui_log_handler)
        self.download_thread: Optional[DownloadThread] = None

    def setup_ui(self):
        # Input text area
        self.input_text = QTextEdit()
        self.input_text.setAcceptRichText(False)
        self.input_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.layout.addWidget(QLabel("Clip Information:"))
        self.layout.addWidget(self.input_text)

        # Output directory selection
        output_layout = QHBoxLayout()
        self.output_entry = QLineEdit()
        self.output_button = QPushButton("Browse")
        self.output_button.clicked.connect(self.select_output_directory)
        output_layout.addWidget(QLabel("Output Directory:"))
        output_layout.addWidget(self.output_entry)
        output_layout.addWidget(self.output_button)
        self.layout.addLayout(output_layout)

        # Log area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.layout.addWidget(QLabel("Log:"))
        self.layout.addWidget(self.log_text)

        # Start Download button
        self.start_button = QPushButton("Start Download")
        self.start_button.clicked.connect(self.start_download)
        self.layout.addWidget(self.start_button)

    def set_dark_mode_styles(self):
        # Set dark background and light text for better contrast
        dark_palette = self.palette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        self.setPalette(dark_palette)

        # Style for QTextEdit (input_text and log_text)
        text_edit_style = """
            QTextEdit {
                background-color: #232323;
                color: #ffffff;
                border: 1px solid #555555;
            }
        """
        self.input_text.setStyleSheet(text_edit_style)
        self.log_text.setStyleSheet(text_edit_style)

        # Remove link formatting
        text_char_format = QTextCharFormat()
        text_char_format.setForeground(QColor(255, 255, 255))
        text_char_format.setAnchor(False)
        self.input_text.setCurrentCharFormat(text_char_format)

        # Style for QLineEdit
        self.output_entry.setStyleSheet("""
            QLineEdit {
                background-color: #232323;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 2px;
            }
        """)

        # Style for QPushButton
        button_style = """
            QPushButton {
                background-color: #4a4a4a;
                color: #ffffff;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #808080;
            }
        """
        self.output_button.setStyleSheet(button_style)
        self.start_button.setStyleSheet(button_style)

    def select_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_entry.setText(dir_path)

    def start_download(self):
        input_text = self.input_text.toPlainText()
        output_dir = self.output_entry.text() or self.default_output_dir

        if not input_text.strip():
            self.log_text.append("Please enter clip information.")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        clips_info = load_clips_info(input_text)
        self.download_thread = DownloadThread(clips_info, output_dir, self.logger)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.error.connect(self.handle_error)
        self.download_thread.start()

        self.start_button.setEnabled(False)
        self.start_button.setStyleSheet(self.start_button.styleSheet())

    def download_finished(self):
        self.log_text.append("Download completed.")
        self.start_button.setEnabled(True)
        self.start_button.setStyleSheet(self.start_button.styleSheet())

    def handle_error(self, error_message):
        self.log_text.append(f"Error: {error_message}")
        self.start_button.setEnabled(True)
        self.start_button.setStyleSheet(self.start_button.styleSheet())

    def update_log(self, message):
        self.log_text.append(message)

def main():
    app = QApplication(sys.argv)
    window = TwitchClipDownloaderGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()