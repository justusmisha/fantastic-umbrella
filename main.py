import time

from card_parser import CardParser
from db_base import get_links_from_db
from excel_downloader import Downloader


def main(sheet=None, google_sheet=None, query_id=None, link=None):
    try:
        if link:
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
            range_start = f"{sheet}!A1:H1"
            downloader.export_to_google(google_sheet, range_start, "USER_ENTERED")
        else:
            links = get_links_from_db(query_id)
            for idx, link in enumerate(links, start=1):
                parser = CardParser(url=link[2])
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
                range_start = f"{sheet}!A{idx}:H{idx}"
                downloader.export_to_google(google_sheet, range_start, "USER_ENTERED")
                time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")
