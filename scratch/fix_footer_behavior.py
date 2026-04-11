import os
import re

directory = '.'
files = [f for f in os.listdir(directory) if f.endswith('.html')]

# Fix to-top button
to_top_target = r'<a href="#0" id="to-top" class="btn btn-to-top slide-up"[^>]*>.*?<i class="ph ph-arrow-up"[^>]*></i>.*?</a>'
to_top_replacement = '''<a href="#0" id="to-top" class="btn btn-to-top slide-up anim-no-delay">
      <i class="ph ph-arrow-up"></i>
    </a>'''

# Fix socials container
socials_container_target = r'<div class="footer-blocks__socials" style="[^"]*">'
socials_container_replacement = '<div class="footer-blocks__socials">'

# Fix social items
social_item_target = r'<li class="footer-socials__item" style="[^"]*">'
social_item_replacement = '<li class="footer-socials__item anim-uni-in-up">'

# Fix social links (remove inline color)
social_link_target = r'<a href="([^"]*)" class="footer-socials__link" target="_blank" style="[^"]*">'
social_link_replacement = r'<a href="\1" class="footer-socials__link" target="_blank">'

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(to_top_target, to_top_replacement, content, flags=re.DOTALL)
    new_content = re.sub(socials_container_target, socials_container_replacement, new_content)
    new_content = re.sub(social_item_target, social_item_replacement, new_content)
    new_content = re.sub(social_link_target, social_link_replacement, new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed footer in {filename}")
    else:
        print(f"No changes needed for {filename}")
