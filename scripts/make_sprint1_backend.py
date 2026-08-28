
# Trade OS Sprint 1 Backend Generator
import os
def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '
')
    print(f'+[CHECK] Wrote {path}')

#