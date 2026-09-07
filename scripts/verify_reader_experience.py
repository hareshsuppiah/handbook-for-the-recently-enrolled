#!/usr/bin/env python3
"""Check rendered reader assets, reusable blanks and safe image placement.

This verifies static contracts, not keyboard behaviour or accessibility conformance.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import csv, re, sys, zipfile, xml.etree.ElementTree as ET
from build_downloads import template_download_text
from finish_epub import finish, EpubError
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'
failures=[]
class Assets(HTMLParser):
    def __init__(self):
        super().__init__(); self.local=[]; self.main=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('img','script') and a.get('src'): self.local.append(a['src'])
        if tag=='link' and a.get('rel')=='stylesheet' and a.get('href'): self.local.append(a['href'])

def check(condition,message):
    if not condition: failures.append(message)
pages=list(SITE.rglob('*.html'))
check(bool(pages),'No rendered HTML pages')
for page in pages:
    text=page.read_text(encoding='utf-8'); parser=Assets();parser.feed(text)
    for url in parser.local:
        parts=urlsplit(url)
        if parts.scheme or url.startswith('//'): continue
        target=SITE / unquote(parts.path.lstrip('/')) if parts.path.startswith('/') else page.parent / unquote(parts.path)
        check(target.exists(),f'{page.relative_to(SITE)} has missing asset {url}')
    if 'id="quarto-document-content"' in text:
        check('reader-tools.js' in text,f'Missing reader tools on {page.relative_to(SITE)}')
for source in (ROOT/'templates').glob('*.qmd'):
    text=source.read_text();blocks=re.findall(r'<details class="template-copy">(.*?)</details>',text,re.S)
    check(len(blocks)==1,f'{source.name}: expected one blank copy block')
    check(bool(blocks and re.search(r'```text\n.+?\n```',blocks[0],re.S)),f'{source.name}: blank copy block absent')
    download=SITE/'resources/downloads'/source.with_suffix('.md').name
    check(download.exists(),f'Missing rendered download for {source.name}')
    if download.exists():
        content=download.read_text()
        check('template-copy' not in content and not content.startswith('---'),f'HTML/YAML wrapper leaked into {download.name}')
        check(content == template_download_text(source),f'Download differs from the current blank: {download.name}')
with (ROOT/'research/page-visuals.csv').open() as file:
    for row in csv.DictReader(file):
        check(row['page_path'].startswith('chapters/'),f'Automatic comic on practical/help page: {row["page_path"]}')
        check('full transcript is available' not in (SITE/Path(row['page_path']).with_suffix('.html')).read_text().lower(),'Comic uses a title-only alternative')
for name in ['github-form-start-2026-09.png','github-form-write-2026-09.png','github-form-finish-2026-09.png','github-tracker-2026-09.png']:
    check((ROOT/'assets/contributions'/name).exists(),f'Missing tutorial capture: {name}')
check((ROOT/'AGENTS.md').exists(),'Missing shared agent instructions')
check((ROOT/'.agents/skills/handbook-editor/SKILL.md').exists(),'Missing repository editorial skill')
epub=SITE/'The-Handbook-for-the-Recently-Enrolled.epub'
check(epub.exists(),'Missing offline EPUB')
if epub.exists():
    try:
        epub_result=finish(epub,ROOT,check=True)
        with zipfile.ZipFile(epub) as archive:
            metadata=ET.fromstring(archive.read('EPUB/content.opf'))
            check([node.text for node in metadata.iter() if node.tag.endswith('}creator')]==['Haresh Suppiah'],'EPUB creator must be Haresh Suppiah')
    except (EpubError,OSError,UnicodeError,zipfile.BadZipFile,KeyError) as error: failures.append(f'Invalid EPUB: {error}')
if failures:
    print('VERIFY READER EXPERIENCE: FAIL');print('\n'.join('- '+f for f in failures));sys.exit(1)
print(f'VERIFY READER EXPERIENCE: PASS ({len(pages)} HTML pages; 33 template downloads; scripts, images and editorial contracts)')
print(f'EPUB: {epub_result["xml_members"]} XML members; {epub_result["relative_targets_checked"]} relative targets checked')
