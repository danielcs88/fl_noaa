# -*- coding: utf-8 -*-
# %%
"""
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
╠═════════════════╬═════════════════╬════════════════════════════════════════════════╣
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
LOCAL_FILES = os.listdir()

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

with open(FILENAME, "r") as file:
    DATA = file.read()

"""
1. Find patterns matching 1st column with names
2. Separate using spaces.
3. Replace all spaces with commas.
"""

FORMATREGEX = re.compile(
    r"""(
        (\d{2})            # State code
        (\d{3})            # FIPS county code (last 3 digits)
        (\d{2})            # Variable
        (\d{4})            # Year
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # January
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # February
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # March
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # April
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # May
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # June
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # July
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # August
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # September
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # October
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # November
        (\s{2,3})           #    Space
        (-?\d{1,2}.\d{2})  # December
    )""",
    re.VERBOSE,
)

MATCHES = []

for groups in FORMATREGEX.findall(DATA):
    info = ",".join(groups[1:5])
    months = ",".join(groups[6::2])
    final = info + "," + months
    MATCHES.append(final)

CSV_NAME = VARIABLES.get(FILENAME)
print(CSV_NAME)

with open(f"{CSV_NAME}.csv", "w") as text_file:
    for i in MATCHES:
        print(i, sep="\n", file=text_file)

# %%
for FILENAME in KEYS[1:]:
    print(FILENAME)
    with open(FILENAME, "r") as file:
        DATA = file.read()

    """
    1. Find patterns matching 1st column with names
    2. Separate using spaces.
    3. Replace all spaces with commas.
    """

    FORMATREGEX = re.compile(
        r"""(
            (\d{2})            # State code
            (\d{3})            # FIPS county code (last 3 digits)
            (\d{2})            # Variable
            (\d{4})            # Year
            (\s{1,3})           # Space
            (-?\d{1,3}.\d{2})  # January
            (\s{1,3})           # Space
            (-?\d{1,3}.\d{2})  # February
            (\s{1,3})           # Space
            (-?\d{1,3}.\d{2})  # March
            (\s{1,3})            # Space
            (-?\d{1,3}.\d{2})  # April
            (\s{1,3})            # Space
            (-?\d{1,3}.\d{2})  # May
            (\s{1,3})            # Space
            (-?\d{1,3}.\d{2})  # June
            (\s{1,3})            # Space
            (-?\d{1,3}.\d{2})  # July
            (\s{1,3})            # Space
            (-?\d{1,3}.\d{2})  # August
            (\s{1,3})            # Space
            (-?\d{1,3}.\d{2})  # September
            (\s{1,3})            # Space
            (-?\d{1,3}.\d{2})  # October
            (\s{1,3})            # Space
            (-?\d{1,3}.\d{2})  # November
            (\s{1,3})            # Space
            (-?\d{1,3}.\d{2})  # December
        )""",
        re.VERBOSE,
    )

    MATCHES = []

    for groups in FORMATREGEX.findall(DATA):
        info = ",".join(groups[1:5])
        months = ",".join(groups[6::2])
        final = info + "," + months
        MATCHES.append(final)

    CSV_NAME = VARIABLES.get(FILENAME)
    print(CSV_NAME)

    with open(f"{CSV_NAME}.csv", "w") as text_file:
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
LOCAL_FILES = os.listdir()

# values = ["precipitation", "max_temp", "min_temp", "avg_temp"]

DATAFRAMES = []

for file in list(os.listdir()):
    for variable in VALUES:
        if file.startswith(variable):
            DATAFRAMES.append(file)

# %%
print(DATAFRAMES)

# %%
WEATHER = pd.DataFrame()

for variable in DATAFRAMES:
    print(variable)
    WEATHER = WEATHER.append(
        pd.read_csv(variable, names=COLUMNS, na_values=["-9.99", "-99.9"])
    )

# %%
FL = WEATHER.query("state == 8 and year >= 1959").reset_index(drop=True).copy()_

# %%
FL

# %%
FL.describe()

# %%
DF = pd.melt(
    FL,
    id_vars=COLUMNS[:4],
    value_vars=COLUMNS[4:],
    var_name="month",
    value_name="value",
)

# %%
def month(text):
    """
    Parse abbreviated text month to its integer representation.

    e.g. "jan" -> 1
    """

    keys = COLUMNS[4:]
    values = list(range(1, len(keys) + 1))
    months = dict(zip(keys, values))

    month = months.get(text)

    return month


# %%
DF["month"] = DF.apply(lambda x: month(x["month"]), axis=1)


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
FLORIDA = pd.read_csv("data/florida_county_population.csv")


# %%
def county_name(fips):
    """
    Returns county name for FIPS code.
    """

    keys = list(FLORIDA["FIPS"])
    values = list(FLORIDA.county)
    counties = dict(zip(keys, values))

    county = counties.get(fips)

    return county


# %%
DF["county"] = DF.apply(lambda x: county_name(x["fips"]), axis=1)


# %%
def variable_weather(variable):
    """
    Change variable integer to actual variable.

    i.e.,

    01 = Precipitation
    02 = Average Temperature
    27 = Maximum Temperature
    28 = Minimum Temperature
    """

    keys = [1, 2, 27, 28]
    values = ["precipitation", "avg_temp", "max_temp", "min_temp"]

    variables = dict(zip(keys, values))

    weather = variables.get(variable)

    return weather


# %%
DF["element"] = DF.apply(lambda x: variable_weather(x["variable"]), axis=1)

# %%
DF = DF[["date", "fips", "county", "element", "value"]]

# %%
# def negative_clean_up(value):
#     """
#     Converts all missing values to NaN (-9.99 and -99.90)
#     """

#     if value in (-9.99, -99.90):
#         value = float("NaN")

#     return value

# %%
# DF.value = DF.apply(lambda x: negative_clean_up(x["value"]), axis=1)

# %%
DF = DF.dropna()

# %%
DF.tail()

# %%
PRECIPITATION = (
    DF.query("element == 'precipitation'")
    .reset_index(drop=True)
    .sort_values(by=["fips", "date"])
    .rename(columns={"value": "precipitation"})
    .drop(["element"], axis=1)
)
AVG_TEMP = (
    DF.query("element == 'avg_temp'")
    .reset_index(drop=True)
    .sort_values(by=["fips", "date"])
    .rename(columns={"value": "avg_temp"})
    .drop(["element"], axis=1)
)
MAX_TEMP = (
    DF.query("element == 'max_temp'")
    .reset_index(drop=True)
    .sort_values(by=["fips", "date"])
    .rename(columns={"value": "max_temp"})
    .drop(["element"], axis=1)
)
MIN_TEMP = (
    DF.query("element == 'min_temp'")
    .reset_index(drop=True)
    .sort_values(by=["fips", "date"])
    .rename(columns={"value": "min_temp"})
    .drop(["element"], axis=1)
)

# %%
for file in os.listdir():
    if os.path.getsize(file) > 3000000:
        os.remove(file)

# %%
PRECIPITATION["month_change"] = (
    PRECIPITATION.groupby("county").diff().precipitation.round(2)
)
PRECIPITATION["month_rate_change"] = PRECIPITATION.groupby(
    "county"
).precipitation.pct_change()
PRECIPITATION["month_yoy_change"] = (
    PRECIPITATION.groupby("county").diff(12).precipitation.round(2)
)
PRECIPITATION["month_yoy_rate_change"] = PRECIPITATION.groupby(
    "county"
).precipitation.pct_change(12)

# %%
AVG_TEMP["month_change"] = AVG_TEMP.groupby("county").diff().avg_temp.round(2)
AVG_TEMP["month_rate_change"] = AVG_TEMP.groupby("county").avg_temp.pct_change()
AVG_TEMP["month_yoy_change"] = AVG_TEMP.groupby("county").diff(12).avg_temp.round(2)
AVG_TEMP["month_yoy_rate_change"] = AVG_TEMP.groupby("county").avg_temp.pct_change(12)

# %%
MAX_TEMP["month_change"] = MAX_TEMP.groupby("county").diff().max_temp.round(2)
MAX_TEMP["month_rate_change"] = MAX_TEMP.groupby("county").max_temp.pct_change()
MAX_TEMP["month_yoy_change"] = MAX_TEMP.groupby("county").diff(12).max_temp.round(2)
MAX_TEMP["month_yoy_rate_change"] = MAX_TEMP.groupby("county").max_temp.pct_change(12)

# %%
MIN_TEMP["month_change"] = MIN_TEMP.groupby("county").diff().min_temp.round(2)
MIN_TEMP["month_rate_change"] = MIN_TEMP.groupby("county").min_temp.pct_change()
MIN_TEMP["month_yoy_change"] = MIN_TEMP.groupby("county").diff(12).min_temp.round(2)
MIN_TEMP["month_yoy_rate_change"] = MIN_TEMP.groupby("county").min_temp.pct_change(12)

# %%
PRECIPITATION = PRECIPITATION.query("date >= 1960")
AVG_TEMP = AVG_TEMP.query("date >= 1960")
MAX_TEMP = MAX_TEMP.query("date >= 1960")
MIN_TEMP = MIN_TEMP.query("date >= 1960")

# %%
PRECIPITATION.to_csv("precipitation.csv", index=False)
AVG_TEMP.to_csv("avg_temp.csv", index=False)
MAX_TEMP.to_csv("max_temp.csv", index=False)
MIN_TEMP.to_csv("min_temp.csv", index=False)
