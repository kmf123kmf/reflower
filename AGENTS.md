# Reflower

Single-file local web app (`index.html`, no dependencies, works from `file://`) that reflows
hard-wrapped story text files. Drag a `.txt` or `.rtf` onto the page.

RTF support: `Reflow.fromRTF(src)` converts RTF to plain text (bold/italic as `**x**`/`_x_`)
plus `hints` (line index -> `heading` | `center` | `verse`) that `Reflow.analyze(text, { hints })`
honours. The UI routes files ending `.rtf` or starting `{\rtf` through it.

Search (`/` or the Search button) is a literal, case-insensitive find over the rendered text:
`Reflow.searchFold` / `Reflow.searchPattern` (engine, unit-tested) build the matcher; the UI scans
`doc.blocks` in ~8 ms slices and marks matches with the CSS Custom Highlight API (no DOM changes).

## Layout
- `index.html` – everything. `<script id="reflow-engine">` holds the pure reflow engine
  (`Reflow.analyze / toHTML / toText`, no DOM access); the second script is the UI.
- `tests/make_samples.py` – generates synthetic hard-wrapped samples into `samples/` and
  `tests/expectations.json`.
- `tests/test.html` – engine test page (extracts the engine from `index.html`).
- `tests/ui.html` – UI smoke test / screenshot harness (loads the app in an iframe and opens the
  sample through a simulated file drop, so `.rtf` samples work too). `&search=<text>&next=N` drives
  the search panel, `&scrub=<value>&hover=<0..1>` the bottom scrub bar, `&toc=<n>` the Contents, `&fonts=1` lists the
  font menu here and as it would be on typical macOS / Linux font sets; run it with `--force-prefers-reduced-motion` (see the note in the file).
- `tests/bench.html` – performance benchmark (needs `samples/real/pg1342.txt`).
- `samples/real/` – optional real Project Gutenberg files for manual checks (not generated).

## Verification (no Node on this machine; use Python + headless Chrome)
```
python tests/make_samples.py
python -m http.server 8765 --bind 127.0.0.1        # from repo root, keep running
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
"$CHROME" --headless=new --disable-gpu --user-data-dir="$TEMP/reflower-chrome" --virtual-time-budget=10000 \
  --dump-dom "http://127.0.0.1:8765/tests/test.html" | grep -E "FAIL|PASSED|ERROR"
```
- `test.html?v=<sample>` prints reflowed text, `?trace=<sample>` prints per-line join decisions,
  `?file=real/pg1342.txt[&v=trace]` analyses an arbitrary file under `samples/`.
- Screenshots: `--window-size=1400,900 --screenshot=out.png "http://127.0.0.1:8765/tests/ui.html?sample=gutenberg_72.txt&layout=spread&page=1&debug=1"`.
