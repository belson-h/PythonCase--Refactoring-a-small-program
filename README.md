# PythonCase--Refactoring-a-small-program

A Python program that reads order data, validates and cleans it, calculates order values and discounted values, and compiles sales and returns reports by product category and region.

The program is a refactored version of a previously linear script. The same calculations and the same main results are preserved, but the code has been restructured into clearly separated modules to make it easier to understand, test, and maintain.

## What the program does

From a CSV file with order data, the program creates four reports:

- **`overview.csv`** - overall key figures (total sales, number of orders, number of returns)
- **`sales_by_category.csv`** - sales and returns by product category
- **`sales_by_region.csv`** - sales and returns by region
- **`returns_by_category.csv`** - return rate by product category

## Setup / installation

The project uses a `src/` layout. Install in editable mode so that the package and test dependencies become available:

```powershell
pip install -e .[test]
```

### Dependencies

- Python 3.10+
- pandas
- pytest (to run the tests)

## How to run the program

Run the program as a module from the project's top level (the folder containing `pyproject.toml`):

```powershell
python -m order_report
```

The program reads input data from `data/orders.csv` and saves the four reports in the `output/` folder.
The paths can be changed in `config.py` (`ReportConfig`).

## How to run the tests

```powershell
pytest
```

Or to run a specific test file with detailed output:

```powershell
pytest tests/test_transformation.py -v
```

The tests cover both normal cases and relevant edge cases, e.g. missing required columns and empty input data.

## Project structure

```
order_report/
├── pyproject.toml
├── data/
│   └── orders.csv
├── output/                    # created automatically, contains the reports
├── src/
│   └── order_report/
│       ├── __main__.py        # entry point (python -m order_report)
│       ├── config.py          # ReportConfig – paths for input/output
│       ├── pipeline.py        # ties the whole flow together (run)
│       ├── preprocessing.py   # loading, column validation, data cleaning
│       ├── transformation.py  # calculations: order_value, discounted_value, return_rate
│       ├── reporting.py       # aggregation: overview, summarize_by
│       └── io_utils.py        # file handling: load_orders, save_report
└── tests/
    ├── test_preprocessing.py
    └── test_transformation.py
```

## Design decisions worth knowing

- `returns_by_category.csv` includes a `total_sales` column that was not present in the original. This is a deliberate simplification (the same `summarize_by` function is used for all three grouped reports) and does not affect the meaning of the other figures.
- With empty input data (0 rows), the program does not raise an error; instead `unit_price` is filled with `NaN` (the median of an empty series). This is the same behavior as in the original script and is documented via a dedicated test.
