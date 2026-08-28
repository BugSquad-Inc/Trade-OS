# Trade OS Full Sprint 1 Generator
import os
import sys

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f'[CREATED] {path}')

print('generate_all.py initialized')
