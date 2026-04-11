import re

html_file = 'index-personal-portfolio.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix the SVG sizing in the footer:
# Remove hardcoded width, height, zoomAndPan, preserveAspectRatio
content = re.sub(
    r'<svg class="mxd-footer__svg-v2" xmlns="http://www\.w3\.org/2000/svg" xmlns:xlink="http://www\.w3\.org/1999/xlink" width="518" zoomAndPan="magnify" viewBox="0 0 388\.5 54" height="72" preserveAspectRatio="xMidYMid meet" version="1\.0">',
    r'<svg class="mxd-footer__svg-v2" version="1.0" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 388.5 54" xml:space="preserve">',
    content
)

# 2. Fix the email: remove hello@
content = re.sub(
    r'<a href="mailto:hello@ondwariobiko\.com\?subject=Message%20from%20your%20site">hello@ondwariobiko\.com</a>',
    r'<a href="mailto:ondwariobiko.com?subject=Message%20from%20your%20site">ondwariobiko.com</a>',
    content
)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
