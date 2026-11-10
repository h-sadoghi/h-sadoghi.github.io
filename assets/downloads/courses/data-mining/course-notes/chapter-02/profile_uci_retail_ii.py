#!/usr/bin/env python3
"""Optional UCI Online Retail II Excel profiler (requires pandas/openpyxl).

Download the original dataset manually from https://archive.ics.uci.edu/dataset/502/online+retail+ii
Usage: python profile_uci_retail_ii.py path/to/online_retail_II.xlsx [max_rows]
Does not modify the input file, does not claim that the data is random sampled.
"""
from __future__ import annotations
import sys
from pathlib import Path

def main():
    try:
        import pandas as pd
    except ImportError:
        print('Optional packages missing: python -m pip install pandas openpyxl')
        return 2
    if len(sys.argv) < 2:
        print('Usage: python profile_uci_retail_ii.py <xlsx_file> [max_rows_per_sheet]')
        return 2
    p = Path(sys.argv[1])
    if not p.is_file():
        print('File not found:',p)
        return 2
    limit = int(sys.argv[2]) if len(sys.argv)>2 else 50000
    if limit<1:raise ValueError('max_rows must be positive')
    x = pd.ExcelFile(p)
    print('Sheets:',x.sheet_names)
    for sheet in x.sheet_names:
        df=pd.read_excel(x,sheet_name=sheet,nrows=limit)
        mapping={str(c).strip().lower().replace(' ','').replace('_',''):c for c in df.columns}
        print('\nSheet:',sheet,'rows examined:',len(df),'column labels:',list(df.columns))
        # Different UCI exports may vary in headers; report actual names first.
        idcol=next((mapping[k] for k in ['invoice','invoiceno'] if k in mapping),None)
        custcol=next((mapping[k] for k in ['customerid','customer'] if k in mapping),None)
        qtycol=next((mapping[k] for k in ['quantity'] if k in mapping),None)
        if idcol:
            invoice=df[idcol].astype('string').str.strip()
            print('distinct invoices:',invoice.nunique(dropna=True))
            print('cancellation-prefixed row fraction:',float(invoice.str.upper().str.startswith('C',na=False).mean()))
        if custcol:
            print('customer ID missing fraction:',float(df[custcol].isna().mean()))
        if qtycol:
            numeric=pd.to_numeric(df[qtycol],errors='coerce')
            print('negative quantity fraction:',float((numeric<0).mean()))
        print('null counts:',df.isna().sum().to_dict())
        print('WARNING: The first rows of the exported file are not a random sample.')
    return 0

if __name__=='__main__':raise SystemExit(main())
