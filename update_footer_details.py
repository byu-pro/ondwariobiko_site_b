import re

html_file = 'index-personal-portfolio.html'
svg_file = 'my_brand_assets/logos/footerlarge_text.svg'

with open(svg_file, 'r', encoding='utf-8') as f:
    new_svg = f.read().strip()

# We should ensure the new SVG has the right class so it gets styled correctly, but the original has `class="mxd-footer__svg-v2"`.
# Let's insert the class `class="mxd-footer__svg-v2"` into the user's SVG.
if '<svg ' in new_svg:
    new_svg = new_svg.replace('<svg ', '<svg class="mxd-footer__svg-v2" ', 1)

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the original footer SVG block (lines 866-890)
# We can use regex to match exactly from `<svg class="mxd-footer__svg-v2"` to `</svg>` inside `<div class="mxd-footer__fullwidth-text personal anim-top-to-bottom">`
regex_svg = re.compile(r'<svg class="mxd-footer__svg-v2".*?</svg>', re.DOTALL)
content = regex_svg.sub(new_svg, content, count=1)

# Modify email
content = re.sub(
    r'<a href="mailto:example@example\.com[^"]*">hello@rayostudio\.com</a>',
    r'<a href="mailto:hello@ondwariobiko.com?subject=Message%20from%20your%20site">hello@ondwariobiko.com</a>',
    content
)

# Modify phone number
content = re.sub(
    r'<a href="tel:\+12127089400">\+1 212-708-9400</a>',
    r'<a href="tel:+254702255575">+254 702 255 575</a>',
    content
)

# Also ensure that fill colors in the provided SVG use currentColor or css variable so it inherits correctly if needed,
# Wait, the user has fill="#000000" in all their paths based on the file content. 
# We should probably change `#000000` to `var(--t-bright)` so it respects dark mode!
content = content.replace('fill="#000000"', 'fill="var(--t-bright)"')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated footer SVG, email, and phone number!")
