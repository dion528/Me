"""Build the Position Atlas PDF.  Usage: python3 build.py  ->  build/Position-Atlas.pdf"""
import os, subprocess, sys
from playwright.sync_api import sync_playwright
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
subprocess.run([sys.executable, 'atlas.py'], check=True)          # writes atlas.html
os.makedirs('build', exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('PW_CHROMIUM') or None); pg = b.new_page()
    pg.goto('file://' + os.path.join(here, 'atlas.html')); pg.wait_for_timeout(1000)
    pg.pdf(path='build/Position-Atlas.pdf', format='A4', print_background=True, prefer_css_page_size=True)
    b.close()
print('built build/Position-Atlas.pdf')
