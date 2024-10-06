import re

def load_clips_info(input_text):
    clips_info = []
    lines = input_text.strip().split('\n')
    
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            name = lines[i].strip()
            url = lines[i + 1].strip()
            
            # Extract the clip name from the URL if it's not provided
            if not name:
                match = re.search(r'/clip/([^?]+)', url)
                if match:
                    name = match.group(1)
                else:
                    name = f"Clip_{i//2 + 1}"
            
            clips_info.append({
                'name': f"{i//2 + 1}. {name}",
                'url': url
            })
    
    return clips_info
