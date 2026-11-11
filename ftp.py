# -*- coding: utf-8 -*-
# %%
r"""
Script to download latest values for weather variables from NOAA NCEI.

NOAA retired the anonymous FTP server (ftp.ncei.noaa.gov). The climdiv files
are now served over HTTPS from the directory below.
"""

# %
__author__ = "Daniel Cárdenas"
__version__ = "2.0"
__maintainer__ = "Daniel Cárdenas"
__email__ = "jcard151@fiu.edu"

# %% [markdown]
# # HTTPS Downloader for NOAA Climate County Data

# %%
import os
import re
import urllib.request

# %%
BASE_URL = (
    "https://www.ncei.noaa.gov/monitoring-content/data/us/climdiv/monthly/current/"
)
PREFIXES = ("climdiv-pcpncy", "climdiv-tmaxcy", "climdiv-tmincy", "climdiv-tmpccy")

# %%
# Delete existing raw NOAA weather files (the only files larger than 3 MB)
for file in os.listdir():
    if os.path.isfile(file) and os.path.getsize(file) > 3000000:
        os.remove(file)


# %%
def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "fl-noaa-updater"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


# %%
PROCDATE = fetch(BASE_URL + "procdate.txt").decode().strip()
print(f"NOAA processing date: {PROCDATE}")

# %%
LISTING = fetch(BASE_URL).decode()
FILE_LIST = sorted(set(re.findall(r'href="(climdiv-[^"/]+)"', LISTING)))
FINAL_LIST = [f for f in FILE_LIST if f.startswith(PREFIXES)]
print(FINAL_LIST)

if len(FINAL_LIST) != len(PREFIXES):
    raise RuntimeError(f"Expected {len(PREFIXES)} files, found: {FINAL_LIST}")

# %%
for filename in FINAL_LIST:
    print(filename)
    with open(filename, "wb") as f:
        f.write(fetch(BASE_URL + filename))
