"""Quick preview grid.  python3 render.py scenes out.png "Mount|K guard"   (then LOOK at the PNG)"""
import sys,importlib,os
from playwright.sync_api import sync_playwright
from fig import figure_html, PANEL_CSS
mod=importlib.import_module(sys.argv[1]); out=sys.argv[2]
sel=[x for x in mod.SC if (len(sys.argv)<4 or x[0] in sys.argv[3].split('|'))]
cells=''.join(f'<div style="display:inline-block;width:420px;margin:6px;vertical-align:top"><div style="font:700 15px sans-serif;margin:2px 0">{t}</div>{figure_html(f()[0])}</div>' for t,f in sel)
open('prev.html','w').write(f'<html><head><style>body{{font-family:DejaVu Sans,sans-serif}}{PANEL_CSS}</style></head><body style="margin:0;background:#fff;width:880px">{cells}</body></html>')
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=os.environ.get('PW_CHROMIUM') or None); pg=b.new_page(viewport={'width':880,'height':800}); pg.goto('file://'+os.path.abspath('prev.html')); pg.screenshot(path=out,full_page=True); b.close()
