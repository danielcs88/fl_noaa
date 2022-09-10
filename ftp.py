# -*- coding: utf-8 -*-
# %%
r"""
Script to download latest values for weather variables from NOAA FTP Server
"""

# %
__author__ = "Daniel Cárdenas"
__version__ = "1.0"
__maintainer__ = "Daniel Cárdenas"
__email__ = "jcard151@fiu.edu"

# %% [markdown]
# # FTP Downloader for NOAA Climate County Data

# %%
import ftplib
import os
from datetime import datetime

# %%
# Delete existing *.csv files or NOAA weather files

for file in os.listdir():
    if os.path.getsize(file) > 3000000:
        os.remove(file)


# %%
# some utility functions that we gonna need
def get_size_format(n, suffix="B"):
    """
    Converts bytes to scaled format (e.g KB, MB, etc.)
    """

    for unit in ["", "K", "M", "G", "T", "P"]:
        if n < 1024:
            return f"{n:.2f}{unit}{suffix}"
        n /= 1024


def get_datetime_format(date_time):
    """
    Returns formatted date/time.
    """

    # convert to datetime object
    date_time = datetime.strptime(date_time, "%Y%m%d%H%M%S")
    # convert to human readable date time string
    return date_time.strftime("%Y/%m/%d %H:%M:%S")


# %%
# initialize FTP session

# FTP_USER = "anonymous"
# FTP_PASS = ""

try:
    FTP_HOST = r"ftp.ncdc.noaa.gov"
    #     FTP = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    FTP = ftplib.FTP(FTP_HOST)
    FTP.login()

except EOFError:
    FTP_HOST = r"ftp.ncei.noaa.gov"
    #     FTP = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    FTP = ftplib.FTP(FTP_HOST)
    FTP.login()

# %%
# force UTF-8 encoding
FTP.encoding = "utf-8"

# %%
# print the welcome message
print(FTP.getwelcome())

# %%
FTP.cwd("pub/data/cirs/climdiv")

# %%
FILE_LIST = FTP.nlst()

# %%
FINAL_LIST = []

for file in FILE_LIST:
    if file.startswith("climdiv-pcpncy"):
        FINAL_LIST.append(file)
    elif file.startswith("climdiv-tmaxcy"):
        FINAL_LIST.append(file)
    elif file.startswith("climdiv-tmincy"):
        FINAL_LIST.append(file)
    elif file.startswith("climdiv-tmpccy"):
        FINAL_LIST.append(file)

# %%
print(FINAL_LIST)

# %%
for filename in FINAL_LIST:
    print(filename)

    with open(filename, "wb") as f:
        FTP.retrbinary("RETR " + filename, f.write)

FTP.close()

# %%
# quit and close the connection
