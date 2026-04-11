import os
import re
import time

directory = '.'
# Unique timestamp based on current time
version = str(int(time.time()))

meta_tags = '''    <!-- Cache-Busting Settings Start -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <!-- Cache-Busting Settings End -->'''

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Add Meta Tags if not present, place them right before </head>
        if 'Cache-Busting Settings' not in content:
            content = content.replace('</head>', f'{meta_tags}\n  </head>')
        
        # 2. Add or update versioning on CSS references (?v=123456789)
        # Regex matches href="css/file.css" or href="css/file.css?v=anything"
        content = re.sub(r'(href="css/.*?\.css)(\?v=.*?)?(")', rf'\1?v={version}\3', content)
        
        # 3. Add or update versioning on JS references (?v=123456789)
        content = re.sub(r'(src="js/.*?\.js)(\?v=.*?)?(")', rf'\1?v={version}\3', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Anti-cache settings updated in {filename}")
