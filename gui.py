from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog
)
from PyQt6.QtCore import QThread, pyqtSignal
import sys
import os
from typing import Optional
from downloader.clip_loader import load_clips_info
from downloader.downloader import download_clips
from utils.logger import setup_logger, GUILogHandler
from PyQt6.QtGui import QColor, QPalette, QTextCharFormat
import os
from pathlib import Path

class DownloadThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, input_text: str, output_dir: str):
        super().__init__()
        self.input_text = input_text
        self.output_dir = output_dir
        self.gui_log_handler = GUILogHandler()
        
    def run(self):
        try:
            logger = setup_logger(gui_handler=self.gui_log_handler)
            clips_info = load_clips_info(self.input_text)
            download_clips(clips_info, self.output_dir, logger=logger)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

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
        self.logger = setup_logger()
        self.download_thread: Optional[DownloadThread] = None

    def setup_ui(self):
        # Input text area
        self.input_text = QTextEdit()
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

        # Set default output directory
        default_download_path = str(Path.home() / "Downloads")
        self.default_output_dir = os.path.join(default_download_path, "clips")
        if not os.path.exists(self.default_output_dir):
            os.makedirs(self.default_output_dir)
        self.output_entry.setText(self.default_output_dir)

        # Log area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.layout.addWidget(QLabel("Log:"))
        self.layout.addWidget(self.log_text)

        # Buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Download")
        self.start_button.clicked.connect(self.start_download)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_download)
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(button_layout)

        # Add these lines at the end of setup_ui method
        self.input_text.setAcceptRichText(False)
        self.input_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    def select_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_entry.setText(directory)

    def start_download(self):
        input_text = self.input_text.toPlainText()
        output_dir = self.output_entry.text() or self.default_output_dir

        if not input_text.strip():
            self.log_text.append("Please enter clip information.")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.start_button.setEnabled(False)
        self.start_button.setStyleSheet(self.start_button.styleSheet())
        self.cancel_button.setEnabled(True)
        self.cancel_button.setStyleSheet(self.cancel_button.styleSheet())

        self.download_thread = DownloadThread(input_text, output_dir)
        self.download_thread.gui_log_handler.new_log.connect(self.update_log)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.error.connect(self.handle_error)
        self.download_thread.start()

    def cancel_download(self):
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.terminate()
            self.log_text.append("Download cancelled.")
            self.download_finished()

    def download_finished(self):
        self.start_button.setEnabled(True)
        self.start_button.setStyleSheet(self.start_button.styleSheet())
        self.cancel_button.setEnabled(False)
        self.cancel_button.setStyleSheet(self.cancel_button.styleSheet())

    def update_log(self, message: str):
        self.log_text.append(message)

    def handle_error(self, error_message: str):
        self.log_text.append(f"Error: {error_message}")
        self.download_finished()

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
                border: 1px solid #555555;
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
        self.cancel_button.setStyleSheet(button_style)

def main():
    app = QApplication(sys.argv)
    window = TwitchClipDownloaderGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()