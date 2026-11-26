#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md_formatter.py -- Clean up AI-chat / AI-search exported Markdown files.

Pipeline (applied per line unless inside ``` code fences / ASCII diagrams):
  1. Drop scraped-SERP artifacts   "Show more", "Name·https://site", empty bullets
                                   ("* " alone), "CareersWe are...", truncated
                                   fragments ("... , S" / "... .")
  2. Drop chatbot chatter blocks   "Would you like to...:" + its option bullets
                                   + "Let me know..." closer
  3. Remove citation links         "[1] (/goto?url=...)", "[2](https://...)",
                                   bare bracket markers "[1, 2]", "[3, 5, 6]"
  4. Dereference markdown links    "[WeChat](https://...)" -> "WeChat"
  5. Remove bare parenthesized URLs "(https://...)"
  6. Convert tab-separated blocks  -> proper Markdown pipe tables
  7. Protect ASCII diagrams        box-drawing blocks (──> │ └──>) wrapped in
                                   ``` fences so spacing/alignment survives
  8. Normalize ordered lists       consecutive indented "1. item" lines become
                                   real list items (no accidental headings)
  9. Promote headings              first title-like line -> "# ", standalone
                                   short lines -> "## " ("### 1. Numbered ...")
 10. Bold list lead-ins            "- **Label.** rest" / "- **Label:** rest",
                                   also numbered "1. **Label:** rest"
 11. Whitespace tidy               blank line around lists/headings/tables, no
                                   space before punctuation, "U.S."/"e.g." intact

Usage
-----
  python md_formatter.py FILE.md                      # in place, keeps .bak
  python md_formatter.py FILE.md -o OUT.md            # write OUT, input intact
  python md_formatter.py FILE.md --title "My Title"   # prepend "# My Title"
  python md_formatter.py *.md                         # batch

Options
-------
  --dry-run            print result to stdout, write nothing
  --title TEXT         prepend "# TEXT" when file has no leading H1
  --keep-urls          keep "(https://...)" URLs and "[text](url)" links
  --keep-chatter       keep "Would you like to..." option blocks
  --no-headings        do not promote heading-like lines
  --no-bold            do not bold list lead-ins
  --no-junk            keep UI / truncated artifact lines
  --no-diagram         do not protect/box ASCII diagrams
  --junk-regex RX      extra junk-line regex (repeatable)
  --no-backup          do not write .bak

Exit codes: 0 ok, 1 usage/IO error.
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------- regexes ----
# "[1] (/goto?url=....)" / "[2](https://...)"
CITATION_RE = re.compile(r"\s*\[\d+\]\s*\([^()]*\)")
# bare bracket citation markers: "[1, 2]" / "[3, 5, 6]" / "[5]" (digits+commas only,
# so prose brackets like "[User Traffic Spike]" are never touched)
BRACKET_CITATION_RE = re.compile(r"\s*\[\s*\d+(?:\s*,\s*\d+)*\s*\]")
# real markdown links "[Label](https://...)" -> keep Label
MD_LINK_RE = re.compile(r"\[([^\[\]]*)\]\(\s*<?https?://[^()\s]+>?\s*\)")
# parenthesized bare URL "(https://....)"
BARE_PAREN_URL_RE = re.compile(r"\s*\(\s*https?://[^()]*\)")
EMPTY_PAREN_RE = re.compile(r"\(\s*\)")
# citation runs leave ", , " / ", ." / trailing "," behind once the links are gone
MULTI_COMMA_RE = re.compile(r"[ \t]*,[ \t]*(?:,[ \t]*)+")
ORPHAN_TAIL_RE = re.compile(r"[ \t]*,[ \t]*(?=[.,;:!?]|\s*$)")
SPACE_BEFORE_PUNCT_RE = re.compile(r"[ \t]+([.,;:!?)\]])")
# collapse *repeated identical* punctuation only (".." -> ".", ",," -> ",").
# Must NOT touch "U.S., Europe" (period followed by a comma).
RUN_PUNCT_RE = re.compile(r"([.,;:!])\1+")
# "bans.And" -> "bans. And" ; only lowercase->uppercase, so "U.S." / "e.g." survive
GLUE_PUNCT_RE = re.compile(r"(?<=[a-z])([.,])(?=[A-Z])")
MULTI_SPACE_RE = re.compile(r"[ \t]{2,}")
URL_IN_LINE_RE = re.compile(r"https?://")
NUM_HEAD_RE = re.compile(r"^\d+\.\s+\S")
# bullets "- x" / "* x" AND ordered items "1. x" (bold lead-in support)
BULLET_RE = re.compile(r"^([*+-]\s+|\d+\.\s+)(.*)$", re.S)
# unicode bullet chars that should behave like "* " bullets ("• The Chokepoint. ...")
BULLET_CHAR_RE = re.compile(r"^\s*[•●▪◦‣]\s+")
# bullet/list line: "- x" / "* x" / "• x" / "1. x" — used by the chatter swallow rule
LIST_LINE_RE = re.compile(r"^[*+•●▪◦‣-]\s+|\d+\.\s+")
TABLE_LINE_RE = re.compile(r"^\|")
# ordered list item, possibly indented
ORDERED_LINE_RE = re.compile(r"^\s*\d+\.\s+\S")
# empty bullet artifact: a line holding only "* " / "-" / "+"
EMPTY_BULLET_RE = re.compile(r"^\s*[*+-]\s*$")
# empty bullet artifact: a line holding only "* " / "-" / "+" / "•" etc.
EMPTY_BULLET_RE = re.compile(r"^\s*[*+•●▪◦‣-]\s*$")
# ASCII-art / box-drawing characters (U+2500-U+25FF) and Unicode arrows
DIAGRAM_RE = re.compile(r"[\u2500-\u25FF\u2190-\u21FF]")

# Hard junk: drop the whole line.
HARD_JUNK_PATTERNS = [
    r"^\s*Show (?:more|less)\s*$",        # SERP UI text
    r"^Careers(?=[A-Z])",                 # "CareersWe are hiring..." scraped panel
    r"·\s*https?://\S+\s*$",              # site chip: "Tenstorrent·https://tenstorrent.com"
    r"\$\s?\d[\d.,]*\s*(?:\.\.\.|…)",     # mashed snippet: "Announces a $1.5 ...Tenstorrent"
    r"(?:\.\.\.|…)\s*$",                  # dangling ellipsis tail: "With an open-source ..."
    r"^\s*[*+•●▪◦‣-]\s*$",                # empty bullet artifact: "* " alone
]
# Soft junk: the line is a truncated fragment - trim back to its last full sentence.
TRUNCATED_TAIL_RE = re.compile(r"(?:,\s*[A-Z]|[ \t\u00a0\u200b][.,;:])\s*$")

CHATTY_RE = re.compile(
    r"(let me know|i can help|i can give|would you like|you'?d like|are you looking|"
    r"are you evaluating|are you planning|are you wondering|are you interested|"
    r"are you curious|do you want|want me to|should i|tell me (?:what|which)|"
    r"if you are evaluating|happy to help|dive deeper)",
    re.I,
)
CHATTY_HEAD_RE = re.compile(
    r"^(let me know|i can help|i can give|would you like|are you looking|"
    r"are you evaluating|are you planning|are you wondering|are you interested|"
    r"are you curious|do you want|if you are evaluating|happy to help)",
    re.I,
)
YES_OPENER_RE = re.compile(r"^(?:Yes|No)\s*[—,:-]\s*")

HEADING_MAX_LEN = 80
TITLE_MAX_WORDS = 12
LEAD_MAX_LEN = 72
ABBREV_RE = re.compile(
    r"(?:^|\s)(?:[A-Za-z]\.|U\.S|U\.K|i\.e|e\.g|vs|Inc|Ltd|Co|Corp|Jr|Sr|"
    r"Mr|Mrs|Ms|Dr|St|No|approx|etc)$",
    re.IGNORECASE,
)
# finite verbs that mark a bullet lead as a full sentence, not a label
VERB_WORDS = {
    "is", "are", "was", "were", "be", "been", "being", "has", "have", "had",
    "acts", "act", "will", "can", "could", "may", "might", "must", "shall",
    "should", "would", "does", "do", "did", "means", "refers", "describes",
    "represents", "takes", "gives", "gets", "sells", "provides", "includes",
    "offers", "uses", "requires", "contains", "consists", "works", "operates",
    "happens", "occurs", "exists", "remains", "stays", "becomes", "became",
    "looks", "seems",
}


# ------------------------------------------------------------- line clean ----
def _last_sentence_end(text: str) -> int:
    """Index just past the last real sentence end, ignoring "U.S."/"Inc." style dots."""
    best = -1
    for m in re.finditer(r"[.!?](?=\s|$)", text):
        word = text[:m.start()].rsplit(None, 1)[-1]
        if len(word) <= 1 or word.lower() in {
            "u.s", "u.k", "e.g", "i.e", "vs", "inc", "ltd", "co", "corp",
            "etc", "no", "st", "dr", "mr", "mrs", "ms", "jr", "sr", "approx",
        }:
            continue
        best = m.start() + 1
    return best


def trim_truncated(line: str) -> str:
    """'...offices in Toronto, Belgrade, S' -> keep up to the last full sentence."""
    m = TRUNCATED_TAIL_RE.search(line)
    if not m:
        return line
    cut = line[:m.start()]
    last = _last_sentence_end(cut)
    return cut[:last] if last != -1 else ""


def clean_line(line: str, keep_urls: bool) -> str:
    s = line.replace("\u00a0", " ").replace("\u200b", "")
    s = CITATION_RE.sub("", s)
    s = BRACKET_CITATION_RE.sub("", s)
    if not keep_urls:
        s = MD_LINK_RE.sub(lambda m: m.group(1).strip(), s)
        s = BARE_PAREN_URL_RE.sub("", s)
    s = EMPTY_PAREN_RE.sub("", s)
    s = MULTI_COMMA_RE.sub(", ", s)
    s = ORPHAN_TAIL_RE.sub("", s)
    s = SPACE_BEFORE_PUNCT_RE.sub(r"\1", s)
    s = RUN_PUNCT_RE.sub(r"\1 ", s)
    s = GLUE_PUNCT_RE.sub(r"\1 ", s)
    s = MULTI_SPACE_RE.sub(" ", s)
    s = YES_OPENER_RE.sub("", s.strip())
    # "• Point. rest" -> "* Point. rest" (ASCII bullet for downstream bold/list logic)
    if s.startswith(("•", "●", "▪", "◦", "‣")):
        s = "* " + s[1:].lstrip()
    if s and s[0].islower():
        s = s[0].upper() + s[1:]
    return s.rstrip()


# ---------------------------------------------------------------- tables ----
def convert_tables(lines):
    """Turn runs of tab-separated lines (>=2) into Markdown pipe tables."""
    out, i, n, converted = [], 0, len(lines), 0
    while i < n:
        if "\t" in lines[i]:
            j = i
            while j < n and "\t" in lines[j]:
                j += 1
            block = lines[i:j]
            if len(block) >= 2:
                rows = [[c.strip().replace("|", r"\|") for c in ln.split("\t")] for ln in block]
                ncol = max(len(r) for r in rows)
                rows = [r + [""] * (ncol - len(r)) for r in rows]
                if out and out[-1].strip():
                    out.append("")
                out.append("| " + " | ".join(rows[0]) + " |")
                out.append("| " + " | ".join(["---"] * ncol) + " |")
                for r in rows[1:]:
                    out.append("| " + " | ".join(r) + " |")
                out.append("")
                converted += 1
                i = j
                continue
        out.append(lines[i])
        i += 1
    return out, converted


# --------------------------------------------------------------- fences ------
def _fence_spans(lines):
    """Per-line mask: True for fence markers and everything inside fences."""
    mask, inside = [False] * len(lines), False
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("```"):
            mask[i] = True
            inside = not inside
        else:
            mask[i] = inside
    return mask


def protect_diagrams(lines):
    """Wrap runs of ASCII-art lines (box drawing + adjacent indented lines) in fences."""
    fence = _fence_spans(lines)
    marked = [not fence[i] and bool(DIAGRAM_RE.search(ln)) for i, ln in enumerate(lines)]
    changed = True
    while changed:
        changed = False
        for i, ln in enumerate(lines):
            if marked[i] or fence[i]:
                continue
            if re.match(r"^\s{2,}\S", ln) and (
                (i > 0 and marked[i - 1]) or (i + 1 < len(lines) and marked[i + 1])
            ):
                marked[i] = True
                changed = True
    if not any(marked):
        return lines, 0
    out, i, n, fenced = [], 0, len(lines), 0
    while i < n:
        if marked[i]:
            j = i
            while j < n and marked[j]:
                j += 1
            if out and out[-1].strip():
                out.append("")
            out.append("```")
            out.extend(ln.rstrip() for ln in lines[i:j])
            out.append("```")
            fenced += j - i
            if j < n and lines[j].strip():
                out.append("")
            i = j
        else:
            out.append(lines[i])
            i += 1
    return out, fenced


def normalize_ordered_runs(lines):
    """Consecutive numbered lines (only blanks between) are list items, not headings.

    '   1. The Post: ...' / '   2. The Settings: ...'  ->  '1. ...' / '2. ...'
    Returns (lines, set_of_indexes_normalized).
    """
    fence = _fence_spans(lines)
    idx = [i for i, ln in enumerate(lines) if not fence[i] and ORDERED_LINE_RE.match(ln)]
    in_run = set()
    k = 0
    while k < len(idx):
        j = k
        while j + 1 < len(idx) and all(
            not lines[t].strip() for t in range(idx[j] + 1, idx[j + 1])
        ):
            j += 1
        if j > k:
            in_run.update(idx[k:j + 1])
        k = j + 1
    if not in_run:
        return lines, in_run
    out = []
    for i, ln in enumerate(lines):
        if i in in_run:
            m = re.match(r"^\s*(\d+\.\s+)(.*)$", ln)
            out.append(m.group(1) + m.group(2))
        else:
            out.append(ln)
    return out, in_run


# --------------------------------------------------------------- heading ----
def heading_for(line: str):
    """Return ('##'|'###', text) when the line looks like a section heading."""
    if not line or line != line.strip():
        return None
    s = line.strip()
    if s.startswith(("#", "|", "*", "-", "+", ">", "!", "```", "---", "[")):
        return None
    if len(s) > HEADING_MAX_LEN or URL_IN_LINE_RE.search(s):
        return None
    if s.endswith((".", "?", "!", ":", ";", ",")):
        return None
    if not re.search(r"[A-Za-z]", s) or s[0].islower():
        return None
    if NUM_HEAD_RE.match(s):
        return ("###", s)
    return ("##", s)


def title_for(line: str):
    """Return ('#', text) for a short title-like first line of the document."""
    if not line or line != line.strip():
        return None
    s = line.strip()
    if s.startswith(("#", "|", "*", "-", "+", ">", "!", "```", "---", "[")):
        return None
    if ORDERED_LINE_RE.match(s):
        return None
    if len(s) > HEADING_MAX_LEN or URL_IN_LINE_RE.search(s):
        return None
    if s.endswith((".", "?", "!", ":", ";", ",")):
        return None
    if len(s.split()) > TITLE_MAX_WORDS or not re.search(r"[A-Za-z]", s):
        return None
    return ("#", s[0].upper() + s[1:])


# ----------------------------------------------------------- bold leads -----
def bold_bullet_lead(line: str) -> str:
    """'- Label. rest' / '1. Label: rest' -> '- **Label.** rest' / '1. **Label:** rest'"""
    m = BULLET_RE.match(line)
    if not m:
        return line
    prefix, body = m.group(1), m.group(2)
    if body.startswith(("**", "[", "(`")):
        return line

    skip_until = 0
    for mm in re.finditer(r"[.:]\s", body):
        if mm.start() < skip_until:
            continue
        end = mm.start() + 1
        lead, rest = body[:end], body[mm.end():]
        if not rest or not rest[0].isupper():
            continue
        # "U.S." / "Non-U." -> 'S.' is an acronym continuation, not a label end
        if rest[0].isupper() and len(rest) > 1 and rest[1] == "." and lead[-2].isupper():
            skip_until = mm.end() + 1
            continue
        lead = lead.strip()
        if len(lead) > LEAD_MAX_LEN or lead[0].islower():
            continue
        if lead.count("(") != lead.count(")") or lead.count("[") != lead.count("]"):
            continue
        words = lead[:-1].strip().split()
        if not words or "." in words[-1] or ABBREV_RE.search(" " + words[-1]):
            continue
        # period-ended lead holding a finite verb is a sentence, not a label
        # (colon-ended leads like "Use Wi-Fi:" are imperative labels, keep them)
        if lead.endswith(".") and any(w.lower() in VERB_WORDS for w in words):
            continue
        return prefix + "**" + lead + "** " + rest.lstrip()
    return line


# --------------------------------------------------------------- chatter ----
def is_chatty(line: str) -> bool:
    s = line.strip()
    if not s or s.startswith(("|", "#")):
        return False
    if not CHATTY_RE.search(s):
        return False
    if len(s) > 320:
        return False
    return bool(s.endswith((":", "?", "!")) or CHATTY_HEAD_RE.match(s))


# ----------------------------------------------------------------- main ------
def process(text: str, opts) -> tuple:
    stats = Counter()
    stats.update({"citations": 0, "brcitations": 0, "urls": 0, "links": 0,
                  "junk": 0, "chatty": 0, "emptied": 0, "tables": 0,
                  "headings": 0, "titles": 0, "olitems": 0, "fenced": 0,
                  "bolds": 0, "paras": 0})

    hard_res = [] if opts.no_junk else [re.compile(p) for p in HARD_JUNK_PATTERNS]
    hard_res += [re.compile(p) for p in opts.junk_regex]

    lines, in_fence, in_diagram, skip_bullets = [], False, False, False
    for raw in text.splitlines():
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            in_diagram = False
            lines.append(raw.rstrip())
            continue
        if in_fence:
            lines.append(raw.rstrip())
            continue

        # ASCII diagram block: pass through verbatim until a blank line
        if not opts.no_diagram:
            if in_diagram:
                if raw.strip():
                    lines.append(raw.rstrip())
                    continue
                in_diagram = False
                lines.append("")
                continue
            if DIAGRAM_RE.search(raw):
                in_diagram = True
                lines.append(raw.rstrip())
                continue

        if any(rx.search(raw) for rx in hard_res):
            stats["junk"] += 1
            skip_bullets = False
            continue

        if not opts.no_junk:
            trimmed = trim_truncated(raw)
            if trimmed != raw:
                stats["junk"] += 1
                if not trimmed.strip():
                    skip_bullets = False
                    continue
                raw = trimmed

        if not opts.keep_chatter:
            if skip_bullets and LIST_LINE_RE.match(raw.strip()):
                stats["chatty"] += 1
                continue
            if is_chatty(raw):
                stats["chatty"] += 1
                skip_bullets = True
                continue
        skip_bullets = False

        stats["citations"] += len(CITATION_RE.findall(raw))
        stats["brcitations"] += len(BRACKET_CITATION_RE.findall(raw))
        if not opts.keep_urls:
            stats["urls"] += len(BARE_PAREN_URL_RE.findall(raw))
            stats["links"] += len(MD_LINK_RE.findall(raw))

        cleaned = clean_line(raw, opts.keep_urls)
        if not cleaned.strip():
            if raw.strip():
                stats["emptied"] += 1
            lines.append("")
        else:
            lines.append(cleaned)

    lines, stats["tables"] = convert_tables(lines)
    if not opts.no_diagram:
        lines, stats["fenced"] = protect_diagrams(lines)
    lines, ol_idx = normalize_ordered_runs(lines)
    stats["olitems"] = len(ol_idx)
    fence_mask = _fence_spans(lines)

    final = []
    prev_kind = "blank"
    first_done = False
    has_h1 = any(ln.startswith("# ") for ln in lines)

    for i, ln in enumerate(lines):
        if not ln.strip():
            if final and final[-1].strip():
                final.append("")
                prev_kind = "blank"
            continue

        head = None
        if not opts.no_headings and not fence_mask[i] and i not in ol_idx:
            if not first_done and not opts.title and not has_h1:
                head = title_for(ln)
            if head is None:
                head = heading_for(ln)
        if head:
            level, text_ = head
            if final and final[-1].strip():
                final.append("")
            final.append(f"{level} {text_}")
            final.append("")
            if level == "#":
                stats["titles"] += 1
            else:
                stats["headings"] += 1
            prev_kind = "heading"
            first_done = True
            continue

        new = bold_bullet_lead(ln) if not opts.no_bold else ln
        if new != ln:
            stats["bolds"] += 1

        # never insert blanks touching fence content (diagrams need contiguous lines)
        fence_hit = fence_mask[i] or (i > 0 and fence_mask[i - 1])

        if LIST_LINE_RE.match(new):
            if prev_kind in ("text", "table") and not fence_hit:
                final.append("")
            kind = "list"
        else:
            kind = "table" if TABLE_LINE_RE.match(new) else "text"
            if not fence_hit:
                if prev_kind == "list":
                    final.append("")
                elif prev_kind == "text" and kind == "text":
                    final.append("")          # split adjacent text lines into
                    stats["paras"] += 1       # separate paragraphs (blank line)

        final.append(new)
        prev_kind = kind
        first_done = True

    while final and not final[-1].strip():
        final.pop()

    body = "\n".join(final)
    if opts.title and not body.lstrip().startswith("# "):
        body = f"# {opts.title}\n\n" + body

    return body.rstrip() + "\n", stats


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Format AI-chat-exported Markdown (strip citations/links, fix tables/headings).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("files", nargs="+", help="Markdown file(s) to process")
    ap.add_argument("-o", "--output", help="write result to OUT (single input only)")
    ap.add_argument("--title", help="prepend '# TITLE' if the file has no leading H1")
    ap.add_argument("--dry-run", action="store_true", help="print result, write nothing")
    ap.add_argument("--keep-urls", action="store_true",
                    help="keep bare URLs and [text](url) markdown links")
    ap.add_argument("--keep-chatter", action="store_true", help="keep chat option blocks")
    ap.add_argument("--no-headings", action="store_true", help="do not promote headings")
    ap.add_argument("--no-bold", action="store_true", help="do not bold list lead-ins")
    ap.add_argument("--no-junk", action="store_true", help="keep UI artifact lines")
    ap.add_argument("--no-diagram", action="store_true", help="do not protect ASCII diagrams")
    ap.add_argument("--junk-regex", action="append", default=[], metavar="RX",
                    help="extra junk-line regex (repeatable)")
    ap.add_argument("--no-backup", action="store_true", help="do not create .bak")
    opts = ap.parse_args(argv)

    if opts.output and len(opts.files) > 1:
        ap.error("-o/--output works with a single input file")

    failed = False
    for name in opts.files:
        src = Path(name)
        if not src.is_file():
            print(f"[ERROR] not a file: {src}", file=sys.stderr)
            failed = True
            continue
        try:
            text = src.read_text(encoding="utf-8-sig", errors="replace")
        except OSError as exc:
            print(f"[ERROR] read failed: {src}: {exc}", file=sys.stderr)
            failed = True
            continue

        result, st = process(text, opts)
        summary = (f"citations={st['citations']}+{st['brcitations']}br urls={st['urls']} "
                   f"links={st['links']} junk={st['junk']} chatty={st['chatty']} "
                   f"emptied={st['emptied']} tables={st['tables']} "
                   f"headings={st['headings']}+{st['titles']}t olitems={st['olitems']} "
                   f"fenced={st['fenced']} bolds={st['bolds']} paras={st['paras']}")

        if opts.dry_run:
            print(result, end="")
            print(f"# dry-run {src.name}: {summary}", file=sys.stderr)
            continue

        dst = Path(opts.output) if opts.output else src
        if dst == src and not opts.no_backup:
            src.with_name(src.name + ".bak").write_text(text, encoding="utf-8")
        dst.write_text(result, encoding="utf-8", newline="\n")

        extra = "" if (opts.output or opts.no_backup) else f"  (backup: {dst.name}.bak)"
        print(f"{src.name}: {summary} -> {dst}{extra}")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
