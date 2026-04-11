import os
import re

directory = '.'
files = [f for f in os.listdir(directory) if f.endswith('.html')]

# Caption replacement
caption_target = r'<p class="mxd-menu__caption menu-fade-in">\s*🦄 Innovative design\s*<br>\s*and cutting-edge development\s*</p>'
caption_replacement = '<p class="mxd-menu__caption menu-fade-in">🎯 Strategic brand systems<br>for businesses scaling with clarity</p>'

# Bio replacement (handling different line breaks)
bio_target = r'<p class="menu-promo__caption menu-fade-in">\s*👋 Nice to see you!<br>\s*I\'m Ondwari Obiko, digital\s*\n?\s*designer and illustrator based in Odesa, Ukraine\s*</p>'
bio_replacement = '<p class="menu-promo__caption menu-fade-in">👋 Nice to see you!<br>I\'m Ondwari Obiko, a Digital Architect and Brand Engineer based in Nairobi, Kenya</p>'

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(caption_target, caption_replacement, content, flags=re.DOTALL)
    new_content = re.sub(bio_target, bio_replacement, new_content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"No changes for {filename}")
