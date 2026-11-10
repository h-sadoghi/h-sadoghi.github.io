# Chapter 02 — Reproducible materials

All included CSVs are **synthetic teaching examples**, not samples of any UCI dataset.

## Windows one-click

Double-click `RUN_CHAPTER02_EXAMPLES.cmd` inside `downloads`. Python 3.10+ is needed, but **no third-party packages** are needed for `chapter02_examples.py`.

## Other platforms

```bash
python chapter02_examples.py
```

The script reads `retail_lines_synthetic.csv` and `measurements_synthetic.csv` from its own directory and prints a data-quality audit, a robust summary, a Simpson paradox and a missingness-bias calculation. It does **not modify input data**.

The companion `chapter02_examples.ipynb` opens in Jupyter and uses the same files. To use the optional **real** UCI Online Retail II dataset, download it from https://archive.ics.uci.edu/dataset/502/online+retail+ii and run:

```bash
python -m pip install pandas openpyxl
python profile_uci_retail_ii.py "path/to/online_retail_II.xlsx" 50000
```

The profiler is **read-only**; rows at the beginning of the dataset are **not a representative random sample**. The downloaded real dataset is not redistributed here. Cite its DOI: https://doi.org/10.24432/C5CG6D.

For reproducibility, Python 3.10+ is sufficient for the core examples. External links are optional and are not required to run the chapter demonstration.
