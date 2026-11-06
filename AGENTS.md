# Reflower

Single-file local web app (`index.html`, nothing to install or fetch, works from `file://`; StPageFlip is inlined) that reflows
hard-wrapped story text files. Drag a `.txt` or `.rtf` onto the page.

RTF support: `Reflow.fromRTF(src)` converts RTF to plain text (bold/italic as `**x**`/`_x_`)
plus `hints` (line index -> `heading` | `center` | `verse`) that `Reflow.analyze(text, { hints })`
honours. The UI routes files ending `.rtf` or starting `{\rtf` through it.

Recent files: each opened file's source is kept in IndexedDB (one per file name, so an edited file replaces its old copy and keeps its position; 8 newest, ≤30M chars, storage marked
persistent via `navigator.storage.persist()`). The book open when the page was left reopens on return
(`reflower.lastOpen` in localStorage, cleared by Home; `restoreLast()`); leaving from Home stays Home.

Search (`/` or the Search button) is a literal, case-insensitive find over the rendered text:
`Reflow.searchFold` / `Reflow.searchPattern` (engine, unit-tested) build the matcher; the UI scans
`doc.blocks` in ~8 ms slices and marks matches with the CSS Custom Highlight API (no DOM changes).
Search never changes the page's geometry: on wide windows the panel floats over the page and shrinks to
its find bar (`.mini`, `.low` at the bottom) when it would cover the match; on phones it is one sheet anchored
at the bottom (above the keyboard, `--kb`); picking a result folds the list away (`.mini`), leaving the search row.

Page turns are StPageFlip's curl on a throwaway book (`openFlip`): the column strip stays the only real text, and `setPage` still
moves it at once underneath. `flipPage` copies the blocks on a page into absolutely placed fragments that match the strip to the pixel,
so the hand-over at the end of a turn doesn't jump. Back turns in Page layout are forward turns in a mirrored book (`#flip.mirror`), hinged on the right. The text CSS is `:is(#content, .ftext)` so the copies get it. Mouse drags start at the
page's corners (elsewhere a drag selects text). Reduced motion: no book; turns are instant and a swipe moves the strip.

## Layout
- `index.html` – everything. `<script id="reflow-engine">` holds the pure reflow engine
  (`Reflow.analyze / toHTML / toText`, no DOM access); `<script id="page-flip">` is StPageFlip 2.0.7, patched so its frame loop
  stops with its book (see the note above it); the third script is the UI.
- `tests/make_samples.py` – generates synthetic hard-wrapped samples into `samples/` and
  `tests/expectations.json`.
- `tests/test.html` – engine test page (extracts the engine from `index.html`).
- `tests/ui.html` – UI smoke test / screenshot harness (loads the app in an iframe and opens the
  sample through a simulated file drop, so `.rtf` samples work too). `&search=<text>&next=N` drives
  the search panel (`&tap=N` taps a result row, `&fb=1` steps with the folded phone search row, unfolds it and drags the list, `&close=1` then closes it and samples the current match's fade-out; every run checks the text never moves and the match isn't covered), `&scrub=<value>&hover=<0..1>` the bottom scrub bar, `&toc=<n>` the Contents, `&fonts=1` lists the
  font menu here and as it would be on typical macOS / Linux font sets; run it with `--force-prefers-reduced-motion` (see the note in the file).
- `tests/bench.html` – performance benchmark (needs `samples/real/pg1342.txt`).
- `samples/real/` – optional real Project Gutenberg files for manual checks (not generated).

## Verification (no Node on this machine; use Python + headless Chrome)
```
python tests/make_samples.py
python tests/serve.py                              # keep running (no-cache static server + /__hold)
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
"$CHROME" --headless=new --disable-gpu --user-data-dir="$TEMP/reflower-chrome" --virtual-time-budget=10000 \
  --dump-dom "http://127.0.0.1:8765/tests/test.html" | grep -E "FAIL|PASSED|ERROR"
```
- `test.html?v=<sample>` prints reflowed text, `?trace=<sample>` prints per-line join decisions,
  `?file=real/pg1342.txt[&v=trace]` analyses an arbitrary file under `samples/`.
- Phone widths: headless Chrome won't go below a 500px window, so use `ui.html?...&w=390&h=844`
  (sizes the app's iframe). Every ui.html run prints a `fit @Npx` line flagging toolbar buttons or the
  page cut off sideways; `&click=btnSettings,btnTocTb` opens panels and reports whether they fit.
  The compact layout (CSS `@media (max-width: 700px)` + JS `compactMQ`) hides Spread/Raw/Debug.
  Auto-hiding bars (`body.autohide` from JS `autoMQ`: compact width or a short touch screen) float the
  toolbar/scrub bar over the text; `&chrome=1` taps through hide/show and checks page breaks don't move.
  `&swipe=1` drives synthetic touch drags (follow, spring back, flick, edge margin, vertical; run it with `--force-prefers-reduced-motion`, or the strip won't follow: the book does);
  `&flip=1&layout=page|spread&hold=/__hold` (no budget, no reduced-motion flag) checks the page-turn book opens, closes and survives a layout change;
  `&hist=1` checks Home / Back / Forward (each opened book pushes a history entry; Home goes back `depth` entries, all the way Home) and Recent's one-entry-per-name;
  `&restore=1` reloads with a book open (must reopen at the same page) and after Home (must stay Home).
- Use a fresh `--user-data-dir` per run (e.g. `"$TEMP/rf-$RANDOM"`) when testing edits: a reused
  profile can serve a cached `index.html` (`tests/serve.py` sends no-store; plain `http.server` doesn't).
- `--virtual-time-budget` runs render no frames: `requestAnimationFrame` and `ResizeObserver` never fire,
  so anything behind `scheduleRelayout()` is untested that way. For those, drop the budget and add
  `&hold=/__hold` (served slowly by `tests/serve.py`, so `--dump-dom` waits in real time), e.g.
  `ui.html?sample=gutenberg_72.txt&hold=/__hold&inset=34&w=430&h=932`: `&inset=N` shrinks the page area
  with no resize event (as iOS home-screen apps do when applying safe-area insets) and checks the paged
  layout re-fits instead of clipping its bottom line.
- Screenshots: `--window-size=1400,900 --screenshot=out.png "http://127.0.0.1:8765/tests/ui.html?sample=gutenberg_72.txt&layout=spread&page=1&debug=1"`.
