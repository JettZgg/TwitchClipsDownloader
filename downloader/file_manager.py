import os
import requests
import threading

# Thread-safe counter for file naming
class FileCounter:
    def __init__(self, start_number):
        self.count = start_number
        self.lock = threading.Lock()
    
    def get_next(self):
        with self.lock:
            current = self.count
            self.count += 1
            return current

def get_max_number(output_dir):
    max_number = 0
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            if filename.endswith('.mp4'):
                try:
                    number = int(filename.split('.')[0])
                    max_number = max(max_number, number)
                except (ValueError, IndexError):
                    continue
    return max_number

def save_clip(download_url, clip_name, output_dir, file_counter):
    """
    Download and save a Twitch clip to the specified directory.
    
    :param download_url: Download URL.
    :param clip_name: Name of the clip (including order and username with case preserved).
    :param output_dir: Output directory.
    :param file_counter: Thread-safe counter for file naming.
    """
    try:
        # Create file path with exact case preservation
        file_path = os.path.join(output_dir, f"{clip_name}.mp4")
        
        response = requests.get(download_url, stream=True)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"File saved successfully: {file_path}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")
