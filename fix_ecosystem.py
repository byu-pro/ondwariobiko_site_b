import re

html_file = 'index-personal-portfolio.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's strip the 'anim-uni-in-up' from the footer-socials__item list items 
# just in case GSAP is failing to trigger the scroll animation for that far-down card.
content = re.sub(r'class="footer-socials__item anim-uni-in-up"', r'class="footer-socials__item"', content)

# Also let's embed a tiny safety style block right above them to guarantee visibility 
# in case there is some bizarre color clashing (e.g., pitch black text on pitch black background).
safety_style = '<style>.footer-socials__link { opacity: 1 !important; visibility: visible !important; }</style>\n              <div class="footer-blocks__socials">'
content = content.replace('<div class="footer-blocks__socials">', safety_style)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Ecosystem links fixed!")
