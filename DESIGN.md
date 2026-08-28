# Design direction

## Approved direction

The website uses the reading structure Haresh identified in *R for the Rest of Us*: cover and search in the left sidebar, a clear central reading column, and a sticky “On this page” index on the right. The interface is white, black and quiet grey. It does not reproduce the older cream, oxblood and serif styling.

The cover remains a distinct illustrative asset. Haresh approved concept C, the research crossroads, on 28 August 2026. It may recall the broad category of an uncanny manual but must not reproduce the *Beetlejuice* prop, its illustration, layout, lettering, figures or distinctive details.

## Reading contract

The book is for sustained reading and practical use. The interface should disappear behind the content. The left rail is approximately 320 px with the cover and local search. The main text is approximately 720 px. The right rail is approximately 220 px and provides a sticky local index titled “On this page”. At tablet widths, the full book contents remain permanently visible in a narrower left rail and the chapter contents appear expanded below the title. The compact Quarto dropdown bars are never shown. On a phone, where a permanent 100-page rail cannot coexist with readable text, a small **Book contents** button opens the navigation drawer and the chapter contents remain expanded below the title. The reading column uses the available width without horizontal clipping.

The sidebar contains no social, repository or reader-mode icon row. Reader feedback is reached through a clearly labelled page in the book.

## Tokens

- Page and sidebar: `#ffffff`
- Ink: `#171717`
- Muted ink: `#666666`
- Quiet surface: `#f7f7f7`
- Rule: `#dedede`
- Link: `#111111`
- Focus: `#111111`

Headings, body copy and interface labels use IBM Plex Sans with the native system stack as fallback, matching the reference book's lighter, more open reading texture. Headings use 700 weight with restrained negative tracking. Links are black with visible grey underlines. Shadows are absent. Rules are neutral grey. Corners are modest and never pill-shaped. The illustrated cover is the only deliberately atmospheric element.

## Cover assets

- Selected artwork: `assets/cover-artwork.png`
- Deterministic title composition source: `assets/cover.svg`
- Self-contained web cover: `assets/cover-final.png`
- Alt text: “A worn dark-brown handbook cover. A graduate researcher stands before four paths leading towards library stacks, a laboratory, an archive and a staircase.”
