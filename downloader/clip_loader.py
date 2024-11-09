import re

def load_clips_info(input_text):
    clips_info = []
    
    # Regex pattern to match Twitch clip URLs
    twitch_pattern = r'https?://(?:www\.)?twitch\.tv/\w+/clip/[\w-]+(?:\?[^\s]*)?'
    
    # Find all Twitch clip URLs in the input text
    urls = re.finditer(twitch_pattern, input_text)
    
    # Process each valid Twitch clip URL
    for index, match in enumerate(urls, 1):
        url = match.group()
        clips_info.append({
            'name': str(index),
            'url': url
        })
    
    return clips_info
