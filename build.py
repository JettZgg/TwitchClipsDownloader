import PyInstaller.__main__
import os
import sys

def build_executable():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run.py')
    
    common_args = [
        script_path,
        '--name=TwitchClipDownloader',
        '--onefile',
        '--windowed',
        '--add-data=logs:logs',
        '--hidden-import=PyQt6',
        '--hidden-import=selenium',
        '--hidden-import=webdriver_manager',
    ]
    
    if sys.platform.startswith('win'):
        icon_file = 'icon.ico'
    elif sys.platform.startswith('darwin'):
        icon_file = 'icon.icns'
    else:
        icon_file = None
    
    if icon_file:
        common_args.append(f'--icon={icon_file}')
    
    PyInstaller.__main__.run(common_args)

if __name__ == "__main__":
    build_executable()
