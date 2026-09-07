#!/usr/bin/env python3
"""Build portable Markdown from each template's one authoritative blank block."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'resources/downloads'

def template_download_text(source: Path) -> str:
    text = source.read_text(encoding='utf-8')
    title = re.search(r'^title:\s*[\"\']?(.*?)[\"\']?$', text, re.M)[1]
    blocks = re.findall(r'<details class="template-copy">(.*?)</details>', text, re.S)
    if len(blocks) != 1:
        raise ValueError(f'{source.name}: expected exactly one template-copy block')
    blanks = re.findall(r'```text\n(.*?)\n```', blocks[0], re.S)
    if len(blanks) != 1 or not blanks[0].strip():
        raise ValueError(f'{source.name}: expected exactly one nonempty blank text block')
    return ('# ' + title + '\n\nFrom The Handbook for the Recently Enrolled, edited by Haresh Suppiah. CC BY 4.0.\n\n'
            + blanks[0].strip() + '\n\nGuidance: https://hareshsuppiah.github.io/handbook-for-the-recently-enrolled/templates/' + source.stem + '.html\n')

def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = sorted((ROOT / 'templates').glob('*.qmd'))
    for source in sources:
        (OUTPUT / (source.stem+'.md')).write_text(template_download_text(source),encoding='utf-8')
    lines = ['::: {.resource-catalogue}', '', '| Resource | Kind |', '|---|---|']
    for folder, kind in [('checklists','Checklist or decision aid'),('templates','Editable template')]:
        for source in sorted((ROOT/folder).glob('*.qmd')):
            if source.stem == 'index': continue
            title = re.search(r'^title:\s*[\"\']?(.*?)[\"\']?$', source.read_text(), re.M)[1]
            lines.append(f'| [{title}]({folder}/{source.name}) | {kind} |')
    lines.extend(['', ':::', ''])
    (ROOT/'includes/resource-catalogue.qmd').write_text('\n'.join(lines))
    print('Built',len(sources),'downloadable templates and the complete resource catalogue')

if __name__ == '__main__':
    main()
