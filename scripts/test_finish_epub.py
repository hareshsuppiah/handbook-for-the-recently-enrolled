#!/usr/bin/env python3
"""Exercise EPUB repairs, protected archive content, and fail-before-write cases."""
from pathlib import Path
import copy
import io
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED, ZIP_STORED
import xml.etree.ElementTree as ET

import finish_epub as f


def xhtml(body, language='en-AU'):
    return (f'<html xmlns="{f.XHTML}" xmlns:epub="{f.EPUB}" lang="{language}" xml:lang="{language}"><head><title>Test</title><link href="../styles/main.css" rel="stylesheet" /></head><body>{body}</body></html>').encode()


class FinishTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root/'chapters').mkdir()
        (self.root/'_quarto.yml').write_text('book:\n  chapters:\n    - index.qmd\n    - "chapters/second page.qmd"\nformat:\n  epub: default\n')
        (self.root/'index.qmd').write_text('---\ntitle: "I\'m first"\n---\n::: {.content-visible when-format="html"}\n[Download](Test.epub)\n:::\n')
        (self.root/'chapters/second page.qmd').write_text('---\ntitle: "Second page"\n---\n')
        self.path = self.root/'Test.epub'
        self.data = {
            'mimetype': b'application/epub+zip',
            'META-INF/container.xml': b'<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/content.opf" /></rootfiles></container>',
            'EPUB/content.opf': (f'<package xmlns="{f.OPF}" xmlns:dc="{f.DC}" xml:lang="en-AU"><metadata><dc:language>en-AU</dc:language><dc:title>Preserve this title</dc:title></metadata><manifest><item id="first" href="text/ch001.xhtml" media-type="application/xhtml+xml"/><item id="second" href="text/ch002.xhtml" media-type="application/xhtml+xml"/><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml"/><item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/><item id="css" href="styles/main.css" media-type="text/css"/><item id="art" href="media/art.svg" media-type="image/svg+xml"/></manifest><spine toc="ncx"><itemref idref="first"/><itemref idref="second"/></spine></package>').encode(),
            'EPUB/nav.xhtml': (f'<html xmlns="{f.XHTML}" xmlns:epub="{f.EPUB}" lang="en-AU" xml:lang="en-AU"><head><title>Contents</title></head><body><nav hidden="hidden" epub:type="landmarks"><a href="text/ch001.xhtml#first">Beginning</a></nav></body></html>').encode(),
            'EPUB/toc.ncx': b'<ncx><navMap><navPoint><content src="text/ch002.xhtml#target"/></navPoint></navMap></ncx>',
            'EPUB/styles/main.css': b'body { color: black; background-image: url("../media/art.svg#icon"); }',
            'EPUB/media/art.svg': b'<svg xmlns="http://www.w3.org/2000/svg"><g id="icon" /></svg>',
            'EPUB/text/title_page.xhtml': xhtml('<h1>I’m first</h1>'),
            'EPUB/text/ch001.xhtml': xhtml('<section class="level1" id="first"><h1><span class="header-section-number">1</span> I’m first</h1><div data-route-chooser="true" hidden="hidden"><div><select><option value>Web chooser</option></select></div></div><p>Keep the text after the chooser.</p><p><a href="chapters/second%20page.qmd#target">Second section</a></p><p><a href="https://example.org/source.qmd?x=1&amp;y=2#frag">External</a></p><p><a href="Test.epub">Download</a></p><details id="practice"><summary>Outer prompt</summary>Before inner.<details><summary>Inner prompt</summary><p>Nested answer.</p></details>After inner.</details><img src="../media/art.svg#icon" alt="Test diagram" /></section>'),
            'EPUB/text/ch002.xhtml': xhtml('<section class="level1" id="second"><h1><span class="header-section-number">2</span> Second page</h1><section id="target"><h2>Target</h2><a href="../index.qmd">Home</a></section></section>'),
        }
        self.write_archive()

    def tearDown(self):
        self.temporary.cleanup()

    def write_archive(self):
        with ZipFile(self.path, 'w') as z:
            z.comment = b'Preserve archive comment'
            for name, data in self.data.items():
                info = ZipInfo(name, (2024, 2, 3, 4, 5, 6))
                info.compress_type = ZIP_STORED if name == 'mimetype' else ZIP_DEFLATED
                info.comment = b'entry comment'
                info.external_attr = 0o100644 << 16
                z.writestr(info, data)

    def fail_unchanged(self, pattern):
        self.write_archive()
        before = self.path.read_bytes()
        with self.assertRaisesRegex(f.EpubError, pattern):
            f.finish(self.path, self.root)
        self.assertEqual(before, self.path.read_bytes())

    def test_repairs_are_visible_precise_preserved_and_idempotent(self):
        before = self.path.read_bytes()
        result = f.finish(self.path, self.root)
        self.assertEqual(result['state'], 'finished')
        with ZipFile(io.BytesIO(before)) as old, ZipFile(self.path) as new:
            self.assertEqual(old.comment, new.comment)
            self.assertEqual(old.namelist(), new.namelist())
            for member in self.data:
                a, b = old.getinfo(member), new.getinfo(member)
                for field in ('date_time', 'compress_type', 'comment', 'external_attr', 'create_system', 'extra'):
                    self.assertEqual(getattr(a, field), getattr(b, field), (member, field))
                if member not in {'EPUB/text/ch001.xhtml', 'EPUB/text/ch002.xhtml'}:
                    self.assertEqual(old.read(member), new.read(member), member)
            tree = ET.fromstring(new.read('EPUB/text/ch001.xhtml'))
            tags = [f.local_name(e.tag) for e in tree.iter()]
            self.assertNotIn('details', tags)
            self.assertNotIn('summary', tags)
            text = ''.join(tree.itertext())
            for phrase in ('Keep the text after the chooser.', 'Outer prompt', 'Before inner.', 'Nested answer.', 'After inner.'):
                self.assertIn(phrase, text)
            self.assertNotIn('Web chooser', text)
            self.assertNotIn('Download', text)
            hrefs = [e.get('href') for e in tree.iter() if e.get('href')]
            self.assertIn('ch002.xhtml#target', hrefs)
            self.assertIn('https://example.org/source.qmd?x=1&y=2#frag', hrefs)
            self.assertIn(b'ch001.xhtml#first', new.read('EPUB/text/ch002.xhtml'))
        complete = self.path.read_bytes()
        self.assertEqual(f.finish(self.path, self.root)['state'], 'unchanged')
        self.assertEqual(complete, self.path.read_bytes())
        self.assertEqual(f.finish(self.path, self.root, check=True)['state'], 'checked')

    def test_missing_fragment_never_dropped(self):
        self.data['EPUB/text/ch001.xhtml'] = self.data['EPUB/text/ch001.xhtml'].replace(b'.qmd#target', b'.qmd#absent')
        self.fail_unchanged('no EPUB fragment')

    def test_unmapped_qmd_never_redirected(self):
        self.data['EPUB/text/ch001.xhtml'] = self.data['EPUB/text/ch001.xhtml'].replace(b'second%20page.qmd', b'unknown.qmd')
        self.fail_unchanged('unmapped source link')

    def test_css_asset_and_fragment_are_checked(self):
        for asset in ('absent.svg', 'art.svg#absent'):
            with self.subTest(asset=asset):
                self.data['EPUB/styles/main.css'] = ('body { background: url("../media/'+asset+'"); }').encode()
                self.fail_unchanged('missing package target|missing fragment')

    def test_ncx_and_spine_are_checked(self):
        self.data['EPUB/toc.ncx'] = b'<ncx><content src="text/ch099.xhtml#target"/></ncx>'
        self.fail_unchanged('missing package target')
        self.data['EPUB/toc.ncx'] = b'<ncx><content src="text/ch002.xhtml#target"/></ncx>'
        self.data['EPUB/content.opf'] = self.data['EPUB/content.opf'].replace(b'idref="first"', b'idref="absent"')
        self.fail_unchanged('unknown spine idref')

    def test_unrelated_malformed_xml_is_not_normalised(self):
        self.data['EPUB/text/ch002.xhtml'] = self.data['EPUB/text/ch002.xhtml'].replace(b'<h2>Target</h2>', b'<input disabled>')
        self.fail_unchanged('malformed XML')

    def test_duplicate_ids_and_titles_fail(self):
        original = self.data['EPUB/text/ch002.xhtml']
        self.data['EPUB/text/ch002.xhtml'] = original.replace(b'<h2>Target</h2>', b'<h2 id="target">Target</h2>')
        self.fail_unchanged('duplicate XML IDs')
        self.data['EPUB/text/ch002.xhtml'] = original.replace(b'Second page', 'I’m first'.encode())
        self.fail_unchanged('maps to 2 EPUB chapters')

    def test_invalid_language_is_not_silently_changed(self):
        self.data['EPUB/content.opf'] = self.data['EPUB/content.opf'].replace(b'<dc:language>en-AU', b'<dc:language>C')
        self.fail_unchanged('invalid language metadata')

    def test_local_query_requires_explicit_resolution(self):
        self.data['EPUB/text/ch001.xhtml'] = self.data['EPUB/text/ch001.xhtml'].replace(b'.qmd#target', b'.qmd?mode=edit#target')
        self.fail_unchanged('query cannot be resolved offline')

    def test_root_relative_qmd_is_resolved(self):
        self.data['EPUB/text/ch002.xhtml'] = self.data['EPUB/text/ch002.xhtml'].replace(b'../index.qmd', b'/index.qmd')
        self.write_archive()
        f.finish(self.path, self.root)
        with ZipFile(self.path) as z:
            self.assertIn(b'ch001.xhtml#first', z.read('EPUB/text/ch002.xhtml'))

    def test_check_rejects_duplicate_archive_entries(self):
        with ZipFile(self.path, 'a') as z:
            with self.assertWarns(UserWarning):
                z.writestr('EPUB/media/art.svg', b'<svg/>')
        with self.assertRaisesRegex(f.EpubError, 'Duplicate ZIP member'):
            f.finish(self.path, self.root, check=True)

    def test_missing_epub_can_skip_only_for_render_hook(self):
        command = [sys.executable, str(Path(f.__file__).resolve()), str(self.root/'missing.epub')]
        self.assertEqual(subprocess.run(command+['--if-present'], capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(command+['--if-present', '--check'], capture_output=True).returncode, 1)


if __name__ == '__main__':
    unittest.main()
