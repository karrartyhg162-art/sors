import os, re
count = 0
for root, _, files in os.walk('zthon/assistant'):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            # Replace pattern="..." with pattern=r"..." if it contains a backslash
            new_content = re.sub(r'pattern=([\'\"])(.*?\\[\s\S]*?)\1', r'pattern=r\1\2\1', content)
            new_content = re.sub(r'pattern=f([\'\"])(.*?\\[\s\S]*?)\1', r'pattern=fr\1\2\1', new_content)
            if content != new_content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                count += 1
print(f'Fixed {count} files in assistant')
