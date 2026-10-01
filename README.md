# tapas-reading-list-exporter
This is a simple script to export information on your subscriptions ("Reading List") from [Tapas](https://tapas.io/). I created this since the site is shutting down and before long you won't be able to read anything on that website anymore. My hope is that this will help people track down new places to read all the comics and novels they've been keeping up with, wherever their new homes are.

This script intentionally runs very slowly to avoid causing too much load on Tapas's servers, so that nobody gets their IP banned.

# Requirements
1. Python 3.x and PIP
2. BeautifulSoup 4
3. pycurl

# How to use
1. Install Python 3.x (this should automatically install the `pip` package manager, which you need)
2. `pip install BeautifulSoup4`
3. `pip install pycurl`
4. `python tapas-reading-list-exporter.py <your tapas username>`
5. Wait a long time (there will be feedback while it works)
6. Open the generated subscriptions.csv and creators.csv files.

# Notes
* By default, the script will only fetch up to 20 pages of subscriptions. If you have more subscriptions than that, you can increase the limit by passing a number on the command line after your username, like `python tapas-reading-list-exporter.py <your tapas username> 40`
* If a creator has more than 3 links on their tapas profile page only the first three will be exported.
* Many creators don't have custom profiles on Tapas, so their rows in creators.csv will be mostly empty. That's normal.
* You can open the generated csv files with [Excel](https://excel.cloud.microsoft/en-us/) or [Google Sheets](https://docs.google.com/spreadsheets/u/0/).

# Reporting issues
You can file an issue on GitHub here or email me. When reporting an issue, please include your tapas user id and make sure it's correct. If your tapas user id is correct it will pull up a dedicated page on tapas, like mine - `antumbral` - does at [`https://tapas.io/antumbral`](https://tapas.io/antumbral).