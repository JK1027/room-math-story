import os
import re

def set_theme(fpath, theme_colors, gradient_colors):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # replace colors
    for k, v in theme_colors.items():
        content = re.sub(rf'--{k}:\s*#[0-9a-fA-F]+;', f'--{k}: {v};', content)
        content = re.sub(rf'--{k}:\s*rgba\([^)]+\);', f'--{k}: {v};', content)
        
    bg_old = r'radial-gradient\(circle at 20% 30%, rgba[^)]+\) 0%, transparent 40%\),\s*radial-gradient\(circle at 80% 70%, rgba[^)]+\) 0%, transparent 40%\)'
    content = re.sub(bg_old, gradient_colors, content)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

themes = {
    '04': {
        'colors': {'bg-main': '#0c101b', 'glass-bg': 'rgba(15, 23, 42, 0.75)', 'glass-border': 'rgba(224, 180, 76, 0.25)', 'accent': '#e0b44c', 'accent-hover': '#f5d06e'},
        'grad': 'radial-gradient(circle at 20% 30%, rgba(224, 180, 76, 0.08) 0%, transparent 40%), radial-gradient(circle at 80% 70%, rgba(15, 23, 42, 0.3) 0%, transparent 40%)'
    },
    '05': {
        'colors': {'bg-main': '#050508', 'glass-bg': 'rgba(13, 10, 25, 0.75)', 'glass-border': 'rgba(255, 0, 127, 0.25)', 'accent': '#ff007f', 'accent-hover': '#ff3399'},
        'grad': 'radial-gradient(circle at 20% 30%, rgba(255, 0, 127, 0.08) 0%, transparent 40%), radial-gradient(circle at 80% 70%, rgba(0, 240, 255, 0.08) 0%, transparent 40%)'
    },
    '06': {
        'colors': {'bg-main': '#1a140d', 'glass-bg': 'rgba(30, 24, 15, 0.75)', 'glass-border': 'rgba(212, 175, 55, 0.25)', 'accent': '#d4af37', 'accent-hover': '#f0d05c'},
        'grad': 'radial-gradient(circle at 20% 30%, rgba(212, 175, 55, 0.08) 0%, transparent 40%), radial-gradient(circle at 80% 70%, rgba(184, 115, 51, 0.1) 0%, transparent 40%)'
    },
    '07': {
        'colors': {'bg-main': '#0f0a14', 'glass-bg': 'rgba(25, 15, 35, 0.75)', 'glass-border': 'rgba(192, 192, 192, 0.25)', 'accent': '#c0c0c0', 'accent-hover': '#ffffff'},
        'grad': 'radial-gradient(circle at 20% 30%, rgba(192, 192, 192, 0.08) 0%, transparent 40%), radial-gradient(circle at 80% 70%, rgba(128, 0, 128, 0.15) 0%, transparent 40%)'
    },
    '08': {
        'colors': {'bg-main': '#110000', 'glass-bg': 'rgba(25, 5, 5, 0.75)', 'glass-border': 'rgba(255, 30, 30, 0.25)', 'accent': '#ff1e1e', 'accent-hover': '#ff5555'},
        'grad': 'radial-gradient(circle at 20% 30%, rgba(255, 30, 30, 0.08) 0%, transparent 40%), radial-gradient(circle at 80% 70%, rgba(50, 0, 0, 0.2) 0%, transparent 40%)'
    }
}

for unit, theme in themes.items():
    fpath = f'scripts/builders/update_app_m2_{unit}.py'
    set_theme(fpath, theme['colors'], theme['grad'])
    print(f"Theme updated for {unit}")

