import time

from card_parser import CardParser
from db_base import get_links_from_db
from excel_downloader import Downloader


def main(sheet=None, google_sheet=None, query_id=None, link=None):
    try:
        if link:
            process_link(sheet, google_sheet, link)
        else:
            links = get_links_from_db(query_id)
            for idx, link in enumerate(links, start=1):
                process_link(sheet, google_sheet, link[2], idx)
                time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")


def process_link(sheet, google_sheet, link, idx=None):
    try:
        parser = CardParser(url=link)
        profile_link = parser.get_profile_link()
        downloader = Downloader(
            title=parser.get_title(),
            geo=parser.get_geo(),
            number=parser.get_number(),
            views=parser.get_views(),
            description=parser.get_description(),
            description_html=parser.get_description_html(),
            photos=parser.get_photos(),
            profile_link=profile_link,
            product_link=parser.get_product_link(),
            rating=parser.get_rating()
        )
        range_start = f"{sheet}!A{idx}:H{idx}" if idx else f"{sheet}!A1:H1"
        downloader.export_to_google(google_sheet, range_start, "USER_ENTERED")
    except Exception as e:
        print(f"Failed to process link {link}: {e}")

# Ensure you have appropriate memory management and logging
