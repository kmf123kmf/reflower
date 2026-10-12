"""Generate synthetic hard-wrapped story files that exercise the reflow heuristics.

Run:  python tests/make_samples.py
Writes .txt files into ../samples and an expectations file used by tests/test.html.
"""
import json
import os
import random
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "samples")

P = [
    "The rain had been falling since before dawn, a thin grey curtain that hung over the harbour "
    "and blurred the masts of the fishing boats into a single smudge of charcoal. Margaret stood at "
    "the window of the old customs house with her hands pressed flat against the cold glass, watching "
    "for a sail that she already knew would not come.",
    "She had been told, of course. Everyone in the village had made a point of telling her, in the "
    "careful, well-meaning voices people reserve for the bereaved and the slightly mad. The Albatross "
    "was three weeks overdue; the storm off the Hebrides had been the worst in forty years; there was "
    "no sense in hoping.",
    "\"You'll catch your death standing there,\" said Mrs. Pennywhistle from the doorway.",
    "\"Then I shall have caught something, at least.\"",
    "The older woman clicked her tongue and came to stand beside her. For a long moment neither of "
    "them spoke. Somewhere below, a door banged in the wind, and a dog began to bark with the "
    "monotonous persistence of an animal that has forgotten why it started.",
    "\"He wrote to me,\" Margaret said at last. \"Before they sailed. Did I ever tell you that? A "
    "ridiculous letter, all about the weather and the cook's terrible porridge and a gull that had "
    "taken a liking to his hat.\"",
    "\"Sounds like him.\"",
    "\"It does.\" She smiled, though it did not reach her eyes. \"It sounds exactly like him.\"",
    "By noon the rain had thinned to a drizzle and the light had taken on that peculiar pewter quality "
    "that belongs only to coastal towns in late October. Margaret walked the length of the quay twice, "
    "past the lobster pots stacked like the vertebrae of some enormous beast, past the chandler's shop "
    "with its faded sign, past the bench where old Tom Hallett sat every afternoon regardless of the "
    "weather, mending nets that no one would ever use again.",
    "\"Afternoon, Miss Carrow.\"",
    "\"Afternoon, Tom.\"",
    "\"Bit of a blow last night.\"",
    "\"Yes.\"",
    "He looked up at her then, his eyes pale and watery beneath the brim of his cap. \"They'll be "
    "sheltering, like as not. Up past Stornoway--there's coves up there a man could hide a fleet in. "
    "My own father was lost nine days once, and came home with a beard down to here and a barrel of "
    "salt herring he'd traded off a Norwegian.\"",
    "It was a kindness, and she recognised it as one. She thanked him and walked on, and did not let "
    "herself cry until she had turned the corner by the church and there was no one to see.",
    "That night she dreamed of the sea. Not the grey, rain-pocked sea of the harbour, but a vast and "
    "luminous expanse under a sky crowded with stars, and on it a single ship with every sail set, "
    "moving silently northward toward a horizon that kept retreating, and retreating, and never came "
    "any nearer at all.",
    "In the morning there was a knock at the door.",
]

POEM = [
    "O wind that walks upon the water,",
    "    Bring him home, bring him home;",
    "O tide that turns at every quarter,",
    "    Bring him home across the foam.",
]

LETTER = [
    "My dearest Meg,",
    "",
    "The cook has outdone himself again. I am fairly certain the porridge this morning contained a "
    "button, though he swears it was a raisin. The gull is still with us. I have named him Admiral.",
    "",
    "Yours ever,",
    "Will",
]


def wrap(text, width, indent="", first=None):
    first = indent if first is None else first
    return textwrap.wrap(text, width, initial_indent=first, subsequent_indent=indent,
                         break_on_hyphens=True, break_long_words=False)


def center(text, width):
    pad = max(0, (width - len(text)) // 2)
    return " " * pad + text


def justify(line, width):
    words = line.split(" ")
    if len(words) < 2:
        return line
    gaps = len(words) - 1
    extra = width - len(line)
    out = []
    for i, w in enumerate(words[:-1]):
        out.append(w + " " * (1 + extra // gaps + (1 if i < extra % gaps else 0)))
    out.append(words[-1])
    return "".join(out)


def blank_separated(width, paras, out, justify_text=False):
    for p in paras:
        lines = wrap(p, width)
        if justify_text:
            lines = [justify(l, width) for l in lines[:-1]] + lines[-1:]
        out.extend(lines)
        out.append("")


samples = {}
expect = {}

# 1. Gutenberg-like: blank separated, width 72, roman numeral chapters, centered breaks, poem, letter
W = 72
o = ["THE LAST VOYAGE OF THE ALBATROSS", "", "by Eleanor Finch", "", "", "",
     "CHAPTER I.", "", "THE WATCHER AT THE WINDOW", "", ""]
blank_separated(W, P[:8], o)
o += [center("*       *       *", W), ""]
blank_separated(W, P[8:10], o)
o += POEM + [""]
blank_separated(W, P[10:12], o)
o += ["", "", "CHAPTER II.", "", "THE LETTER", "", ""]
for l in LETTER:
    o.extend(wrap(l, W, indent="    ") if l else [""])
o.append("")
blank_separated(W, P[12:], o)
samples["gutenberg_72.txt"] = o
expect["gutenberg_72.txt"] = {"width": 72, "wrapped": True, "headings": 2, "breaks": 1, "title": True,
                                  "verse": 2, "minParas": len(P) - 2}

# 2. Indent style, no blank lines, width 65, "Chapter One" headings, '#' breaks
W = 65
o = ["", center("The Last Voyage", W), center("Eleanor Finch", W), "", "",
     "Chapter One", ""]
for i, p in enumerate(P[:9]):
    o.extend(wrap(p, W, first="    "))
o += ["", center("#", W), ""]
for p in P[9:12]:
    o.extend(wrap(p, W, first="    "))
o += ["", "", "Chapter Two", ""]
for p in P[12:]:
    o.extend(wrap(p, W, first="    "))
samples["indent_style_65.txt"] = o
expect["indent_style_65.txt"] = {"width": 65, "wrapped": True, "headings": 2, "breaks": 1, "paras": len(P)}

# 3. Double spaced: blank line after every line, paragraphs separated by 2+ blanks
W = 80
o = ["Chapter 1", "", "", ""]
for p in P[:10]:
    for l in wrap(p, W):
        o += [l, ""]
    o += [""]
samples["double_spaced_80.txt"] = o
expect["double_spaced_80.txt"] = {"width": 80, "wrapped": True, "doubleSpaced": True, "headings": 1, "paras": 10}

# 4. Unwrapped: one paragraph per line
o = ["The Last Voyage", "", "Chapter 1", ""]
for p in P:
    o += [p, ""]
samples["unwrapped.txt"] = o
expect["unwrapped.txt"] = {"wrapped": False, "headings": 1, "paras": len(P)}

# 5. Fanfic style: metadata header, author's note, "Chapter 3: Title", ~~~ breaks, emphasis
W = 76
o = ["Title: The Last Voyage", "Author: efinch", "Rating: T", "Summary: A woman waits for a ship.",
     "", "A/N: Thanks for all the reviews! This one is a bit _sad_, sorry.", "", "",
     "Chapter 3: The Return", "", ""]
emph = [p.replace("forty years", "*forty* years").replace("well-meaning", "well-meaning")
        for p in P]
blank_separated(W, emph[:7], o)
o += ["~~~", ""]
blank_separated(W, emph[7:], o)
o += ["", "THE END"]
samples["fanfic_76.txt"] = o
expect["fanfic_76.txt"] = {"width": 76, "wrapped": True, "headings": 2, "breaks": 1, "meta": True}

# 6. Justified text, centered headings, width 68
W = 68
o = [center("PART ONE", W), "", center("The Harbour", W), "", ""]
blank_separated(W, P[:9], o, justify_text=True)
o += [center("* * *", W), ""]
blank_separated(W, P[9:], o, justify_text=True)
samples["justified_68.txt"] = o
expect["justified_68.txt"] = {"width": 68, "wrapped": True, "headings": 1, "breaks": 1, "paras": len(P)}

# 7. Mixed widths: section one at 60, section two at 78
o = ["Chapter 1", ""]
blank_separated(60, P[:8], o)
o += ["", "Chapter 2", ""]
blank_separated(78, P[8:], o)
samples["mixed_width.txt"] = o
expect["mixed_width.txt"] = {"wrapped": True, "headings": 2, "paras": len(P)}

# 8. format=flowed style: trailing space marks soft breaks, no blank lines, no indent
W = 72
o = ["Chapter 1", ""]
for p in P:
    lines = wrap(p, W)
    o += [l + " " for l in lines[:-1]] + lines[-1:]
samples["flowed_72.txt"] = o
expect["flowed_72.txt"] = {"width": 72, "wrapped": True, "flowed": True, "headings": 1, "paras": len(P)}

# 9. No blank lines, no indent: paragraphs only detectable by line length
W = 70
o = ["Chapter 1", ""]
for p in P:
    o += wrap(p, W)
samples["noblank_70.txt"] = o
expect["noblank_70.txt"] = {"width": 70, "wrapped": True, "headings": 1, "approxParas": len(P)}

# 10. Ragged, manually typed margins (each line breaks somewhere between 55 and 72)
rng = random.Random(7)


def ragged(text):
    words, lines, cur = text.split(), [], ""
    target = rng.randint(55, 72)
    for w in words:
        if cur and len(cur) + 1 + len(w) > target:
            lines.append(cur)
            cur, target = w, rng.randint(55, 72)
        else:
            cur = f"{cur} {w}" if cur else w
    return lines + [cur]


o = ["Chapter 1", ""]
for p in P:
    o += ragged(p) + [""]
samples["ragged.txt"] = o
expect["ragged.txt"] = {"wrapped": True, "headings": 1, "paras": len(P)}

# 11. Front matter with epigraph + contents, roman numeral headings, list, dehyphenation
W = 72
o = ["THE LAST VOYAGE", "", "", center("The sea has neither meaning nor pity.", W),
     center("-- Anton Chekhov", W), "", "", "CONTENTS", "", "I. The Watcher", "II. The Letter", "", "", "",
     "I.", ""]
hyph = [p.replace("customs house", "customs-house") for p in P]
blank_separated(W, hyph[:6], o)
o += ["She made a list:", "", "  - bread and tea", "  - a new lamp wick", "  - paper for letters", ""]
o += ["", "II.", ""]
blank_separated(W, hyph[6:], o)
# a manually hyphenated word whose joined form appears elsewhere in the text
o += ["It was the kind of quiet the old fishermen said came just before every-",
      "thing changes, and everything did. Even the well-",
      "known gulls had gone.", ""]
samples["frontmatter_72.txt"] = o
expect["frontmatter_72.txt"] = {"width": 72, "wrapped": True, "title": True, "headings": 3, "minParas": len(P) - 2}

# 12. Unwrapped, no blank lines: one paragraph per physical line
o = ["Chapter 1"] + P
samples["unwrapped_noblank.txt"] = o
expect["unwrapped_noblank.txt"] = {"wrapped": False, "headings": 1, "paras": len(P)}

# 13. Word-style RTF: styles, info, header, centred title, heading styles, real paragraphs,
#     italics, escaped/unicode characters, a poem with \line, a centred break, page break, field
def rtf_para(text):
    return text.replace("forty years", r"{\i forty} years").replace("cafe", r"caf\'e9")


word = [
    r"{\rtf1\ansi\ansicpg1252\deff0{\fonttbl{\f0\froman Times New Roman;}{\f1\fswiss Arial;}}",
    r"{\colortbl;\red0\green0\blue0;}",
    r"{\stylesheet{\s0 Normal;}{\s1\b\fs32 heading 1;}{\s15\qc\fs48 Title;}}",
    r"{\info{\title The Last Voyage of the Albatross}{\author Eleanor Finch}}",
    r"{\header\pard\qr\f1 Running header that must not appear\par}",
    r"{\footer\pard\qc Page \chpgn\par}",
    r"\pard\s15\qc\b\fs48 The Last Voyage\b0\fs24\par",
    r"\pard\qc{\i by Eleanor Finch}\par",
    r"\pard\par",
    r"\pard\s1\b Chapter 1\b0\par",
    r"\pard\qc\b The Watcher\b0\par",
    r"\pard\par",
]
for p in P[:6]:
    word.append(r"\pard\fi360 " + rtf_para(p) + r"\par")
word.append(r"\pard\fi360 She remembered the caf\'e9 by the harbour\u8212?the one with the "
            r"\ldblquote blue door\rdblquote  {\*\bkmkstart b1}{\*\bkmkend b1}and the "
            r"{\field{\*\fldinst HYPERLINK \"http://example.com\"}{\fldrslt dreadful coffee}}."
            r"{\footnote\pard Footnote text that must not appear.\par}\par")
word.append(r"\pard\li720 O wind that walks upon the water,\line Bring him home, bring him home;\line "
            r"O tide that turns at every quarter,\line Bring him home across the foam.\par")
word.append(r"\pard\qc *\tab *\tab *\par")
for p in P[6:10]:
    word.append(r"\pard\fi360 " + rtf_para(p) + r"\par")
word.append(r"\page")
word.append(r"\pard\outlinelevel0\b Chapter 2\b0\par")
for p in P[10:]:
    word.append(r"\pard\fi360 " + rtf_para(p) + r"\par")
word.append("}")
samples["story_word.rtf"] = word
expect["story_word.rtf"] = {"title": True, "headings": 2, "breaks": 1, "verse": 1, "paras": len(P) + 1,
                            "contains": ["café", "—the one", "<em>forty</em>", "dreadful coffee", "The Watcher"],
                            "notContains": ["Running header", "Footnote text", "HYPERLINK", "Times New Roman"]}

# 14. Hard-wrapped plain text saved as RTF (WordPad style): every physical line is a \par
wp = [r"{\rtf1\ansi\deff0{\fonttbl{\f0\fnil\fcharset0 Courier New;}}",
      r"\viewkind4\uc1\pard\f0\fs20 CHAPTER ONE\par", r"\par"]
for p in P:
    wp += [line.replace("cafe", r"caf\'e9") + r"\par" for line in wrap(p, 70)] + [r"\par"]
wp.append("}")
samples["wordpad_wrapped.rtf"] = wp
expect["wordpad_wrapped.rtf"] = {"width": 70, "wrapped": True, "headings": 1, "paras": len(P),
                                 "contains": ["Pennywhistle from the doorway"]}

os.makedirs(OUT, exist_ok=True)
for name, lines in samples.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lines) + "\n")
with open(os.path.join(ROOT, "tests", "expectations.json"), "w", encoding="utf-8") as f:
    json.dump(expect, f, indent=2)
print("wrote", len(samples), "samples to", OUT)
