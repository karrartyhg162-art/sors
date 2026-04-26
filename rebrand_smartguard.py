import os, re

def process_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False
        
    original = content
    
    # Replace [Smart Guard](https://t.me/SI0lZ) with [Smart Guard](https://t.me/SI0lZ)
    content = content.replace('[Smart Guard](https://t.me/SI0lZ)', '[Smart Guard](https://t.me/SI0lZ)')
    
    # Split text into markdown links and non-links
    # A markdown link looks like [text](url)
    parts = re.split(r'(\[[^\]]*\]\([^\)]*\))', content)
    for i in range(len(parts)):
        # If this part is NOT a markdown link
        if not parts[i].startswith('['):
            # Replace 'Smart Guard' with linked version
            # We avoid replacing if it's in a getLogger statement, or if it's part of a URL (t.me/Smart Guard)
            # We also avoid if it's already followed by `](` which means it might be a broken split or something
            
            # Simple replace:
            parts[i] = parts[i].replace('Smart Guard', '[Smart Guard](https://t.me/SI0lZ)')
            
            # Fix up double links if they accidentally occurred:
            parts[i] = parts[i].replace('[[Smart Guard](https://t.me/SI0lZ)](https://t.me/SI0lZ)', '[Smart Guard](https://t.me/SI0lZ)')
            
            # Fix up if we replaced inside getLogger
            parts[i] = parts[i].replace('getLogger("[Smart Guard](https://t.me/SI0lZ)', 'getLogger("Smart Guard')
            parts[i] = parts[i].replace('getLogger(\'[Smart Guard](https://t.me/SI0lZ)', 'getLogger(\'[Smart Guard](https://t.me/SI0lZ)')
            
            # Fix up if we replaced inside a URL (like https://github.com/Zed-Thon/Smart Guard/)
            parts[i] = parts[i].replace('Zed-Thon/[Smart Guard](https://t.me/SI0lZ)', 'Zed-Thon/Smart Guard')
            parts[i] = parts[i].replace('t.me/[Smart Guard](https://t.me/SI0lZ)', 't.me/Smart Guard')

    content = ''.join(parts)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

count = 0
for root, _, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root: continue
    for f in files:
        if f.endswith('.py'):
            if process_file(os.path.join(root, f)):
                count += 1
print(f'Rebranded {count} files')
