import os
import requests

def save_clip(download_url, clip_name, output_dir):
    """
    Download and save a Twitch clip to the specified directory.
    
    :param download_url: Download URL.
    :param clip_name: Name of the clip (including number).
    :param output_dir: Output directory.
    """
    try:
        response = requests.get(download_url, stream=True)
        file_path = os.path.join(output_dir, f"{clip_name}.mp4")
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"File saved successfully: {file_path}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")
