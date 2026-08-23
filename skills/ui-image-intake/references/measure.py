#!/usr/bin/env python3
"""Measure a UI mock: DPR, element edges, pitch, box extents, colour, type metrics.

Emits CSS px (image px / DPR) so values compare directly against
getBoundingClientRect() in verify-ui-against-design-headless.

Every failure is a value in the output, never an exception: a caller that cannot
distinguish "measured 0" from "could not measure" will record a guess as evidence.
"""
import argparse, json, sys
from collections import Counter

try:
    import numpy as np
    from PIL import Image
except ImportError as e:
    print(json.dumps({"error": f"missing dependency: {e}. Needs PIL and numpy."}))
    sys.exit(2)

# Deviation of 2 levels separates a shadow ramp from a flat fill; a real boundary
# always jumps at least 5 levels in one pixel, which is what rejects slow gradients.
DEV_THRESH = 2
MIN_STEP = 5
MIN_PLATEAU = 3
MAX_RAMP = 24
MIN_AREA = 800
CLOSE_RADIUS = 5
CHROME_COVERAGE = 0.85


# ---------------------------------------------------------------- primitives

def find_edge(profile):
    """Locate an element boundary along a profile whose first sample is background.

    Returns (index_of_first_fill_pixel, kind) or (None, reason). Two structures
    occur in real mocks: a hard colour step, and a shadow ramp that dips away from
    the background and recovers to the fill. Taking argmax|d| instead finds
    whichever interior content step is strongest, which is not the boundary.
    """
    p = np.asarray(profile, dtype=float)
    if len(p) < MIN_PLATEAU + 1:
        return None, "window too short"
    bg = p[0]
    dev = np.abs(p - bg)
    hits = np.where(dev >= DEV_THRESH)[0]
    if len(hits) == 0:
        return None, "uniform"
    start = int(hits[0])
    end = start
    while end + 1 < len(p) and dev[end + 1] >= DEV_THRESH:
        end += 1
    if float(dev[start:end + 1].max()) < MIN_STEP:
        return None, f"sub-threshold depth {dev[start:end + 1].max():.0f}"

    after = end + 1
    if after + MIN_PLATEAU <= len(p) and (end - start + 1) <= MAX_RAMP:
        plateau = p[after:after + MIN_PLATEAU]
        recovered = np.all(np.abs(plateau - bg) < DEV_THRESH) and np.ptp(plateau) <= 1
        if recovered and abs(p[after] - p[end]) >= MIN_STEP:
            return after, "ramp"

    if end - start + 1 < MIN_PLATEAU:
        return None, f"transient {end - start + 1}px"
    jump = abs(p[start] - p[start - 1]) if start > 0 else float(dev[start:end + 1].max())
    if jump < MIN_STEP:
        return None, f"gradual {jump:.0f}/px, no step"
    return start, "step"


def measure_side(lum, axis, outer, inner, offsets):
    """Vote a boundary across offsets along the side.

    Unanimity is the wrong bar: any single offset can start on content rather than
    background, which is how a clean edge reads as three different values.
    """
    votes, kinds = [], []
    lo, hi = min(outer, inner), max(outer, inner)
    for f in offsets:
        if axis == 'x':
            if not (0 <= f < lum.shape[0]):
                continue
            prof = lum[f, lo:hi + 1]
        else:
            if not (0 <= f < lum.shape[1]):
                continue
            prof = lum[lo:hi + 1, f]
        if outer > inner:
            prof = prof[::-1]
        idx, kind = find_edge(prof)
        kinds.append(kind)
        if idx is not None:
            votes.append((outer + idx) if outer < inner else (outer - idx))
    if not votes:
        reason = Counter(kinds).most_common(1)[0][0] if kinds else "no samples"
        return {"value": None, "refused": reason}
    val, n = Counter(votes).most_common(1)[0]
    frac = n / len(votes)
    out = {"value": int(val), "agreement": round(frac, 2), "samples": len(votes),
           "boundary": Counter(kinds).most_common(1)[0][0]}
    if frac <= 0.5:
        out["value"] = None
        out["refused"] = f"no majority across {len(votes)} offsets"
    return out


def refine_box(lum, dbox, margins=(8, 16, 24, 32)):
    """Replace a discovery box with voted edges on all four sides.

    A discovery box is exact on a hard colour step and inflated on a shadow ramp,
    so no measured value may come from one directly.
    """
    x0, y0, x1, y1 = dbox
    ys = [y for y in range(y0 + (y1 - y0) // 6, y1, max(1, (y1 - y0) // 9))]
    xs = [x for x in range(x0 + (x1 - x0) // 6, x1, max(1, (x1 - x0) // 9))]
    H, W = lum.shape
    # Search inward as far as the box centre. A shadow ramp inflates the discovery
    # box by more than a fixed margin, which would leave the true edge outside a
    # window anchored on the inflated side.
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2

    def widen(axis, edge, inner, offsets, outward):
        """Start just outside the box and widen only on refusal.

        A wide first window reaches past the boundary into unrelated content, which
        votes for the wrong edge instead of reporting that it found nothing.
        """
        last = {"value": None, "refused": "no window produced a majority"}
        for m in margins:
            outer = edge + (m * outward)
            outer = max(0, min((W - 1) if axis == 'x' else (H - 1), outer))
            r = measure_side(lum, axis, outer, inner, offsets)
            r["margin"] = m
            if r.get("value") is not None:
                return r
            last = r
        return last

    sides = {
        "left":   widen('x', x0, cx, ys, -1),
        "right":  widen('x', x1, cx, ys, +1),
        "top":    widen('y', y0, cy, xs, -1),
        "bottom": widen('y', y1, cy, xs, +1),
    }
    got = {k: v["value"] for k, v in sides.items()}
    box = None
    if all(v is not None for v in got.values()):
        box = [got["left"], got["top"], got["right"], got["bottom"]]
    return box, sides


def autocorr_pitch(mask1d):
    """Repeat interval of a run of like items.

    Adjacent differences measure ink-to-ink, which is gap plus twice the padding
    inset whenever the item box is transparent; autocorrelation measures the repeat.
    """
    m = np.asarray(mask1d, dtype=float)
    m = m - m.mean()
    n = len(m)
    if n < 16:
        return None
    best, best_v = None, -1e18
    for lag in range(4, n // 2):
        v = float(np.dot(m[:-lag], m[lag:]))
        if v > best_v:
            best, best_v = lag, v
    return best


def run_centres(mask1d):
    runs, s = [], None
    for i, v in enumerate(mask1d):
        if v and s is None:
            s = i
        elif not v and s is not None:
            runs.append((s, i - 1))
            s = None
    if s is not None:
        runs.append((s, len(mask1d) - 1))
    return runs


def measure_pitch(lum, region):
    x0, y0, x1, y1 = region
    sub = lum[y0:y1 + 1, x0:x1 + 1]
    u, c = np.unique(sub, return_counts=True)
    modal = u[c.argmax()]
    mask = (np.abs(sub - modal) >= DEV_THRESH).any(axis=0)
    ac = autocorr_pitch(mask)
    runs = run_centres(mask)
    ctr = [(a + b) / 2 for a, b in runs]
    out = {"autocorr": ac, "runs": len(runs)}
    if ac is None or len(ctr) < 2:
        out["refused"] = "not enough repeated items"
        return out
    # Ink runs are not items: an icon with a keyboard-hint superscript is two runs
    # of one item, so span over run count understates the period. Constraining the
    # total span to a whole number of autocorrelation periods gives the sub-pixel
    # value without needing to know how many runs each item contributes.
    total = ctr[-1] - ctr[0]
    periods = round(total / ac) if ac else 0
    if periods < 1:
        out["refused"] = "span shorter than one period"
        return out
    refined = total / periods
    out["periods"] = int(periods)
    out["span_total"] = round(total, 2)
    if abs(refined - ac) > 1:
        out["ambiguous"] = True
        out["note"] = "integer-period refinement disagrees with the autocorrelation lag"
    elif refined < 8:
        out["ambiguous"] = True
        out["note"] = ("period below 8px is glyph texture rather than item pitch - "
                       "restrict the region to the row's own box")
    else:
        out["pitch"] = round(refined, 2)
    return out


def exact_extents(rgb, region, min_coverage=0.02):
    """Extent of each exact colour in a region.

    A filled or selected state is the only place the item box is directly visible
    when the resting box is transparent.
    """
    x0, y0, x1, y1 = region
    sub = rgb[y0:y1 + 1, x0:x1 + 1]
    flat = sub.reshape(-1, 3)
    packed = (flat[:, 0].astype(np.int32) << 16) | (flat[:, 1].astype(np.int32) << 8) | flat[:, 2]
    vals, counts = np.unique(packed, return_counts=True)
    total = len(packed)
    order = np.argsort(-counts)
    out = []
    for i in order:
        frac = counts[i] / total
        if frac < min_coverage:
            break
        v = int(vals[i])
        col = ((v >> 16) & 255, (v >> 8) & 255, v & 255)
        m = np.all(sub == col, axis=2)
        rr = np.where(m.any(axis=1))[0]
        cc = np.where(m.any(axis=0))[0]
        out.append({
            "hex": "#%02x%02x%02x" % col,
            "coverage": round(float(frac) * 100, 2),
            "box": [int(x0 + cc[0]), int(y0 + rr[0]), int(x0 + cc[-1]), int(y0 + rr[-1])],
            "w": int(cc[-1] - cc[0] + 1), "h": int(rr[-1] - rr[0] + 1),
        })
    return out


# ---------------------------------------------------------------- colour

def srgb_to_lab(rgb_tuple):
    def inv(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (inv(float(v)) for v in rgb_tuple)
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    xn, yn, zn = 0.95047, 1.0, 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)
    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def de76(a, b):
    la, lb = srgb_to_lab(a), srgb_to_lab(b)
    return sum((x - y) ** 2 for x, y in zip(la, lb)) ** 0.5


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def load_tokens(path):
    """Accept either a flat {name: hex} map or the resolver's wrapped output."""
    doc = json.load(open(path))
    inner = doc.get("tokens") if isinstance(doc, dict) else None
    return inner if isinstance(inner, dict) else doc


def nearest_token(hexcol, tokens):
    """Nearest token by CIE76 in Lab. dE above 10 is reported, not silently snapped."""
    if not tokens:
        return None
    target = hex_to_rgb(hexcol)
    scored = sorted(((de76(target, hex_to_rgb(v)), k, v) for k, v in tokens.items()
                     if isinstance(v, str) and v.startswith('#') and len(v) == 7))
    if not scored:
        return None
    d, name, val = scored[0]
    out = {"token": name, "token_hex": val, "dE": round(d, 1)}
    if len(scored) > 1:
        out["runner_up"] = {"token": scored[1][1], "dE": round(scored[1][0], 1)}
    if d > 10:
        out["off_scale"] = True
        out["action"] = "not in the scale - ask whether to add a token or use the raw hex"
    return out


# ---------------------------------------------------------------- type

def type_metrics(lum, region):
    """Glyph ink runs give cap height, x-height, ascender, descender and baseline.

    font-size follows from the cap ratio, so it carries the ratio assumption and
    the neighbouring candidates rather than presenting one number as measured.
    """
    x0, y0, x1, y1 = region
    sub = lum[y0:y1 + 1, x0:x1 + 1]
    u, c = np.unique(sub, return_counts=True)
    bg = u[c.argmax()]
    mask = np.abs(sub - bg) >= 40
    if not mask.any():
        return {"refused": "no ink in region"}
    runs = run_centres(mask.any(axis=0))
    tops, bots = [], []
    for a, b in runs:
        rr = np.where(mask[:, a:b + 1].any(axis=1))[0]
        if len(rr):
            tops.append(int(rr[0]))
            bots.append(int(rr[-1]))
    if not tops:
        return {"refused": "no glyph runs"}
    baseline = max(bots)
    heights = sorted({baseline - t + 1 for t in tops})
    cap = heights[-1] if heights else None
    xh = Counter(baseline - t + 1 for t in tops).most_common(1)[0][0]
    desc = max(bots) - baseline
    ratio = 0.71
    fs = round(cap / ratio) if cap else None
    return {"glyphs": len(runs), "baseline_row": int(y0 + baseline),
            "cap_height": int(cap), "x_height": int(xh),
            "ascender": int(cap), "descender": int(desc),
            "font_size_px": fs, "cap_ratio_assumed": ratio,
            "candidates": [c for c in (fs - 1, fs, fs + 1)] if fs else None,
            "accuracy": "+/-1px"}


# ---------------------------------------------------------------- discovery + DPR

def discover(lum):
    u, c = np.unique(lum, return_counts=True)
    bg = u[c.argmax()]
    mask = np.abs(lum - bg) >= DEV_THRESH
    # Full-width rules and window chrome are not elements; they merge everything.
    rowcov = mask.mean(axis=1)
    colcov = mask.mean(axis=0)
    mask[rowcov > CHROME_COVERAGE, :] = False
    mask[:, colcov > CHROME_COVERAGE] = False
    m = mask.copy()
    for _ in range(CLOSE_RADIUS):
        m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    for _ in range(CLOSE_RADIUS):
        e = m.copy()
        for sh, ax in ((1, 0), (-1, 0), (1, 1), (-1, 1)):
            e &= np.roll(m, sh, ax)
        m = e
    H, W = m.shape
    seen = np.zeros_like(m, dtype=bool)
    boxes = []
    for sy in range(H):
        for sx in range(W):
            if not m[sy, sx] or seen[sy, sx]:
                continue
            stack = [(sy, sx)]
            seen[sy, sx] = True
            minx = maxx = sx
            miny = maxy = sy
            area = 0
            while stack:
                cy, cx = stack.pop()
                area += 1
                if cx < minx: minx = cx
                if cx > maxx: maxx = cx
                if cy < miny: miny = cy
                if cy > maxy: maxy = cy
                for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                    if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
            if area > MIN_AREA:
                boxes.append({"discovery_box": [int(minx), int(miny), int(maxx), int(maxy)],
                              "area": int(area)})
    boxes.sort(key=lambda b: -b["area"])
    return boxes


def transition_widths(lum):
    """Pixel width of each strong transition.

    A pixel-exact capture crosses a real boundary in one pixel; resampling spreads
    the same boundary over two or three intermediate values.
    """
    out = []
    for y in range(0, lum.shape[0], 2):
        row = lum[y].astype(int)
        d = np.diff(row)
        i = 0
        while i < len(d):
            if abs(d[i]) >= 15:
                sgn = np.sign(d[i])
                w, tot, j = 1, d[i], i + 1
                while j < len(d) and np.sign(d[j]) == sgn and abs(d[j]) >= 3:
                    w += 1
                    tot += d[j]
                    j += 1
                if abs(tot) >= 40:
                    out.append(w)
                i = j
            else:
                i += 1
    return np.array(out)


def detect_dpr(lum, rgb):
    """A pixel-exact 1x capture has 1px hard-edged runs and no antialiasing.

    Refusing beats guessing: at 2x, 36 and 72 are equally plausible tokens.
    """
    u, c = np.unique(lum, return_counts=True)
    bg = u[c.argmax()]
    mask = np.abs(lum - bg) >= DEV_THRESH
    lens = []
    step = max(1, lum.shape[0] // 200)
    for y in range(0, lum.shape[0], step):
        for a, b in run_centres(mask[y]):
            lens.append(b - a + 1)
    if not lens:
        return {"dpr": None, "refused": "no ink found"}
    ones = sum(1 for L in lens if L == 1) / len(lens)
    distinct = len(np.unique(rgb.reshape(-1, 3), axis=0))
    total_px = lum.shape[0] * lum.shape[1]
    aa_ratio = distinct / total_px
    widths = transition_widths(lum)
    sharp = float(np.mean(widths == 1)) if len(widths) else 0.0
    per_mpx = distinct / (total_px / 1e6)
    out = {"one_px_run_fraction": round(ones, 3), "distinct_colours": int(distinct),
           "distinct_per_megapixel": round(per_mpx, 1),
           "single_pixel_transitions": round(sharp, 3), "runs_sampled": len(lens)}

    pixel_exact = ones >= 0.05 and per_mpx < 2000 and sharp >= 0.50
    if pixel_exact:
        out["pixel_exact"] = True
        out["dpr"] = 2 if (lens and all(L % 2 == 0 for L in lens)) else 1
        if out["dpr"] == 2:
            out["note"] = "all run lengths even; values divided by 2"
        return out

    out["pixel_exact"] = False
    out["dpr"] = None
    out["mode"] = "snap-only"
    if per_mpx >= 2000 or sharp < 0.50:
        out["refused"] = ("not a pixel-exact capture - measurement unavailable, snap mode only. "
                          "A resampled or photographed capture can still look sharp, and a clean "
                          "integer downscale keeps geometry integral, so confirm the capture is a "
                          "1x screenshot before trusting any measurement from it.")
    else:
        out["refused"] = "inconclusive - confirm this is an unscaled 1x screenshot"
    return out


# ---------------------------------------------------------------- report

def load(path):
    im = Image.open(path)
    rgb = np.array(im.convert('RGB')).astype(int)
    lum = np.array(im.convert('L')).astype(int)
    return rgb, lum


def full_report(path):
    rgb, lum = load(path)
    dpr_info = detect_dpr(lum, rgb)
    rep = {"image": path, "size": [int(lum.shape[1]), int(lum.shape[0])],
           "unit": "css-px", "dpr": dpr_info}
    if not dpr_info.get("pixel_exact"):
        rep["regions"] = []
        rep["note"] = "no measurements emitted while the capture is not pixel-exact"
        return rep
    d = dpr_info["dpr"]
    regions = []
    for b in discover(lum)[:20]:
        box, sides = refine_box(lum, b["discovery_box"])
        entry = {"discovery_box": b["discovery_box"], "area": b["area"],
                 "box": box, "sides": sides}
        if box:
            entry["w"] = (box[2] - box[0] + 1) // d
            entry["h"] = (box[3] - box[1] + 1) // d
            entry["fills"] = exact_extents(rgb, box)[:6]
        regions.append(entry)
    rep["regions"] = regions
    return rep


# ---------------------------------------------------------------- selftest

def selftest(fixtures_dir):
    import os
    gold_path = os.path.join(fixtures_dir, "golden.json")
    gold = json.load(open(gold_path))
    pos = os.path.join(fixtures_dir, gold["positive_fixture"])
    neg = os.path.join(fixtures_dir, gold["negative_fixture"])
    rgb, lum = load(pos)
    fails = []

    def check(name, got, want):
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: got {got}" + ("" if ok else f", want {want}"))
        if not ok:
            fails.append(name)

    print("edges (exact):")
    for e in gold["edges"]:
        r = measure_side(lum, e["axis"], e["outer"], e["inner"], range(*e["offsets"]))
        check(e["name"], r["value"], e["expect"])

    print("box extents (exact):")
    for b in gold["boxes"]:
        got = None
        for f in exact_extents(rgb, b["region"]):
            if f["hex"] == b["hex"]:
                got = [f["w"], f["h"]]
                break
        check(b["name"], got, b["expect_wh"])

    print("pitch:")
    for p in gold["pitch"]:
        r = measure_pitch(lum, p["region"])
        got = r.get("pitch")
        ok = got is not None and abs(got - p["expect"]) <= p.get("tol", 0.4)
        print(f"  {'PASS' if ok else 'FAIL'}  {p['name']}: got {got}, want {p['expect']}+/-{p.get('tol',0.4)}")
        if not ok:
            fails.append(p["name"])

    print("colour -> token:")
    tokens = gold["tokens"]
    for c in gold["colours"]:
        r = nearest_token(c["hex"], tokens)
        got = r["token"] if r else None
        ok = got == c["expect_token"] and abs(r["dE"] - c["expect_dE"]) <= 0.3
        print(f"  {'PASS' if ok else 'FAIL'}  {c['hex']}: got {got} dE {r['dE'] if r else '-'}, "
              f"want {c['expect_token']} dE {c['expect_dE']}")
        if not ok:
            fails.append(c["hex"])

    print("type metrics (+/-1px):")
    for t in gold["type"]:
        r = type_metrics(lum, t["region"])
        got, cap = r.get("font_size_px"), r.get("cap_height")
        ok = (got is not None and abs(got - t["expect_font_size"]) <= 1
              and cap == t["expect_cap"])
        print(f"  {'PASS' if ok else 'FAIL'}  {t['name']}: cap {cap} font-size {got}, "
              f"want cap {t['expect_cap']} font-size {t['expect_font_size']}+/-1")
        if not ok:
            fails.append(t["name"])

    print("landmark coverage (stability, never the region count):")
    boxes = [b["discovery_box"] for b in discover(lum)]
    for lm in gold["landmarks"]:
        x0, y0, x1, y1 = lm["box"]
        hit = any(not (b[2] < x0 or b[0] > x1 or b[3] < y0 or b[1] > y1) for b in boxes)
        print(f"  {'PASS' if hit else 'FAIL'}  {lm['name']} overlapped by a discovered region")
        if not hit:
            fails.append(f"landmark {lm['name']}")
    print(f"  (discovered {len(boxes)} regions; count is deliberately not asserted)")

    print("negative: edges must refuse")
    for n in gold["negative_edges"]:
        i, kind = find_edge(lum[n["y"], n["x0"]:n["x1"] + 1])
        ok = i is None
        print(f"  {'PASS' if ok else 'FAIL'}  {n['name']}: {'refused (' + kind + ')' if ok else 'found edge at ' + str(i)}")
        if not ok:
            fails.append(n["name"])
    g = np.arange(60, dtype=float) + 200.0
    i, kind = find_edge(g)
    ok = i is None
    print(f"  {'PASS' if ok else 'FAIL'}  synthetic 1-level/px gradient: "
          f"{'refused (' + kind + ')' if ok else 'found edge'}")
    if not ok:
        fails.append("synthetic gradient")

    print("negative fixture: whole-image refusal")
    nrgb, nlum = load(neg)
    nd = detect_dpr(nlum, nrgb)
    ok = nd.get("pixel_exact") is False and nd.get("mode") == "snap-only"
    print(f"  {'PASS' if ok else 'FAIL'}  0.75x fixture refuses: {nd.get('refused', nd)}")
    if not ok:
        fails.append("negative fixture refusal")
    rep = full_report(neg)
    ok2 = rep.get("regions") == []
    print(f"  {'PASS' if ok2 else 'FAIL'}  0.75x fixture emits no measurements")
    if not ok2:
        fails.append("negative fixture emitted measurements")

    print()
    if fails:
        print(f"FAILED {len(fails)}: {', '.join(fails)}")
        return 1
    print("all assertions passed")
    return 0


SUBCOMMANDS = ("pitch", "type", "color", "regions", "edges", "selftest")


def main():
    # The primary interface is a bare image path; subcommands are drill-down only.
    # argparse would read that path as an invalid subcommand choice, so route first.
    argv = sys.argv[1:]
    if argv and argv[0] not in SUBCOMMANDS and not argv[0].startswith("-"):
        print(json.dumps(full_report(argv[0]), indent=2))
        return

    ap = argparse.ArgumentParser(
        description="Measure a UI mock. Emits CSS px. Refusals are values, not exceptions.",
        epilog="Primary use: measure.py IMAGE  (one JSON document for the whole screen)")
    sub = ap.add_subparsers(dest="cmd")

    def region_arg(p):
        p.add_argument("--region", required=True, help="x0,y0,x1,y1")
        p.add_argument("image")

    region_arg(sub.add_parser("pitch", help="repeat interval of a row of like items"))
    region_arg(sub.add_parser("type", help="cap height, x-height, font-size"))
    c = sub.add_parser("color", help="exact-colour histogram and nearest token")
    c.add_argument("--region", required=True)
    c.add_argument("--top", type=int, default=6)
    c.add_argument("--tokens", help="JSON file of {name: hex}")
    c.add_argument("image")
    r = sub.add_parser("regions", help="discovered regions (locator only)")
    r.add_argument("image")
    e = sub.add_parser("edges", help="voted boundary for one side")
    e.add_argument("--region", required=True)
    e.add_argument("image")
    s = sub.add_parser("selftest", help="check against fixtures/golden.json")
    s.add_argument("--fixtures", default=None)
    args = ap.parse_args()

    if args.cmd == "selftest":
        import os
        fx = args.fixtures or os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
        sys.exit(selftest(fx))

    if args.cmd is None:
        ap.print_help()
        sys.exit(1)

    rgb, lum = load(args.image)
    reg = [int(v) for v in args.region.split(",")] if getattr(args, "region", None) else None
    if args.cmd == "regions":
        print(json.dumps(discover(lum), indent=2))
    elif args.cmd == "pitch":
        print(json.dumps(measure_pitch(lum, reg), indent=2))
    elif args.cmd == "type":
        print(json.dumps(type_metrics(lum, reg), indent=2))
    elif args.cmd == "edges":
        box, sides = refine_box(lum, reg)
        print(json.dumps({"box": box, "sides": sides}, indent=2))
    elif args.cmd == "color":
        tokens = load_tokens(args.tokens) if args.tokens else {}
        out = exact_extents(rgb, reg)[:args.top]
        for o in out:
            nt = nearest_token(o["hex"], tokens)
            if nt:
                o["nearest"] = nt
        print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
