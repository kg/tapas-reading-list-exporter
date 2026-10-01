from bs4 import BeautifulSoup
from pycurl import Curl
import sys
import re
import csv
from io import BytesIO
from zipfile import ZipFile
from time import sleep

abort_after_write = False

username = sys.argv[1]
if not username:
    raise Exception("No username specified")

page_limit = 20
if (len(sys.argv) > 2):
    page_limit = int(sys.argv[2])

series_urls = []
subscription_rows = [["author", "title", "series_id", "series_url"]]
sys.stdout.write(f"fetching up to {page_limit} pages of subscriptions for {username}")
sys.stdout.flush()

try:
    for page_index in range(page_limit):
        page_url = f"https://tapas.io/{username}/reading-list?pageNumber={page_index + 1}"

        resp_buffer = BytesIO()
        curl = Curl()
        curl.setopt(curl.URL, page_url)
        curl.setopt(curl.WRITEDATA, resp_buffer)
        curl.perform()
        curl.close()

        page_html = resp_buffer.getvalue().decode('utf8')
        soup = BeautifulSoup(page_html, 'html.parser')
        list_container = soup.find("ul", {"class": "content-list-wrap"})

        # Exit loop on page without list
        if not list_container:
            break

        list_items = list_container.find_all("a", {"class": "thumb-wrap"})
        for list_item in list_items:
            series_url = f"https://tapas.io{list_item["href"]}/info"
            series_urls.append(series_url)
            subscription_rows.append([
                list_item["data-tiara-page-meta-id"], 
                list_item["data-tiara-event-meta-series"],
                list_item["data-series-id"],
                series_url
            ])

        # Exit loop on empty page
        if len(list_items) == 0:
            break

        sys.stdout.write(".")
        sys.stdout.flush()

        sleep(5)
except KeyboardInterrupt:
    print("interrupted")
    abort_after_write = True

with open("subscriptions.csv", "w", newline="") as result_file:
    csv_writer = csv.writer(result_file)
    csv_writer.writerows(subscription_rows)

if abort_after_write:
    exit()

author_urls_to_fetch = set()
sys.stdout.write(f"\nOkay! Now fetching full creator list for each series, {len(series_urls)} in total")
sys.stdout.flush()

try:
    for series_url in series_urls:
        resp_buffer = BytesIO()
        curl = Curl()
        curl.setopt(curl.URL, series_url)
        curl.setopt(curl.WRITEDATA, resp_buffer)
        curl.perform()
        curl.close()

        page_html = resp_buffer.getvalue().decode('utf8')
        soup = BeautifulSoup(page_html, 'html.parser')
        creator_container = soup.find("ul", {"class": "creator-section"})
        if not creator_container:
            continue

        creator_links = creator_container.find_all("a", {"class": "name"})
        for creator_link in creator_links:
            creator_url = f"https://tapas.io{creator_link["href"]}"
            author_urls_to_fetch.add(creator_url)

        sys.stdout.write(".")
        sys.stdout.flush()

        sleep(3)
except KeyboardInterrupt:
    print("interrupted")

sys.stdout.write(f"\nFound {len(author_urls_to_fetch)} unique creators in total. Fetching their info")
sys.stdout.flush()

author_rows = [["creator_name", "creator_website", "creator_description", "creator_tapas_url"]]
try:
    for author_url in author_urls_to_fetch:
        resp_buffer = BytesIO()
        curl = Curl()
        curl.setopt(curl.URL, author_url)
        curl.setopt(curl.WRITEDATA, resp_buffer)
        curl.perform()
        curl.close()

        page_html = resp_buffer.getvalue().decode('utf8')
        soup = BeautifulSoup(page_html, 'html.parser')

        creator_name = soup.find("p", {"class": "author"}).string

        creator_description = soup.find("p", {"class": "js-creator-description"})
        if creator_description:
            creator_description_text = creator_description.string
        else:
            creator_description_text = ""

        creator_link = soup.find("a", {"class": "site-name"})
        if creator_link:
            creator_website_url = creator_link["href"]
        else:
            creator_website_url = ""

        author_rows.append([creator_name, creator_website_url, creator_description_text, author_url])

        sys.stdout.write(".")
        sys.stdout.flush()

        sleep(3)
except KeyboardInterrupt:
    print("interrupted")

with open("creators.csv", "w", newline="") as result_file:
    csv_writer = csv.writer(result_file)
    csv_writer.writerows(author_rows)

print()
print("Done! I created subscriptions.csv and creators.csv containing everything I fetched.")