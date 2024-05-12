import re
import urllib
import requests
import urllib.parse

from bs4 import BeautifulSoup
from conf import TOKEN


def browser_parser(url):
    encoded_url = urllib.parse.quote(url)
    url = f"http://api.scrape.do?token={TOKEN}&url={encoded_url}"
    response = requests.request("GET", url)
    html_soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
    return html_soup


class CardParser:
    def __init__(self, url):
        self.url = url
        self.html_source = browser_parser(self.url)

    def get_title(self):
        divs_with_class = self.html_source.find_all('div', class_='style-titleWrapper-Hmr_5')
        for tag in divs_with_class:
            title = tag.find('h1').text
            return title

    def get_geo(self):
        address_span = self.html_source.find('span', class_='style-item-address__string-wt61A')
        if address_span:
            address = address_span.text.strip()
            return address
        return None

    def get_number(self):
        number_span = self.html_source.find('span', {'data-marker': 'item-view/item-id'})
        if number_span:
            number_text = number_span.text.strip()
            number = re.search(r'\d+', number_text).group()
            return number
        return None

    def get_views(self):
        today_views_span = self.html_source.find('span', {'data-marker': 'item-view/today-views'})
        if today_views_span:
            today_views_text = today_views_span.text.strip()
            today_views = re.search(r'\d+', today_views_text).group()
            return today_views
        return None

    def get_description(self):
        description_span = self.html_source.find('div', {'data-marker': 'item-view/item-description'})
        if description_span:
            description_text = description_span.get_text(strip=True)
            return description_text
        return None

    def get_description_html(self):
        description_span = self.html_source.find('div', {'data-marker': 'item-view/item-description'})
        if description_span:
            description_with_tags = description_span.decode_contents()
            return description_with_tags
        return None

    def get_photos(self):
        divs_photo = self.html_source.find_all('div', class_='image-frame-wrapper-_NvbY')
        if divs_photo:
            photo_urls = []
            for photo in divs_photo:
                photo_url = photo.get('data-url')
                if photo_url:
                    photo_urls.append(photo_url)
            return ''.join(photo_urls)
        return None

    def get_profile_link(self):
        div_tag = self.html_source.find('div', {'data-marker': 'seller-info/name'})
        if div_tag:
            a_tag = div_tag.find('a', {'data-marker': 'seller-link/link'})
            link = a_tag['href'] if a_tag and 'href' in a_tag.attrs else None
            if link:
                if link.startswith("https://www.avito.ru"):
                    return link
                else:
                    return "https://www.avito.ru" + link if link else None
        return None

    def get_product_link(self):
        number = self.get_number()
        return "https://www.avito.ru/" + number

    def get_rating(self):
        span_tag = self.html_source.find('span', {'class': 'style-seller-info-rating-score-C0y96'})
        if span_tag:
            rating = span_tag.text if span_tag else None
            return rating
        return None
