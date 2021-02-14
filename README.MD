# Florida County Time Series: NOAA

![NOAA Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/NOAA_logo.svg/240px-NOAA_logo.svg.png)

## Run

Simply run in Terminal:

```sh
python fl_noaa_time_series.py
```

For more nuanced information on how the files are downloaded from the NOAA FTP site check

- `ftp.py`

## Information

Florida time series by county of:

- Average Temperature
- Maximum Temperature
- Minimum Temperature
- Precipitation

The documentation for the files hosted by NOAA can be found at
[https://www1.ncdc.noaa.gov/pub/data/cirs/climdiv/county-readme.txt](https://www1.ncdc.noaa.gov/pub/data/cirs/climdiv/county-readme.txt)

The relevant information is as follows:

### State Code Table

Range of values of 01-48.

```text
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

### File Format

**IMPORTANT NOTE:**

The format of the county data is slightly different than the other data files.
To accommodate the 2 digit state code and the 3 digit county FIPS code, the first
field contains 11 columns. The other data files still contain 10 columns.

```text
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
> field. Missing values in the latest year are indicated by -99.99.
>
> **Monthly Divisional Precipitation format (f7.2)** Range of values 00.00 to
> 99.99. Decimal point retains a position in the 7-character field. Missing
> values in the latest year are indicated by -9.99.
