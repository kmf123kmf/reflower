# Reflower

A comfortable reader for plain-text stories that were saved with hard line breaks.

Many text files, such as Project Gutenberg books, old archives and stories exported from forums or
editors, wrap every line at a fixed width like 72 or 80 characters. In a browser or phone that leaves
a narrow, ragged column. Reflower works out which line breaks are just wrapping and which are
intentional. It then re-flows the text into proper paragraphs that fit whatever screen you read on.

**Use it online:** https://kmf123kmf.github.io/reflower/
(or download `index.html` and open it in a browser; it is a single file with no dependencies)

Your files never leave your device. Everything runs locally in the browser.

## Opening a file

- Drag a `.txt` or `.rtf` file onto the page, use **Open**, or click/tap the box on the start screen.
- On desktop you can also paste text with Ctrl+V.
- Recently opened files are listed on the start screen (**Home**). Each file reopens at the place you left off.

## What the reflow handles

The engine makes several passes over the file. It detects:

- **The wrap width**, including files that mix widths between chapters, hand-typed ragged margins,
  justified text, double-spaced files, and "format=flowed" trailing-space wrapping.
- **Paragraphs**, whether they are separated by blank lines, by first-line indents, or only by where
  the lines end.
- **Titles, bylines and chapter headings**, such as `CHAPTER XII.`, `Chapter Twenty-One: The Storm`,
  `Part One`, `Prologue`, Roman numerals, and centred or all-caps headings with their subtitles.
- **Scene breaks** such as `* * *`, `~~~` and `#`.
- **Text whose line breaks are kept:** poems, song lyrics, letters and sign-offs, block quotes,
  tables and ASCII art.
- **Dialogue and abbreviations**, so `"Mrs.` at the end of a line does not end a paragraph.
- **Words hyphenated across lines.**
- **Project Gutenberg extras:** `[Illustration]` notes, and the header and licence, which are folded
  away into collapsed sections.

Text that is not hard-wrapped is left alone.

**RTF files** keep paragraphs, bold/italic, special characters, manual line breaks and headings.
Headers, footers, footnotes, pictures and fonts are dropped. An RTF that is really a hard-wrapped
text file is reflowed too.

## Reading

- **Layouts:**
  - **Scroll:** one continuous page.
  - **Page:** one page at a time.
  - **Spread:** two facing pages, on wide screens.
- **Turning pages:** use the arrow keys, Page Up/Down, Space, the mouse wheel, tapping or clicking
  the page edges, or the scrub bar along the bottom. On touch screens you can also swipe: the page
  follows your finger. Swipes that start right at the screen's edge are left to the browser's own
  back/forward gesture.
- **Back button:** Back (or Safari's edge swipe) returns from a book to Home, and Forward reopens it.
- **Contents:** a list of the detected chapters.
- **Search:** finds every match with its chapter. "Back to where I was" returns you to your place.
- **Settings (Aa):**
  - theme (light, sepia or dark), font, size and line height;
  - left or justified text, spaced or indented paragraphs;
  - smart typography (curly quotes, em dashes, ellipses, `_italics_`);
  - in the paged layouts, whether chapters start on a new page.
- **Page width:** on desktop, drag either edge of the page to change it.
- **Export:** saves the reflowed text as `.txt` or as a standalone `.html` page.
- **Phones:**
  - The page uses the full screen width, and Contents and Search are in the toolbar.
  - The toolbar and scrub bar hide while you read: on a page turn, or when you scroll down.
    Tap the middle of the page, or scroll up, to bring them back. While they're hidden, a thin
    line at the bottom shows your progress.
  - Search opens as a sheet at the top with the text still visible below. Tap a result to jump
    there, or double-tap it to also close the search.
  - For the most reading space, use Safari's **Share → Add to Home Screen**. Reflower then opens
    full screen, without Safari's own bars. On iPhone the home-screen copy keeps its own list of
    recent files, separate from Safari's.

### Keyboard shortcuts (desktop)

| Key | Action |
|---|---|
| `O` | Open a file |
| `H` | Home (recent files) |
| `T` | Contents |
| `/` | Search (Enter / Shift+Enter or F3 / Shift+F3 for next / previous) |
| `1` `2` `3` | Scroll / Page / Spread layout |
| `R` | Toggle Raw view (the original file) |
| `D` | Debug overlay |
| `←` `→` `PgUp` `PgDn` `Space` | Previous / next page |
| `Home` `End` | Start / end of the book |
| `Esc` | Close panels |

## When the reflow gets something wrong

Turn on **Debug** (desktop). Every block in the text is then labelled with what it was detected as
and the source lines it came from. A panel also shows the detected wrap width, whether the file was
judged hard-wrapped, and the passes that ran. In **Raw** view with Debug on, each original line
shows whether it was joined to the next, with the score and reasons on hover. If the width was
misjudged, the Debug panel lets you force a specific wrap width.

## Development

There is no build step. Everything is in `index.html`:

- `<script id="reflow-engine">` contains the reflow engine as pure functions:
  `Reflow.analyze`, `Reflow.fromRTF`, `Reflow.toHTML` and `Reflow.toText`.
- The second script is the user interface.

Tests use Python (to serve files and generate samples) and headless Chrome:

```sh
python tests/make_samples.py              # writes synthetic samples to samples/ + tests/expectations.json
python -m http.server 8765 --bind 127.0.0.1
# then open in a browser, or run headless (see AGENTS.md):
#   http://127.0.0.1:8765/tests/test.html    reflow engine tests
#   http://127.0.0.1:8765/tests/ui.html      UI smoke test / screenshots (supports phone sizes)
#   http://127.0.0.1:8765/tests/bench.html   performance benchmark
```

See [AGENTS.md](AGENTS.md) for the full set of test options and headless Chrome commands.
