import os
import re

directory = '.'
files = [f for f in os.listdir(directory) if f.endswith('.html')]

# Footer replacement
# Target the previous replacement I made
footer_target = r'<p class="t-xsmall t-muted">\s*onwariobiko, All Rights Reserved, The Way It\'s Meant To Be\s*<i class="ph-bold ph-copyright"></i>\s*2026\s*</p>'
footer_replacement = '''<p class="t-xsmall t-muted">
                <i class="ph-bold ph-copyright"></i>
                2026 Ondwari Obiko. All Rights Reserved
              </p>'''

# Navigation replacement
nav_target = r'<p class="t-xsmall">\s*onwariobiko, All Rights Reserved, The Way It\'s Meant To Be\s*</p>\s*<p class="t-xsmall">\s*<i class="ph ph-copyright"></i>\s*2026\s*</p>'
nav_replacement = '''<p class="t-xsmall">
                © 2026 Ondwari Obiko. All Rights Reserved
              </p>'''

# Also handle cases where my previous script didn't run or ran differently
footer_target_alt = r'<p class="t-xsmall t-muted">\s*<a class="no-effect" href="https://1\.envato\.market/EKA9WD" target="_blank">Mix_Design</a>\s*<i class="ph-bold ph-copyright"></i>\s*2025\s*</p>'
nav_target_alt = r'<p class="t-xsmall">\s*Made with\s*<i class="ph-fill ph-heart t-additional"></i>\s*by\s*<a class="no-effect" href="https://1\.envato\.market/EKA9WD" target="_blank">Mix_Design</a>\s*</p>\s*<p class="t-xsmall">\s*<i class="ph ph-copyright"></i>\s*2025\s*</p>'

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(footer_target, footer_replacement, content, flags=re.DOTALL)
    new_content = re.sub(nav_target, nav_replacement, new_content, flags=re.DOTALL)
    
    # Also catch any missed ones from previous state
    new_content = re.sub(footer_target_alt, footer_replacement, new_content, flags=re.DOTALL)
    new_content = re.sub(nav_target_alt, nav_replacement, new_content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"No changes for {filename}")
