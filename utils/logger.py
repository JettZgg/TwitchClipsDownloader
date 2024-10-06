import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from PyQt6.QtCore import QObject, pyqtSignal

class GUILogHandler(QObject, logging.Handler):
    new_log = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        logging.Handler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        self.new_log.emit(msg)

def setup_logger(log_file="download.log", max_bytes=1048576, backup_count=5, gui_handler=None):
    logger = logging.getLogger('TwitchClipDownloader')
    logger.setLevel(logging.INFO)
    logger.handlers = []  # Clear existing handlers

    # Determine if the application is running as a script or frozen executable
    if getattr(sys, 'frozen', False):
        if sys.platform.startswith('win'):
            log_dir = os.path.join(os.environ['APPDATA'], 'TwitchClipDownloader', 'logs')
        elif sys.platform.startswith('darwin'):
            log_dir = os.path.expanduser('~/Library/Application Support/TwitchClipDownloader/logs')
        else:
            log_dir = os.path.join(os.path.expanduser('~'), '.TwitchClipDownloader', 'logs')
    else:
        log_dir = 'logs'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, log_file),
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if gui_handler:
        gui_handler.setFormatter(formatter)
        logger.addHandler(gui_handler)

    return logger
