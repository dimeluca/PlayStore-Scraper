# Simple PlayStore scraper.

import lxml
import requests
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable

base_url = "https://play.google.com/store/apps/details?id="
not_available = "Not Available"


def collect_info(app_package):
    req = requests.get(base_url + app_package + "&hl=en&gl=US")
    cont = bs(req.text, "lxml")
    scrape_info(cont)


def scrape_info(content):
    # Application Name
    app_name = content.find("h1", itemprop="name").find_next("span").text

    # Last App Update
    if content.find("div", text="Updated"):
        last_update = content.find("div", text="Updated").find_next("span").text
    else:
        last_update = not_available

    # App Size
    if content.find("div", text="Size"):
        size = content.find("div", text="Size").find_next("span").text
    else:
        size = not_available

    # Downloads Number
    if content.find("div", text="Installs"):
        installs = content.find("div", text="Installs").find_next("span").text
    else:
        installs = not_available

    # Current Version Number
    if content.find("div", text="Current Version"):
        current_version = content.find("div", text="Current Version").find_next("span").text
    else:
        current_version = not_available

    # Minimum Android Version Required
    if content.find("div", text="Requires Android"):
        requires_version = content.find("div", text="Requires Android").find_next("span").text
    else:
        requires_version = not_available

    # Content Rating
    if content.find("div", text="Content Rating"):
        content_rating = content.find("div", text="Content Rating").find_next("span").text
        if "Learn more" in content_rating:
            content_rating = content_rating.replace("Learn more", "")
    else:
        content_rating = not_available

    # Interactive Elements
    if content.find("div", text="Interactive Elements"):
        interactive_elements = content.find("div", text="Interactive Elements").find_next("span").text
    else:
        interactive_elements = not_available

    # Offered By
    if content.find("div", text="Offered By"):
        offered_by = content.find("div", text="Offered By").find_next("span").text
    else:
        offered_by = not_available

    # Developer
    if content.find("div", text="Developer"):
        dev = content.find("div", text="Developer").find_next("div").text
        if "Visit website" in dev:
            dev = dev.replace("Visit website", "")
        if "Privacy Policy" in dev:
            dev = dev.replace("Privacy Policy", "")
    else:
        dev = not_available

    print_table(app_name, last_update, size, installs, current_version, requires_version, content_rating,
                interactive_elements, offered_by, dev)


def print_table(app_name, last_update, size, installs, current_version, requires_version, content_rating,
                interactive_elements, offered_by, dev):
    table = PrettyTable()
    table.title = app_name
    table.field_names = ['Info', 'Value']
    table.add_row(["Last Update", last_update])
    table.add_row(["Size", size])
    table.add_row(["Downloads", installs])
    table.add_row(["Current Version", current_version])
    table.add_row(["Requires Android", requires_version])
    table.add_row(["Content Rating", content_rating])
    table.add_row(["Interactive Elements", interactive_elements])
    table.add_row(["Offered By", offered_by])
    table.add_row(["Developer", dev])
    print(table)


if __name__ == '__main__':
    app = input('Insert a package name (EX: com.lemon.lvoverseas): ')
    collect_info(app)
