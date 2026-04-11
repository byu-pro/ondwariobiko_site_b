import os
import re

directory = '.'
files = [f for f in os.listdir(directory) if f.endswith('.html')]

menu_replacement = '''<ul id="main-menu" class="main-menu__accordion">
                    <li class="main-menu__item">
                      <a class="main-menu__link btn btn-anim" href="index-personal-portfolio.html">
                        <span class="btn-caption">Home</span>
                      </a>
                    </li>
                    <li class="main-menu__item">
                      <a class="main-menu__link btn btn-anim" href="works-simple.html">
                        <span class="btn-caption">Works</span>
                      </a>
                    </li>
                    <li class="main-menu__item">
                      <a class="main-menu__link btn btn-anim" href="about-me.html">
                        <span class="btn-caption">About</span>
                      </a>
                    </li>
                    <li class="main-menu__item">
                      <a class="main-menu__link btn btn-anim" href="services.html">
                        <span class="btn-caption">Services</span>
                      </a>
                    </li>
                    <li class="main-menu__item">
                      <a class="main-menu__link btn btn-anim" href="blog-creative.html">
                        <span class="btn-caption">Insights</span>
                      </a>
                    </li>
                    <li class="main-menu__item">
                      <a class="main-menu__link btn btn-anim" href="contact.html">
                        <span class="btn-caption">Contact</span>
                      </a>
                    </li>
                  </ul>'''

target_regex = r'<ul id="main-menu" class="main-menu__accordion">.*?</ul>'

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Use flags=re.DOTALL to match across multiple lines
    new_content = re.sub(target_regex, menu_replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated menu in {filename}")
    else:
        print(f"No changes needed for {filename}")
