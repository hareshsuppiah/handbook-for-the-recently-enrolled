#!/usr/bin/env python3
"""Finish and validate the handbook EPUB without changing its source or metadata.

Run after Quarto: python3 scripts/finish_epub.py --if-present
For a release:    python3 scripts/finish_epub.py PATH.epub
Read-only check:  python3 scripts/finish_epub.py PATH.epub --check

Only simple, single-line chapter entries/titles used by this repository are
accepted. Ambiguous titles, unknown fragments and missing files fail closed.
The original archive is replaced atomically only after all checks pass.
"""
from __future__ import annotations

import argparse
import copy
import html
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import sys
import tempfile
import unicodedata
from urllib.parse import quote, unquote, urlsplit
from zipfile import ZipFile, ZIP_STORED, BadZipFile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EPUB = ROOT / '_site/The-Handbook-for-the-Recently-Enrolled.epub'
XHTML = 'http://www.w3.org/1999/xhtml'
EPUB = 'http://www.idpf.org/2007/ops'
OPF = 'http://www.idpf.org/2007/opf'
DC = 'http://purl.org/dc/elements/1.1/'
XML = 'http://www.w3.org/XML/1998/namespace'
XML_SUFFIXES = {'.xml', '.xhtml', '.html', '.opf', '.ncx', '.svg', '.smil'}
URL_ATTRIBUTES = {'href', 'src', 'poster', 'data', 'cite', 'longdesc', 'full-path'}
ET.register_namespace('', XHTML)
ET.register_namespace('epub', EPUB)
ET.register_namespace('svg', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')


class EpubError(ValueError):
    """A build condition that must be resolved before publishing."""


def local_name(tag: str) -> str:
    return tag.rsplit('}', 1)[-1] if isinstance(tag, str) else ''


def normalise_title(value: str) -> str:
    value = html.unescape(unicodedata.normalize('NFKC', value))
    value = value.translate(str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-'}))
    value = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', value)
    return ' '.join(value.replace('`', '').replace('*', '').split()).casefold()


def scalar(value: str, context: str) -> str:
    value = value.strip()
    if value.startswith('"'):
        try:
            result = json.loads(value)
        except json.JSONDecodeError as exc:
            raise EpubError(f'{context}: unsupported quoted YAML scalar') from exc
        if not isinstance(result, str):
            raise EpubError(f'{context}: expected a string')
        return result
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    if not value or value[0] in '|>[{':
        raise EpubError(f'{context}: use a supported single-line scalar')
    return re.split(r'\s+#', value, maxsplit=1)[0].rstrip()


def read_sources(root: Path) -> dict[str, str]:
    config = (root / '_quarto.yml').read_text(encoding='utf-8')
    match = re.search(r'^book:\s*\n(.*?)(?=^[^\s#]|\Z)', config, re.M | re.S)
    if not match:
        raise EpubError('_quarto.yml: no book configuration')
    paths = []
    for line in match[1].splitlines():
        if '.qmd' not in line:
            continue
        entry = re.fullmatch(r'\s*-\s+(.+?\.qmd[\"\']?)\s*(?:#.*)?', line)
        if not entry:
            raise EpubError(f'Unsupported QMD chapter entry: {line.strip()}')
        path = scalar(entry[1], 'chapter path')
        if posixpath.normpath(path) != path or path.startswith('/') or '\\' in path:
            raise EpubError(f'Unsafe chapter path: {path}')
        paths.append(path)
    if not paths or len(paths) != len(set(paths)):
        raise EpubError('No chapter sources found, or duplicate chapter entries')
    result = {}
    for path in paths:
        source = root / path
        if not source.is_file():
            raise EpubError(f'Missing chapter source: {path}')
        text = source.read_text(encoding='utf-8')
        front = re.match(r'^---\s*\n(.*?)\n---(?:\s*\n|$)', text, re.S)
        title = re.search(r'^title:\s*(.+)$', front[1], re.M) if front else None
        if not title:
            raise EpubError(f'{path}: missing single-line title')
        result[path] = scalar(title[1], path + ' title')
    return result


class WebOnlyRanges(HTMLParser):
    """Locate explicitly web-only divs even before malformed HTML can be XML."""
    def __init__(self, text: str):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.offsets = [0]
        for line in text.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.start = None
        self.depth = 0
        self.ranges = []

    def absolute_offset(self) -> int:
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag != 'div':
            return
        attrs = dict(attrs)
        marked = ('data-route-chooser' in attrs or
                  ('content-visible' in (attrs.get('class') or '').split() and
                   (attrs.get('when-format') or attrs.get('data-when-format')) == 'html'))
        if self.depth:
            self.depth += 1
        elif marked:
            self.start = self.absolute_offset()
            self.depth = 1

    def handle_endtag(self, tag):
        if tag == 'div' and self.depth:
            self.depth -= 1
            if not self.depth:
                self.ranges.append((self.start, self.text.index('>', self.absolute_offset()) + 1))
                self.start = None

    def handle_startendtag(self, tag, attrs):
        if tag == 'div' and not self.depth:
            self.handle_starttag(tag, attrs)
            if self.depth:
                self.handle_endtag(tag)


def remove_web_containers(text: str) -> tuple[str, int]:
    parser = WebOnlyRanges(text)
    parser.feed(text)
    parser.close()
    if parser.depth:
        raise EpubError('Unclosed web-only container; cannot safely remove it')
    for start, end in reversed(parser.ranges):
        text = text[:start] + text[end:]
    return text, len(parser.ranges)


def parse_xml(data: bytes, member: str) -> ET.Element:
    # ElementTree does not fetch external DTDs; reject entity declarations too.
    if b'<!ENTITY' in data:
        raise EpubError(f'{member}: entity declarations are unsupported')
    try:
        return ET.fromstring(data, parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))
    except ET.ParseError as exc:
        raise EpubError(f'{member}: malformed XML: {exc}') from exc


def title_text(node: ET.Element) -> str:
    parts = [node.text or '']
    for child in node:
        if 'header-section-number' not in child.get('class', '').split():
            parts.append(title_text(child))
        parts.append(child.tail or '')
    return ''.join(parts)


def page_map(sources: dict[str, str], trees: dict[str, ET.Element]):
    candidates = {}
    for member, tree in trees.items():
        if not member.endswith(('.xhtml', '.html')):
            continue
        for section in tree.iter():
            if local_name(section.tag) != 'section' or 'level1' not in section.get('class', '').split():
                continue
            headings = [child for child in section if local_name(child.tag) == 'h1']
            if len(headings) != 1 or not section.get('id'):
                raise EpubError(f'{member}: source chapter needs one H1 and a section ID')
            title = normalise_title(title_text(headings[0]))
            candidates.setdefault(title, []).append((member, section.get('id')))
    forward = {}
    reverse = {}
    for source, title in sources.items():
        matches = candidates.get(normalise_title(title), [])
        if len(matches) != 1:
            raise EpubError(f'{source}: title {title!r} maps to {len(matches)} EPUB chapters')
        member, anchor = matches[0]
        if member in reverse:
            raise EpubError(f'{source}: ambiguous title/page also matched by {reverse[member]}')
        forward[source] = (member, anchor)
        reverse[member] = source
    return forward, reverse


def source_web_links(text: str) -> set[str]:
    """Read only links explicitly authored inside an HTML-only fenced div."""
    stack = []
    links = set()
    in_code = None
    for line in text.splitlines():
        stripped = line.strip()
        code = re.match(r'^(`{3,}|~{3,})', stripped)
        if code:
            marker = code[1][0]
            if in_code == marker:
                in_code = None
            elif in_code is None:
                in_code = marker
            continue
        if in_code:
            continue
        if re.match(r'^:{3,}\s*\{', stripped):
            is_web = ('content-visible' in stripped and
                      bool(re.search(r'when-format=[\"\']?html[\"\']?(?:\s|\})', stripped)))
            stack.append(is_web or any(stack))
        elif re.fullmatch(r':{3,}', stripped):
            if stack:
                stack.pop()
        elif any(stack):
            links.update(html.unescape(href) for href in re.findall(r'\]\(([^)]+)\)', line))
    return links


def discard_element(parent: ET.Element, element: ET.Element):
    """Remove a web-only element while preserving the following prose tail."""
    index = list(parent).index(element)
    tail = element.tail or ''
    if index:
        previous = parent[index - 1]
        previous.tail = (previous.tail or '') + tail
    else:
        parent.text = (parent.text or '') + tail
    parent.remove(element)


def transform_page(tree, source, member, root, mapping, ids):
    changes = 0
    web_links = source_web_links((root / source).read_text(encoding='utf-8'))
    parents = {child: parent for parent in tree.iter() for child in parent}
    for element in list(tree.iter()):
        if local_name(element.tag) == 'a' and element.get('href') in web_links:
            parent = parents.get(element)
            # An explicitly HTML-only download paragraph is safe to omit. Never
            # discard surrounding meaningful prose or an anchor-bearing section.
            if (parent is None or local_name(parent.tag) != 'p' or len(parent) != 1 or
                    (parent.text or '').strip() or (element.tail or '').strip() or
                    parent.get('id') or element.get('id')):
                raise EpubError(f'{member}: cannot safely omit web-only link {element.get("href")!r}')
            discard_element(parents[parent], parent)
            changes += 1
    for element in tree.iter():
        tag = local_name(element.tag)
        if tag in {'details', 'summary'}:
            element.tag = f'{{{XHTML}}}' + ('div' if tag == 'details' else 'p')
            classes = element.get('class', '').split()
            classes.append('offline-details' if tag == 'details' else 'offline-summary')
            element.set('class', ' '.join(dict.fromkeys(classes)))
            for attr in ('open', 'name', 'aria-expanded', 'aria-controls', 'role', 'tabindex', 'hidden'):
                element.attrib.pop(attr, None)
            if tag == 'summary':
                element.set('style', element.get('style', '').rstrip(';') + ';font-weight: bold;')
            changes += 1
        for attr, value in list(element.attrib.items()):
            if local_name(attr) not in {'href', 'src'}:
                continue
            url = urlsplit(value)
            if url.scheme or url.netloc or not url.path.lower().endswith('.qmd'):
                continue
            if url.query:
                raise EpubError(f'{member}: local QMD query cannot be resolved offline: {value}')
            path = unquote(url.path)
            if '\\' in path:
                raise EpubError(f'{member}: non-POSIX QMD path: {value}')
            target = posixpath.normpath(path.lstrip('/') if path.startswith('/') else posixpath.join(posixpath.dirname(source), path))
            if target not in mapping:
                raise EpubError(f'{member}: unmapped source link {value!r} (source target {target!r})')
            destination, main_anchor = mapping[target]
            fragment = unquote(url.fragment) if url.fragment else main_anchor
            if fragment not in ids[destination]:
                raise EpubError(f'{member}: no EPUB fragment {fragment!r} in {target}; refusing to drop it')
            relative = posixpath.relpath(destination, posixpath.dirname(member))
            element.set(attr, quote(relative, safe='/.-_~') + '#' + quote(fragment, safe='-._~'))
            changes += 1
    return changes


def xml_members(data: dict[str, bytes]) -> set[str]:
    members = {name for name in data if PurePosixPath(name).suffix.lower() in XML_SUFFIXES}
    for name in list(members):
        if not name.endswith('.opf'):
            continue
        tree = parse_xml(data[name], name)
        for item in tree.findall(f'{{{OPF}}}manifest/{{{OPF}}}item'):
            media = item.get('media-type', '')
            if media.endswith('+xml') or media in {'text/xml', 'application/xml'}:
                href = item.get('href', '')
                if not urlsplit(href).scheme:
                    members.add(posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(urlsplit(href).path))))
    missing = members - data.keys()
    if missing:
        raise EpubError('Missing XML package members: ' + ', '.join(sorted(missing)))
    return members


def collect_ids(trees):
    ids = {}
    for name, tree in trees.items():
        values = [e.get('id') or e.get(f'{{{XML}}}id') for e in tree.iter() if e.get('id') or e.get(f'{{{XML}}}id')]
        if len(values) != len(set(values)):
            raise EpubError(f'{name}: duplicate XML IDs')
        ids[name] = set(values)
    return ids


def relative_target(member, value, root_relative=False):
    url = urlsplit(value)
    if url.scheme or url.netloc:
        return None
    if '\\' in url.path or url.path.startswith('/'):
        raise EpubError(f'{member}: invalid package-relative URL {value!r}')
    path = unquote(url.path)
    target = posixpath.normpath(posixpath.join('' if root_relative else posixpath.dirname(member), path)) if path else member
    if target.startswith('../') or target in {'..', '.'}:
        raise EpubError(f'{member}: URL escapes the EPUB package: {value!r}')
    return target, unquote(url.fragment)


def css_urls(text):
    for match in re.finditer(r'url\(\s*(?:"([^\"]*)"|\'([^\']*)\'|([^\s)]*))\s*\)', text, re.I):
        yield next(group for group in match.groups() if group is not None)
    for match in re.finditer(r'@import\s+(?:"([^\"]*)"|\'([^\']*)\')', text, re.I):
        yield match[1] if match[1] is not None else match[2]


def validate_data(data: dict[str, bytes], language='en-AU') -> dict[str, int]:
    if data.get('mimetype') != b'application/epub+zip':
        raise EpubError('mimetype must contain exactly application/epub+zip')
    trees = {name: parse_xml(data[name], name) for name in sorted(xml_members(data))}
    ids = collect_ids(trees)
    checked = 0

    def check_url(member, value, root_relative=False):
        nonlocal checked
        if not value:
            return
        resolved = relative_target(member, value, root_relative)
        if resolved is None:
            return
        target, fragment = resolved
        if urlsplit(value).path.lower().endswith('.qmd'):
            raise EpubError(f'{member}: unfinished QMD link {value!r}')
        if target not in data:
            raise EpubError(f'{member}: missing package target {value!r} -> {target}')
        if fragment and fragment not in ids.get(target, set()):
            raise EpubError(f'{member}: missing fragment {fragment!r} in {target}')
        checked += 1

    for name, tree in trees.items():
        if local_name(tree.tag) == 'html':
            if tree.get('lang') != language or tree.get(f'{{{XML}}}lang') != language:
                raise EpubError(f'{name}: language must be {language}; set lang in Quarto and rebuild')
        for element in tree.iter():
            if local_name(element.tag) in {'details', 'summary'}:
                raise EpubError(f'{name}: unexpanded offline disclosure')
            if 'data-route-chooser' in element.attrib:
                raise EpubError(f'{name}: web-only route chooser remains')
            if f'{{{XML}}}base' in element.attrib:
                raise EpubError(f'{name}: xml:base requires explicit URL resolution support')
            for attr, value in element.attrib.items():
                key = local_name(attr)
                if key in URL_ATTRIBUTES:
                    check_url(name, value, root_relative=key == 'full-path')
                elif key == 'style':
                    for url in css_urls(value):
                        check_url(name, url)
                elif key == 'srcset':
                    # Do not guess around commas in data-URI candidates.
                    if 'data:' in value:
                        raise EpubError(f'{name}: data-URI srcset needs explicit validation support')
                    for candidate in value.split(','):
                        fields = candidate.strip().split()
                        if fields:
                            check_url(name, fields[0])
            if local_name(element.tag) == 'style':
                for url in css_urls(''.join(element.itertext())):
                    check_url(name, url)
    for name, content in data.items():
        if name.endswith('.css'):
            for url in css_urls(content.decode('utf-8')):
                check_url(name, url)
    container = trees.get('META-INF/container.xml')
    if container is None:
        raise EpubError('Missing META-INF/container.xml')
    rootfiles = [e.get('full-path') for e in container.iter() if local_name(e.tag) == 'rootfile']
    if not rootfiles:
        raise EpubError('Container has no package document')
    for package_name in rootfiles:
        package = trees.get(package_name)
        if package is None or package.tag != f'{{{OPF}}}package':
            raise EpubError(f'Invalid package document: {package_name}')
        if package.get(f'{{{XML}}}lang') != language:
            raise EpubError(f'{package_name}: package language must be {language}; rebuild the EPUB')
        langs = [e.text for e in package.findall(f'{{{OPF}}}metadata/{{{DC}}}language')]
        if language not in langs or 'C' in langs:
            raise EpubError(f'{package_name}: invalid language metadata {langs!r}; rebuild the EPUB')
        items = package.findall(f'{{{OPF}}}manifest/{{{OPF}}}item')
        manifest = {item.get('id'): item for item in items}
        if None in manifest or len(manifest) != len(items):
            raise EpubError(f'{package_name}: duplicate or missing manifest IDs')
        for itemref in package.findall(f'{{{OPF}}}spine/{{{OPF}}}itemref'):
            if itemref.get('idref') not in manifest:
                raise EpubError(f'{package_name}: unknown spine idref {itemref.get("idref")!r}')
        spine = package.find(f'{{{OPF}}}spine')
        if spine is not None and spine.get('toc') and spine.get('toc') not in manifest:
            raise EpubError(f'{package_name}: unknown NCX manifest reference')
    return {'xml_members': len(trees), 'relative_targets_checked': checked}


def read_archive(raw: bytes):
    with ZipFile(io.BytesIO(raw)) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(names) != len(set(names)):
            raise EpubError('Duplicate ZIP member names')
        for name in names:
            normal = posixpath.normpath(name.rstrip('/'))
            if name.startswith('/') or '\\' in name or normal.startswith('../') or normal != name.rstrip('/'):
                raise EpubError(f'Unsafe ZIP member path: {name!r}')
        bad = archive.testzip()
        if bad:
            raise EpubError(f'ZIP CRC failure: {bad}')
        data = {info.filename: archive.read(info) for info in infos if not info.is_dir()}
        return infos, archive.comment, data


def validate_archive(raw: bytes, language='en-AU'):
    infos, _, data = read_archive(raw)
    if not infos or infos[0].filename != 'mimetype' or infos[0].compress_type != ZIP_STORED or infos[0].extra:
        raise EpubError('mimetype must be the first uncompressed ZIP entry, with no extra field')
    return validate_data(data, language)


def finish(path: Path, root: Path = ROOT, language='en-AU', check=False):
    original = path.read_bytes()
    if check:
        return {'state': 'checked', **validate_archive(original, language)}
    infos, comment, data = read_archive(original)
    rewritten = dict(data)
    removals = 0
    trees = {}
    initial_changes = set()
    for name in sorted(xml_members(data)):
        content = data[name]
        if name.endswith(('.xhtml', '.html')):
            text, count = remove_web_containers(content.decode('utf-8'))
            if count:
                initial_changes.add(name)
                removals += count
                content = text.encode('utf-8')
        trees[name] = parse_xml(content, name)
    mapping, reverse = page_map(read_sources(root), trees)
    ids = collect_ids(trees)
    changes = 0
    for name, source in reverse.items():
        count = transform_page(trees[name], source, name, root, mapping, ids)
        if count or name in initial_changes:
            rewritten[name] = b'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n' + ET.tostring(trees[name], encoding='utf-8') + b'\n'
            changes += count
    if initial_changes - reverse.keys():
        raise EpubError('Web-only content appeared in an unmapped EPUB document')
    result = validate_data(rewritten, language)
    changed_members = sum(rewritten[name] != data[name] for name in data)
    valid_mimetype = bool(infos and infos[0].filename == 'mimetype' and infos[0].compress_type == ZIP_STORED and not infos[0].extra)
    if not changed_members and valid_mimetype:
        return {'state': 'unchanged', 'mapped_pages': len(mapping), **result}
    buffer = io.BytesIO()
    with ZipFile(buffer, 'w') as output:
        output.comment = comment
        ordered = [i for i in infos if i.filename == 'mimetype'] + [i for i in infos if i.filename != 'mimetype']
        for original_info in ordered:
            info = copy.copy(original_info)
            if info.filename == 'mimetype':
                info.compress_type = ZIP_STORED
                info.extra = b''
            output.writestr(info, rewritten.get(info.filename, b''))
    completed = buffer.getvalue()
    validate_archive(completed, language)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.finish-epub-', suffix='.epub', dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(completed)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, path.stat().st_mode & 0o777)
        if path.read_bytes() != original:
            raise EpubError('EPUB changed during finishing; preserve the newer render and rerun')
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return {'state': 'finished', 'mapped_pages': len(mapping), 'changed_members': changed_members,
            'web_containers_removed': removals, 'link_or_disclosure_changes': changes, **result}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('epub', nargs='?', type=Path, default=DEFAULT_EPUB)
    parser.add_argument('--source-root', type=Path, default=ROOT)
    parser.add_argument('--check', action='store_true', help='Validate without rewriting')
    parser.add_argument('--if-present', action='store_true', help='Skip when an HTML-only render produced no EPUB')
    args = parser.parse_args()
    try:
        if not args.epub.exists() and args.if_present and not args.check:
            print('FINISH EPUB: SKIP (no EPUB present; HTML-only render)')
            return 0
        result = finish(args.epub, args.source_root, check=args.check)
        print('FINISH EPUB: PASS ' + json.dumps(result, sort_keys=True))
        return 0
    except (EpubError, OSError, BadZipFile, UnicodeError) as exc:
        print('FINISH EPUB: FAIL ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
