# Responsive navigation verification

Verified on 28 August 2026 against the locally rendered Quarto site.

## Required behaviour

- Desktop: the illustrated cover, search and full book contents remain in the left rail; the chapter table of contents remains in the right rail.
- Tablet: the illustrated cover, search and complete book contents remain permanently visible in a fixed left rail; `On this page` remains expanded inline below the page title.
- Phone: a small `Book contents` button opens the drawer because a permanent 100-page rail cannot coexist with a readable 390 px column; `On this page` remains expanded inline.
- The compact Quarto title and `On this page` dropdown bars are hidden at every width.
- All widths: the reading column remains inside the viewport without horizontal clipping.

## Checks completed

| Viewport | Book contents | Page contents | Horizontal overflow | Result |
|---|---|---|---|---|
| 1440 × 1000 | Persistent left rail | Persistent right rail | None observed | Pass |
| 800 × 900 | Persistent fixed left rail with cover, search and full navigation | Inline two-column list; duplicate right rail suppressed | None observed | Pass |
| 390 × 844 | Small labelled drawer button; no full-width dropdown bar | Inline single-column list generated from page headings | None observed | Pass |

The phone drawer was opened and all 12 Parts, Practical resources and References remained reachable. The 800 px tablet view retained the complete navigation without covering or clipping the reading column. The responsive behaviour is implemented in `includes/responsive-navigation.html` and `styles.scss`.

This report covers responsive navigation only. It does not close the broader accessibility, keyboard, search, link or print audits.
