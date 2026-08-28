# Responsive navigation verification

Verified on 28 August 2026 against the locally rendered Quarto site.

## Required behaviour

- Desktop: the illustrated cover, search and full book contents remain in the left rail; the chapter table of contents remains in the right rail.
- Compact and mobile: a visible `Contents` control opens the full book-navigation drawer; `On this page` remains visible inline below the page title.
- All widths: the reading column remains inside the viewport without horizontal clipping.

## Checks completed

| Viewport | Book contents | Page contents | Horizontal overflow | Result |
|---|---|---|---|---|
| 1440 × 1000 | Persistent left rail | Persistent right rail | None observed | Pass |
| 900 × 900 | Labelled drawer control | Inline two-column list; duplicate right rail suppressed | None observed | Pass |
| 700 × 900 | Labelled drawer control | Inline two-column list | None observed | Pass |
| 390 × 844 | Labelled drawer control; long Part titles wrap | Inline single-column list | None observed | Pass |

The compact drawer was opened at mobile width and all 12 Parts, Practical resources and References remained reachable. The responsive behaviour is implemented in `includes/responsive-navigation.html` and `styles.scss`.

This report covers responsive navigation only. It does not close the broader accessibility, keyboard, search, link or print audits.
