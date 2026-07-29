#!/usr/bin/env python3
"""Audit the Docusaurus docs against the MZpack C# source.

Reports, per docs page, which NinjaTrader UI parameters ([Display] attributes in
the product source) are missing from the documentation, which documented rows no
longer exist in the source, and which descriptions merely restate the label.

Read-only: never modifies docs. Run from the docs repo root:

    python3 scripts/param_audit.py [--report scripts/param-audit-report.md]
"""

import argparse
import os
import re
import sys
from collections import OrderedDict

SRC = "/home/mikhail/mzpack/repo/MZpack.NT8"
DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

# Retail build. FREE/TRIAL are applied by the packaging pipeline, not a csproj
# configuration, so the retail set is the !FREE set.
DEFINED = {"DATA", "APISAMPLE", "CUSTOM_INDI", "STRAT", "LIC", "NATIVE_CALC"}

# Groups excluded from user-facing docs (dev-only or FREE-edition placeholders).
SKIP_GROUPS = {"tests", "easter", "about mzpack free version", "base", "licensing"}

# Params every indicator inherits; documented once on the common-settings page.
# Listing them here keeps them from being reported as stale on each indicator page.
INDICATOR_BASE = ["Core/CoreIndicator.cs", "Core/TickIndicator.cs",
                  "Levels/LevelsIndicator.cs", "Levels/ContinuousLevel.cs"]
STRATEGY_BASE = ["Algo/MZpackStrategyBase.cs"]

# page -> source files whose params are legitimately documented there but counted
# against a different page (inherited/base parameters).
INHERITED = {
    "docs/indicators/mzFootprint.md": INDICATOR_BASE,
    "docs/indicators/mzBigTrade.md": INDICATOR_BASE,
    "docs/indicators/mzMarketDepth.md": INDICATOR_BASE,
    "docs/indicators/mzVolumeDelta.md": INDICATOR_BASE,
    # mzDeltaDivergence derives from mzVolumeDelta and inherits all of its params
    "docs/indicators/mzDeltaDivergence.md": INDICATOR_BASE + ["mzVolumeDelta/mzVolumeDelta.cs"],
    "docs/indicators/mzVolumeProfile.md": INDICATOR_BASE,
    "docs/strategies/built-in-strategies.md": STRATEGY_BASE,
}

# doc page -> source files contributing its parameters
TARGETS = OrderedDict([
    ("docs/indicators/mzFootprint.md", ["mzFootprint/mzFootprint.cs"]),
    ("docs/indicators/mzBigTrade.md", ["mzBigTrade/mzBigTrade.cs"]),
    ("docs/indicators/mzMarketDepth.md", ["mzMarketDepth/mzMarketDepth.cs"]),
    ("docs/indicators/mzVolumeDelta.md", ["mzVolumeDelta/mzVolumeDelta.cs"]),
    ("docs/indicators/mzDeltaDivergence.md", ["mzDeltaDivergence/mzDeltaDivergence.cs"]),
    ("docs/indicators/mzVolumeProfile.md", ["mzVolumeProfile/mzVolumeProfile.cs"]),
    ("docs/indicators/common-settings.md", [
        "Core/CoreIndicator.cs",
        "Core/TickIndicator.cs",
        "Levels/LevelsIndicator.cs",
        "Levels/ContinuousLevel.cs",
    ]),
    ("docs/strategies/strategy-framework.md", ["Algo/MZpackStrategyBase.cs"]),
    ("docs/strategies/built-in-strategies.md", [
        "Algo/Strategies/FootprintAction/FootprintAction.cs",
        "Algo/Strategies/GhostResistance/GhostResistance.cs",
        "Algo/Strategies/Data_Export/Data_Export.cs",
    ]),
])

# Base params declared [Browsable(false)] in CoreIndicator but re-exposed per
# indicator via a [Browsable(true)] override (which reuses the base [Display]).
# They belong to those pages, not to the shared common-settings page.
REEXPOSED = {
    "docs/indicators/mzFootprint.md": ["Optimize render performance", "Maximal render time, ms"],
    "docs/indicators/mzBigTrade.md": ["Optimize render performance", "Maximal render time, ms"],
    "docs/indicators/mzVolumeProfile.md": ["Optimize render performance", "Maximal render time, ms"],
    "docs/indicators/mzMarketDepth.md": ["Optimize render performance", "Maximal render time, ms",
                                         "Refresh delay, ms"],
}

# Display( ... ) allowing parentheses inside string arguments. The lookbehind
# matches `Display(` after `[` or after `, ` in a shared attribute bracket while
# excluding `DisplayXxx(` and `foo.Display(`.
DISPLAY_RE = re.compile(r'(?<![\w.])Display\((?:[^()"]|"(?:[^"\\]|\\.)*")*\)')
NAME_RE = re.compile(r'Name\s*=\s*"((?:[^"\\]|\\.)*)"')
GROUP_RE = re.compile(r'GroupName\s*=\s*"((?:[^"\\]|\\.)*)"')
ORDER_RE = re.compile(r'Order\s*=\s*(-?\d+)')
DESC_RE = re.compile(r'Description\s*=\s*"((?:[^"\\]|\\.)*)"')
RANGE_RE = re.compile(r'\[\s*Range\s*\(([^)]*)\)\s*\]')
PROP_RE = re.compile(
    r'public\s+(?:virtual\s+|override\s+|static\s+|readonly\s+|new\s+)*'
    r'([\w<>\[\],.?]+)\s+(\w+)\s*(?:\{|=>|$)')
DEFAULT_RE = re.compile(r'\}\s*=\s*(.+?);\s*$')
INSTANCE_RE = re.compile(r'^#\d+\s*:?\s*')


# ---------------------------------------------------------------- preprocessor

def eval_cond(expr):
    """Evaluate a C# #if expression against DEFINED."""
    expr = expr.strip()
    # Translate to Python, mapping identifiers to their defined-ness.
    py = expr.replace("&&", " and ").replace("||", " or ").replace("!", " not ")
    py = re.sub(r'\b([A-Za-z_]\w*)\b',
                lambda m: "True" if m.group(1) in DEFINED else "False", py)
    py = py.replace("not True", "not True").replace("not False", "not False")
    try:
        return bool(eval(py, {"__builtins__": {}}, {}))
    except Exception:
        return True  # unparseable: assume active rather than silently dropping


def active_lines(lines):
    """Return a list of booleans: is this line inside an active #if region?"""
    out = []
    stack = []  # list of (this_branch_active, any_branch_taken)
    for raw in lines:
        s = raw.strip()
        if s.startswith("#if "):
            cond = eval_cond(s[4:])
            parent = all(a for a, _ in stack) if stack else True
            stack.append((cond and parent, cond))
            out.append(False)
            continue
        if s.startswith("#elif "):
            if stack:
                _, taken = stack[-1]
                cond = eval_cond(s[6:])
                parent = all(a for a, _ in stack[:-1]) if len(stack) > 1 else True
                stack[-1] = ((not taken) and cond and parent, taken or cond)
            out.append(False)
            continue
        if s.startswith("#else"):
            if stack:
                _, taken = stack[-1]
                parent = all(a for a, _ in stack[:-1]) if len(stack) > 1 else True
                stack[-1] = ((not taken) and parent, True)
            out.append(False)
            continue
        if s.startswith("#endif"):
            if stack:
                stack.pop()
            out.append(False)
            continue
        out.append(all(a for a, _ in stack) if stack else True)
    return out


# ------------------------------------------------------------------ source side

def norm(name):
    """Normalise a parameter name for matching."""
    n = name.strip()
    # docs escape UI labels containing angle brackets so MDX does not parse them
    n = (n.replace("&lt;", "<").replace("&gt;", ">")
          .replace("&amp;", "&").replace("`", ""))
    n = INSTANCE_RE.sub("", n)          # drop "#1 " .. "#5 " instance prefix
    n = re.sub(r'\s+', " ", n)
    return n.lower()


def parse_source(relpath, include_hidden=False):
    path = os.path.join(SRC, relpath)
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    active = active_lines(lines)
    params = []
    for i, line in enumerate(lines):
        if not active[i]:
            continue
        if line.lstrip().startswith("//"):
            continue
        for m in DISPLAY_RE.finditer(line):
            blob = m.group(0)
            name_m = NAME_RE.search(blob)
            if not name_m:
                continue
            name = name_m.group(1)
            if not name.strip():
                continue  # spacer row
            # [Browsable(false)] hides the property from the NT8 grid. Scan only
            # from the preceding line up to this property's own declaration —
            # a Browsable(false) after it belongs to the next property (usually
            # the XML-serialization shadow).
            hidden = "Browsable(false)" in lines[i - 1].replace(" ", "") if i else False
            for j in range(i, min(i + 8, len(lines))):
                if "Browsable(false)" in lines[j].replace(" ", ""):
                    hidden = True
                if PROP_RE.search(lines[j]):
                    break
            if hidden and not include_hidden:
                continue
            group_m = GROUP_RE.search(blob)
            group = group_m.group(1) if group_m else "<none>"
            if group.strip().lower() in SKIP_GROUPS:
                continue
            order_m = ORDER_RE.search(blob)
            desc_m = DESC_RE.search(blob)
            # look ahead for [Range] and the property declaration
            rng = ptype = default = None
            for j in range(i + 1, min(i + 8, len(lines))):
                nxt = lines[j]
                if not active[j] or nxt.lstrip().startswith("//"):
                    continue
                if rng is None:
                    r = RANGE_RE.search(nxt)
                    if r:
                        rng = r.group(1).strip()
                p = PROP_RE.search(nxt)
                if p:
                    ptype, _propname = p.group(1), p.group(2)
                    d = DEFAULT_RE.search(nxt)
                    if d:
                        default = d.group(1).strip()
                    break
                if "Display(" in nxt:
                    break
            params.append({
                "file": relpath, "line": i + 1, "name": name, "group": group,
                "order": int(order_m.group(1)) if order_m else 0,
                "desc": desc_m.group(1) if desc_m else "",
                "type": ptype, "default": default, "range": rng,
            })
    return params


# -------------------------------------------------------------------- docs side

def gnorm(s):
    """Normalise a group name / heading for loose comparison."""
    return re.sub(r'[^a-z0-9]', "", (s or "").lower())


def parse_docs(relpath):
    """Return documented rows from CANON tables, keyed by (heading, name)."""
    path = os.path.join(os.path.dirname(DOCS), relpath)
    if not os.path.exists(path):
        return {}, []
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    documented = {}
    thin = []
    heading = ""
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
        if line.startswith("|") and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i + 1].strip()):
            cells = [c.strip() for c in line.strip("|").split("|")]
            head = [c.lower() for c in cells]
            is_canon = head and head[0] == "setting" and not (len(head) > 1 and head[1] == "value")
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                if is_canon:
                    row = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                    if row and row[0]:
                        raw = re.sub(r'^\*\*|\*\*$', "", row[0]).strip()
                        # description column position varies between sections
                        desc = ""
                        for idx, col in enumerate(head[1:], start=1):
                            if col.startswith("description") and idx < len(row):
                                desc = row[idx]
                        if not desc and len(row) > 2:
                            desc = row[-1]
                        key = (gnorm(heading), norm(raw))
                        if key[1] and key not in documented:
                            documented[key] = (raw, desc, j + 1, heading)
                        if desc and raw and desc.strip().lower().rstrip(".") in (
                                raw.strip().lower(), raw.strip().lower() + " color",
                                raw.strip().lower() + " style", raw.strip().lower() + " font"):
                            thin.append((raw, desc, j + 1))
                j += 1
            i = j
            continue
        i += 1
    return documented, thin


# ---------------------------------------------------------------------- report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default="scripts/param-audit-report.md")
    args = ap.parse_args()

    out = ["# Parameter audit: docs vs. C# source", ""]
    out.append("Generated by `scripts/param_audit.py`. Retail (`!FREE`) parameter set.")
    out.append("")
    summary = []
    details = []
    total_missing = 0

    for page, srcs in TARGETS.items():
        params = []
        for s in srcs:
            params.extend(parse_source(s))
        # base params this page re-exposes via a [Browsable(true)] override
        wanted = REEXPOSED.get(page, [])
        if wanted:
            for p in parse_source("Core/CoreIndicator.cs", include_hidden=True):
                if p["name"] in wanted:
                    params.append(p)
        # collapse #1..#5 instances and duplicate (group,name) pairs
        logical = OrderedDict()
        for p in params:
            key = (p["group"].strip().lower(), norm(p["name"]))
            if key not in logical:
                logical[key] = p
        documented, thin = parse_docs(page)

        # params legitimately documented here but owned by a shared page
        inherited_names = set()
        for s in INHERITED.get(page, []):
            for p in parse_source(s):
                inherited_names.add(norm(p["name"]))

        by_name = {}
        for (h, n), v in documented.items():
            by_name.setdefault(n, []).append((h, v))

        missing, loose = [], []
        for (g, n), p in logical.items():
            hits = by_name.get(n)
            if not hits:
                missing.append(p)
                continue
            if any(h == gnorm(g) or (h and gnorm(g) and (h in gnorm(g) or gnorm(g) in h))
                   for h, _ in hits):
                continue          # documented under the matching section
            loose.append((p, hits[0][1]))   # documented, but under another heading

        src_names = {k[1] for k in logical} | inherited_names
        extra = [v for (h, n), v in documented.items() if n not in src_names]

        total_missing += len(missing)
        summary.append((page, len(logical), len(documented), len(missing), len(extra), len(thin)))

        details.append("")
        details.append(f"## {page}")
        details.append("")
        details.append(f"Source files: {', '.join('`%s`' % s for s in srcs)}")
        details.append("")
        details.append(f"- UI parameters in source (deduped): **{len(logical)}**")
        details.append(f"- Documented rows matched: **{len(documented) - len(extra)}**")
        details.append(f"- **Missing: {len(missing)}**")
        details.append("")

        if missing:
            by_group = OrderedDict()
            for p in missing:
                by_group.setdefault(p["group"], []).append(p)
            for group, items in by_group.items():
                details.append(f"### Missing — group `{group}` ({len(items)})")
                details.append("")
                details.append("| Order | Name | Type | Default | Range | Source Description | Location |")
                details.append("|---|---|---|---|---|---|---|")
                for p in sorted(items, key=lambda x: x["order"]):
                    details.append(
                        f"| {p['order']} | {p['name']} | {p['type'] or ''} | "
                        f"{p['default'] or ''} | {p['range'] or ''} | {p['desc']} | "
                        f"`{p['file']}:{p['line']}` |")
                details.append("")

        if loose:
            details.append(f"### Documented under a different heading ({len(loose)})")
            details.append("")
            details.append("Check the label matches the UI and sits in the right section.")
            details.append("")
            for p, v in sorted(loose, key=lambda x: x[1][2]):
                details.append(
                    f"- **{p['name']}** — source group `{p['group']}`, "
                    f"documented under \"{v[3]}\" at `{page}:{v[2]}`")
            details.append("")

        if extra:
            details.append(f"### Documented but not found in source ({len(extra)})")
            details.append("")
            details.append("Stale rows, renamed params, or labels that do not match the UI.")
            details.append("")
            for raw, desc, ln, head in sorted(extra, key=lambda x: x[2]):
                details.append(f"- **{raw}** — under \"{head}\" at `{page}:{ln}`")
            details.append("")

        if thin:
            details.append(f"### Thin descriptions ({len(thin)})")
            details.append("")
            for raw, desc, ln in thin:
                details.append(f"- **{raw}** → \"{desc}\" — `{page}:{ln}`")
            details.append("")

    out.append("## Summary")
    out.append("")
    out.append("| Page | In source | Documented | Missing | Stale | Thin |")
    out.append("|---|---|---|---|---|---|")
    for page, nsrc, ndoc, nmiss, nextra, nthin in summary:
        out.append(f"| `{page}` | {nsrc} | {ndoc} | **{nmiss}** | {nextra} | {nthin} |")
    out.append("")
    out.append(f"**Total missing: {total_missing}**")
    out.extend(details)

    text = "\n".join(out) + "\n"
    with open(args.report, "w", encoding="utf-8") as fh:
        fh.write(text)

    print("\n".join(out[:len(out) - len(details)]))
    print(f"\nFull report written to {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
