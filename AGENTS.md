# AGENTS.md

Guidance for AI agents working in this repository.

## Project Overview

A Streamlit web app that converts accounting CSV exports (e.g. Xero "Account Transactions" reports) into a multi-sheet Excel workbook, splitting transactions by account and labelling each row as Transaction / Opening / Closing / Total / Account Name / Blank.

## Stack

- Python 3.12+ (Railway runtime)
- Streamlit (web UI)
- pandas, numpy, altair, xlsxwriter, tqdm, python-dateutil

## Deployment

Railway via nixpacks. Run locally with:

```
streamlit run app.py
```

Deployment config lives in `Procfile`, `railway.toml`, `.streamlit/config.toml`, and `requirements.txt`.

## Commands

- Run app: `streamlit run app.py`
- Type-check: `python3 -m py_compile app.py`
- No test suite exists.

## Code Conventions

- All logic is in a single file, `app.py`. Do not split into modules unless asked.
- No comments unless explicitly requested.
- 2-space indentation is used throughout `app.py` — match it when editing existing functions.
- Functions are defined at module top; the Streamlit UI runs as top-level script after the function defs.

## pandas Gotchas (IMPORTANT)

This codebase has been bitten repeatedly by pandas indexing and dtype changes. When editing `app.py`:

- **Never use chained indexing** like `df.iloc[i][j]` or `row[-1]`. The first selection returns a Series; the second then indexes **by label**, not position, which raises `KeyError` for integer keys when columns are strings or when negative labels are unsupported.
  - Use `df.iloc[i, j]` (single call, two positional args) for DataFrame cells.
  - Use `row.iloc[-1]` / `row.iloc[-2]` / `row.iloc[-3]` for Series positional access.
- **`pd.to_datetime(..., errors='ignore')` was removed in pandas 2.0.** Use `errors='coerce'` (invalid values become `NaT`, whose type != `Timestamp`, preserving the original logic).
- **pandas 3.x defaults object columns to a strict `str` dtype** that rejects assigning numeric values into them in place. To convert a string column to numeric, reassign the whole column by name rather than overwriting in place:
  ```python
  df[col] = pd.to_numeric(df[col].apply(replace_to_number), errors='coerce')
  ```
  Avoid `df.iloc[:, k] = <numeric series>` for columns currently holding strings.
- When setting a single cell by position on a column that may have any dtype, use `df.iloc[i, df.columns.get_loc('ColumnName')] = value` rather than `df.iloc[i]['ColumnName'] = value`.

## Verification

After editing `app.py`, before reporting done:

1. `python3 -m py_compile app.py` — must succeed.
2. Run the end-to-end harness below (requires only pandas + tqdm + python-dateutil installed; streamlit and altair are stubbed) to confirm the sample CSV processes without error:

```
python3 << 'EOF'
import sys, types, io as _io
import pandas as pd
import math, re, time, datetime, numpy as np
from tqdm import tqdm
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date

sys.modules['altair'] = types.ModuleType('altair')
class StubFile(_io.BytesIO):
    def __init__(self, p): super().__init__(open(p,'rb').read())
st = types.ModuleType('streamlit')
st.title = lambda *a, **k: None
class _P:
    def progress(self, v): pass
st.progress = lambda x: _P()
st.file_uploader = lambda *a, **k: StubFile('AustGrade_Mascot_Swimming_Pty_Ltd_-_Account_Transactions (1).csv')
st.download_button = lambda **k: None
sys.modules['streamlit'] = st
exec(open('app.py').read())
print('OK')
EOF
```

Expect `OK` on the last line. Any traceback means a regression.

## Files

- `app.py` — entire application (functions + Streamlit script).
- `requirements.txt` — pip dependencies for Railway/local.
- `Procfile` / `railway.toml` / `.streamlit/config.toml` — deployment config.
- `AustGrade_Mascot_Swimming_Pty_Ltd_-_Account_Transactions (1).csv` — sample input used for verification.
- `RAILWAY_FIX.md` — notes on a previous Railway build fix.