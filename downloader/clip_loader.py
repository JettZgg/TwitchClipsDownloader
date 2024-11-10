import re

def load_clips_info(input_text):
    clips_info = []
    
    # Split text into lines to preserve order
    lines = input_text.split('\n')
    current_index = 1
    
    # Process lines in pairs (username line + URL line)
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
            
        # Extract username from @ mention
        username_match = re.match(r'^@(\S+)', line)
        if username_match:
            username = username_match.group(1)  # This preserves case
            
            # Look for URL in next lines
            j = i + 1
            while j < len(lines):
                url_line = lines[j].strip()
                url_match = re.search(r'https?://(?:www\.)?twitch\.tv/[^/]+/clip/[\w-]+(?:\?[^\s]*)?', url_line)
                if url_match:
                    clips_info.append({
                        'name': str(current_index),
                        'url': url_match.group(0),
                        'order': current_index,
                        'player': username  # Using case-preserved username from @ mention
                    })
                    current_index += 1
                    i = j
                    break
                j += 1
        i += 1
    
    return clips_info
