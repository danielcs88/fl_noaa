# pylint: disable=pointless-string-statement, pointless-statement
# %%
r"""
Time Series tidy Pandas DataFrame script.
"""

# %%
__author__ = "Daniel Cárdenas"
__version__ = "1.0"
__maintainer__ = "Daniel Cárdenas"
__email__ = "jcard151@fiu.edu"

# %%
import os
import re

import pandas as pd

# %%
import ftp  # This will download the most recent files from NOAA FTP

# %%
# %load_ext watermark

# %%
# %watermark

# %% [markdown]
"""
# County Time Series: NOAA

Florida time series by county of:

- Average Temperature
- Maximum Temperature
- Minimum Temperature
- Precipation
"""

# %% [markdown]
"""
The documentation for the files hosted by NOAA can be found at
https://www1.ncdc.noaa.gov/pub/data/cirs/climdiv/county-readme.txt

The relevant information is as follows:
"""

# %% [markdown]
"""
## State Code Table:

Range of values of 01-48.

```
01 Alabama                 28 New Jersey
02 Arizona                 29 New Mexico
03 Arkansas                30 New York
04 California              31 North Carolina
05 Colorado                32 North Dakota
06 Connecticut             33 Ohio
07 Delaware                34 Oklahoma
08 Florida                 35 Oregon
09 Georgia                 36 Pennsylvania
10 Idaho                   37 Rhode Island
11 Illinois                38 South Carolina
12 Indiana                 39 South Dakota
13 Iowa                    40 Tennessee
14 Kansas                  41 Texas
15 Kentucky                42 Utah
16 Louisiana               43 Vermont
17 Maine                   44 Virginia
18 Maryland                45 Washington
19 Massachusetts           46 West Virginia
20 Michigan                47 Wisconsin
21 Minnesota               48 Wyoming
22 Mississippi
23 Missouri
24 Montana
25 Nebraska
26 Nevada
27 New Hampshire
```

## File Format:

**IMPORTANT NOTE:**

The format of the county data is slightly different than the other data files.
To accomadate the 2 digit state code and the 3 digit county FIPS code, the first
field contains 11 columns. The other data files still contain 10 columns.

```
╔═════════════════╦═════════════════╦════════════════════════════════════════════════╗
║ Element Name    ║ Record Position ║ Element Description                            ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ STATE-CODE      ║ 1-2             ║ STATE-CODE as indicated in State Code Table as ║
║                 ║                 ║ described in FILE 1. Range of values is 01-48. ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ DIVISION-NUMBER ║ 3-5             ║ COUNTY FIPS - Range of values 001-999.         ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ ELEMENT CODE    ║ 6-7             ║ 01 = Precipitation                             ║
║                 ║                 ║ 02 = Average Temperature                       ║
║                 ║                 ║ 27 = Maximum Temperature                       ║
║                 ║                 ║ 28 = Minimum Temperature                       ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ YEAR            ║ 8-11            ║ This is the year of record. Range is 1895 to   ║
║                 ║                 ║ current year processed.                        ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ *************** ║ *************** ║ ********************************************** ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ JAN-VALUE       ║ 12-18           ║                                                ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ FEB-VALUE       ║ 19-25           ║                                                ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ MAR-VALUE       ║ 26-32           ║                                                ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ APR-VALUE       ║ 33-39           ║                                                ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ MAY-VALUE       ║ 40-46           ║                                                ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ JUNE-VALUE      ║ 47-53           ║                                                ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ JULY-VALUE      ║ 54-60           ║                                                ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ AUG-VALUE       ║ 61-67           ║                                                ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ SEPT-VALUE      ║ 68-74           ║                                                ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ OCT-VALUE       ║ 75-81           ║                                                ║
╠═════════════��═══╬═════════════════╬════════════════════════════════════════════════╣
║ NOV-VALUE       ║ 82-88           ║                                                ║
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
║ DEC-VALUE       ║ 89-95           ║                                                ║
╚═════════════════╩═════════════════╩════════════════════════════════════════════════╝
```

> **Monthly Divisional Temperature format (f7.2)** Range of values -50.00 to
> 140.00 degrees Fahrenheit. Decimals retain a position in the 7-character
> field.  Missing values in the latest year are indicated by -99.99.

> **Monthly Divisional Precipitation format (f7.2)** Range of values 00.00 to
> 99.99.  Decimal point retains a position in the 7-character field. Missing
> values in the latest year are indicated by -9.99.
"""

# %%
LOCAL_FILES = sorted(os.listdir())

VALUES = ["precipitation", "max_temp", "min_temp", "avg_temp"]

KEYS = []

for file in LOCAL_FILES:
    if file.startswith("climdiv-pcpncy"):
        KEYS.insert(0, file)
    elif file.startswith("climdiv-tmaxcy"):
        KEYS.insert(1, file)
    elif file.startswith("climdiv-tmincy"):
        KEYS.insert(2, file)
    elif file.startswith("climdiv-tmpccy"):
        KEYS.insert(3, file)

VARIABLES = dict(zip(KEYS, VALUES))

# %%
FILENAME = KEYS[0]  # Precipitation
print(FILENAME)

with open(FILENAME, "r", encoding="utf-8") as file:
    DATA = file.read()

# 1. Find patterns matching 1st column with names
# 2. Separate using spaces.
# 3. Replace all spaces with commas.

FORMATREGEX = re.compile(
    r"(\d{2})(\d{3})(\d{2})(\d{4})(?:\s+)((?:-?\d+\.\d+\s+){11}-?\d+\.\d+)", re.VERBOSE
)

MATCHES = []

for groups in FORMATREGEX.findall(DATA):
    # print(groups)
    INFO = ",".join(groups[:4])
    MONTHS = ",".join(groups[4].split())
    final = f"{INFO},{MONTHS}"
    # print(final)

    MATCHES.append(final)

CSV_NAME = VARIABLES.get(FILENAME)
print(CSV_NAME)

with open(f"{CSV_NAME}.csv", "w", encoding="utf-8") as text_file:
    for i in MATCHES:
        print(i, sep="\n", file=text_file)

# %%
for FILENAME in KEYS[1:]:
    print(FILENAME)
    with open(FILENAME, "r", encoding="utf-8") as file:
        DATA = file.read()

    # 1. Find patterns matching 1st column with names
    # 2. Separate using spaces.
    # 3. Replace all spaces with commas.

    MATCHES = []

    for groups in FORMATREGEX.findall(DATA):
        # print(groups)
        INFO = ",".join(groups[:4])
        MONTHS = ",".join(groups[4].split())
        final = f"{INFO},{MONTHS}"
        MATCHES.append(final)

    CSV_NAME = VARIABLES.get(FILENAME)
    print(CSV_NAME)

    with open(f"{CSV_NAME}.csv", "w", encoding="utf-8") as text_file:
        for i in MATCHES:
            print(i, sep="\n", file=text_file)

# %%
COLUMNS = [
    "state",
    "fips_suffix",
    "variable",
    "year",
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
]


# %%
WEATHER = pd.concat(
    [
        pd.read_csv(variable, names=COLUMNS, na_values=["-9.99", "-99.9"])
        for variable in [
            "precipitation.csv",
            "max_temp.csv",
            "min_temp.csv",
            "avg_temp.csv",
        ]
    ]
)

# %%
FL = WEATHER.query("state == 8").reset_index(drop=True).copy()

# %%
FL

# %%
DF = pd.melt(
    FL,
    id_vars=COLUMNS[:4],
    value_vars=COLUMNS[4:],
    var_name="month",
    value_name="value",
)


# %%
def month() -> dict:
    """
    Parse abbreviated text month to its integer representation.

    e.g. "jan" -> 1
    """

    keys = COLUMNS[4:]
    values = list(range(1, len(keys) + 1))
    months = dict(zip(keys, values))

    # month = months.get(text)

    return months


# %%
# Map
DF["month"] = DF["month"].map(month())

# %%
DF["date"] = pd.to_datetime(DF[["year", "month"]].assign(day=1))

# %%
DF["fips"] = DF.fips_suffix + 12000

# %%
DF = (
    DF.drop(["state", "year", "month", "fips_suffix"], axis=1)
    .sort_values(by=["fips", "date"])
    .reset_index(drop=True)
)


# %%
def county_name() -> dict[int, str]:
    """
    Returns county name for FIPS code.
    """

    FLORIDA = pd.read_csv("data/florida_county_population.csv")
    keys = list(FLORIDA["FIPS"])
    values = list(FLORIDA["county"])
    counties = dict(zip(keys, values))

    return counties


# %%
DF["county"] = DF["fips"].map(county_name())


# %%
DF["element"] = DF["variable"].map(
    {1: "precipitation", 2: "avg_temp", 27: "max_temp", 28: "min_temp"}
)

# %%
DF = DF[["date", "fips", "county", "element", "value"]]

# %%
DF = DF.dropna()


# %%
def select_variable(df: pd.DataFrame, w_variable: str) -> pd.DataFrame:
    return (
        df.query("element == @w_variable")
        .reset_index(drop=True)
        .sort_values(by=["fips", "date"])
        .rename(columns={"value": w_variable})
        .drop(["element"], axis=1)
    )


# %%
PRECIPITATION, AVG_TEMP, MAX_TEMP, MIN_TEMP = (
    DF.pipe(select_variable, w)
    for w in ["precipitation", "avg_temp", "max_temp", "min_temp"]
)


# %%
def erase_large_files():
    for file in os.listdir():
        if os.path.getsize(file) > 3000000:
            os.remove(file)


erase_large_files()


# %%
def prepare_final_df(df: pd.DataFrame) -> pd.DataFrame:
    """"""
    # change = lambda df, variable, n: df[variable].diff(n)
    # rate_change = lambda df, variable, n: df[variable].pct_change(n)

    # df = (
    # df.assign(
    #     month_change=change(df, variable, 1),
    #     month_rate_change=rate_change(df, variable, 1),
    #     month_yoy_change=change(df, variable, 12),
    #     month_yoy_rate_change=rate_change(df, variable, 1),
    # )
    # df.query("date>=1960").set_index("date")
    # )

    # df.to_parquet(f"{variable}.parquet")
    # df = df.query("date>=1960").set_index("date")
    # df.index = df.index.to_period("M")
    # return df
    return df.set_index("date")


# %%
PRECIPITATION, AVG_TEMP, MAX_TEMP, MIN_TEMP = (
    df.pipe(prepare_final_df)
    for variable, df in dict(
        zip(
            ["precipitation", "avg_temp", "max_temp", "min_temp"],
            [PRECIPITATION, AVG_TEMP, MAX_TEMP, MIN_TEMP],
        )
    ).items()
)

# %%
TEMP = (
    pd.concat([AVG_TEMP, MIN_TEMP, MAX_TEMP], axis="columns", sort=True)
    .T.drop_duplicates()
    .T
)

# %%
TEMP.to_parquet("temp.parquet", compression="brotli")

# %%
PRECIPITATION.to_parquet("precipitation.parquet", compression="brotli")
