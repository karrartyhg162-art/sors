import os
path = r"c:\Users\LOQ\Desktop\Source-main\zthon\utils\startup.py"
with open(path, 'rb') as f:
    content = f.read().decode('utf-8')

# Reduce retry count from 5 to 1 to prevent infinite-feeling loops
# when a module truly cannot be installed (e.g. pytgcalls on Windows)
content = content.replace('if check > 5:', 'if check > 1:')

with open(path, 'wb') as f:
    f.write(content.encode('utf-8'))
print("Done - reduced retry count")
