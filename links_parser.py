import urllib.parse
import requests

from bs4 import BeautifulSoup

from db_base import save_links_db, get_links_from_db


def parse_links_by_query(token, query_str, query_id, page_numbers, city=None):
    if city:
        for page_number in range(page_numbers, 0, -1):
            query = query_str.split(' ')
            targetUrl = f"https://www.avito.ru/{city}?q={'+'.join(query)}&p={page_number}"
            encoded_url = urllib.parse.quote(targetUrl)
            url = f"http://api.scrape.do?token={token}&url={encoded_url}"
            response = requests.get(url)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            divs_with_class = html_soup.find('div', class_='items-items-kAJAg')
            divs_with_class = divs_with_class.find_all('div', class_='iva-item-root-_lk9K')

            if not divs_with_class:
                break

            for tag in divs_with_class:
                links_from_db = get_links_from_db(query_id)
                href_link = tag.find('a', class_='iva-item-sliderLink-uLz1v')
                if href_link:
                    url = href_link.get("href")
                    parts = url.split('/')
                    new_url = '/' + '/'.join(parts[2:])
                    final_link = f'https://www.avito.ru/{city}{new_url}'
                    if final_link not in links_from_db:
                        save_links_db(final_link, query_id)

    else:
        for page in range(page_numbers, 0, -1):
            unique_links = set()
            targetUrl = query_str + f'&p={page}'
            encoded_url = urllib.parse.quote(targetUrl)
            url = f"http://api.scrape.do?token={token}&url={encoded_url}"
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Failed to fetch page {page}. Status code: {response.status_code}")
                continue

            html = BeautifulSoup(response.text, 'html.parser')
            items = 12
            for item in range(items):
                divs = html.find_all('div',
                                     {'data-marker': f'item_list_with_filters/item({item})',
                                      'itemscope': '',
                                      'itemtype': 'http://schema.org/Product'})
                if not divs:
                    break

                for div in divs:
                    a_tags = div.find_all('a', itemprop='url')
                    for a_tag in a_tags:
                        href = a_tag.get('href')
                        if href not in unique_links:
                            unique_links.add(href)
                            if href.startswith("https://www.avito.ru"):
                                save_links_db(query_id=query_id, url=href)
                            else:
                                save_links_db(query_id=query_id, url="https://www.avito.ru" + href)


def get_name_profile(html_source):
    names = html_source.find_all('div', class_='AvatarNameView-name-UrFI_')
    for name in names:
        h1_name = name.find('h1').text.strip()
        return h1_name
    return None
