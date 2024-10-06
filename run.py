import sys
import os

# Determine if the application is running as a script or frozen executable
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# Add the application path to sys.path
sys.path.insert(0, application_path)

from utils.suppress_warnings import suppress_warnings
suppress_warnings()

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from main import main

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set a default font for the entire application
    if sys.platform.startswith('win'):
        default_font = QFont("Segoe UI", 10)
    elif sys.platform.startswith('darwin'):
        default_font = QFont("SF Pro", 13)
    else:
        default_font = QFont("Arial", 12)
    
    app.setFont(default_font)
    
    main()
    sys.exit(app.exec())
