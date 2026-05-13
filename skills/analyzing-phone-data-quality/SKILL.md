---
name: analyzing-phone-data-quality
description: Use when given a CSV of raw phone numbers to audit data quality, detect formatting patterns, find separators between multi-number cells, validate against a national standard, and produce a cleansing plan with invalid ratio and normalized output
---

# Analyzing Phone Data Quality

## Overview

Audit raw phone number CSV data to produce an actionable cleansing plan.

**Core principle:** Pipeline architecture keeps each stage independently testable.

```
reader → parse_cells → analyze → write_report
(raw_cell) (one row/number) (classified) (json+csv+md)
```

## Separator Detection

Detect in priority order to avoid false positives from spaces within formatted numbers:

```python
_SEPARATORS = [", ", " | ", "/", "\n"]  # explicit first

def detect_separator(cell: str) -> str:
    for sep in _SEPARATORS:
        if sep in cell:
            return sep
    if " " in cell.strip():
        tokens = [t for t in cell.split(" ") if t.strip()]
        if len(tokens) >= 2 and all(_looks_like_phone(t) for t in tokens):
            return " "     # confirmed space-separated numbers
    if len(cell) > 15:
        return "unknown_multi"   # too long, no recognized separator
    return "none"
```

Cells with `unknown_multi` → override to `invalid_reason="unparseable"` after analysis.

## Thai Phone Validation

| Type | Digits | Example |
|------|--------|---------|
| Mobile | 10 | `085-123-4567` |
| Landline | 9 | `02-123-4567` |

Valid = starts with `0`, digit count is 9 or 10.

**International prefix:** strip before validating: `+66XX → 0XX`, `66XX → 0XX`.

**Format fingerprint:** `re.sub(r"\d", "N", raw.strip())` — groups variants like `NNN-NNN-NNNN` vs `NNNNNNNNNN`.

## Key Polars Patterns

```python
# Read headerless single-column CSV, all strings
df = pl.read_csv(path, has_header=False, new_columns=["raw_cell"],
                 infer_schema_length=0, truncate_ragged_lines=True)

# Empty cells are None, not "" — use is_null()
empty = df.filter(df["raw_cell"].is_null() | (df["raw_cell"].str.strip_chars() == "")).height

# Apply struct-returning function then unnest
result = df.with_columns(
    df["raw_number"].map_elements(classify_number,
        return_dtype=pl.Struct({"digit_count": pl.Int32, "is_valid": pl.Boolean, ...})
    ).alias("_c")
).unnest("_c")

# After explode(), deduplicate before counting separators per cell
df.select(["cell_idx", "cell_separator"]).unique("cell_idx") \
  .group_by("cell_separator").agg(pl.len())
```

## Outputs

| File | Contents |
|------|----------|
| `summary.json` | Totals: valid/invalid counts, separator distribution, format patterns |
| `detail.csv` | One row per extracted number with all classification fields |
| `executive-report.md` | Headline (strict valid/invalid/empty), At-a-Glance table, §1 Invalid Analysis (5 defect-type groups, descriptive), §2 Recommended Actions (yield-layering + action plan), §3 Decisions Required, AI Insights |

### Executive Summary Headline

The `executive-report.md` opens with a single bold sentence in three-way form,
followed by three bullets that orient the reader:

```
**X% of N cells in <file> are valid as stored;
Y% are invalid and Z% are empty.**

- Dataset: N cells from <file>
- Top invalid groups (cells): Format f · Structural s · Wrong-type w · ...
- Decisions required: see §3
```

Recovery framing (auto-cleanup, splitting, yields) belongs in §2 Recommended
Actions — never in the headline or §1.

## Strict Validity Rule

A cell is *valid* iff it stores exactly one `0XXXXXXXXX` 10-digit mobile number
— no formatting, no prefix, no whitespace. Anything else is invalid.

## Recovery Actions

These run **after** validity classification — they do not affect §1 of the report.

1. Auto-clean Format defects: strip non-digit chars; normalize `+66` / `66` prefix
2. Split Structural defects: split on detected separator; primary number → `phone`, rest → `PspInf.PspPcsTel`
3. Route landline / wrong-length / non-numeric / unparseable → `PspInf.PspPcsTel` as free text
4. Empty source cells → both fields NULL

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `phonenumbers` library for Thai | Pure regex is sufficient |
| Counting separators after explode | `unique("cell_idx")` first |
| `== ""` for null check | Use `.is_null()` — Polars nulls are `None` |
| `unknown_multi` cells left valid | Override after classify: always → `is_valid=False, invalid_reason="unparseable"` |
| Folding `needs_cleanup` into the valid headline | `needs_cleanup` is invalid until Step 1 of the recovery plan runs. Keep validity strict in §1; quantify recovery only in §2. |

## Key Decisions for Stakeholders

1. Multi-number cells: split into separate rows, or add `alt_phone` column?
2. 9-digit landlines: retain or filter?
3. International numbers (~120 in 655k-row set): keep separately or discard?
4. "Don't know" text entries: NULL or flag separately?
