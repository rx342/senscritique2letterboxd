import urllib
import xmltodict
import xml.etree.ElementTree as ET
from lxml import etree
from typing import Dict, List
from rich.progress import track


USER_URL = "https://www.senscritique.com/%s"


def is_valid_profile(username: str) -> bool:
    """
    Check if `username` is valid.

    If it is not, SensCritique usually returns to homepage.

    :username: Your username
    """

    with urllib.request.urlopen(USER_URL % p_args.username) as f:
        data = f.read()
        parser = etree.XMLParser(recover=True)
        root = ET.fromstring(data, parser=parser)
        title = root.find('head/title').text

    correct_title = 'Profil culturel et avis de'
    return correct_title in title


def is_private_profile(username: str) -> bool:
    """
    Check if `username` is a private profile.

    :username: Your username
    """

    restart = True
    while restart:
        with urllib.request.urlopen(USER_URL % p_args.username) as f:
            data = f.read()
            parser = etree.XMLParser(recover=True)
            root = ET.fromstring(data, parser=parser)

        no_cover = len(root.findall('.//*[@class="uco-cover no-cover"]')) == 0
        cover = len(root.findall('.//*[@class="uco-cover "]')) == 0
        restart = no_cover and cover

    field = root.findall('.//*[@class="uvi-numbers-item"]')
    return len(field) == 0


def get_number_of_pages(username: str, collection: str = 'film') -> List[
        Dict[str, str]]:
    """
    Return the number of pages in the `collection`.

    :username: Your username
    :collection: 'film' or 'tv'
    """

    if collection == 'film':
        action = 'done'
        choice = 'films'
    else:
        action = 'rating'
        choice = 'series'

    url = (USER_URL % username
           + '/collection/%s' % action
           + '/%s/all/all/all/all/all/all/list' % choice
           + '/page-1')

    restart = True
    while restart:
        with urllib.request.urlopen(url) as f:
            data = f.read()
            parser = etree.XMLParser(recover=True)
            root = ET.fromstring(data, parser=parser)

            elements = root.findall('.//*[@class="eipa-page"]/a')

        restart = (len(elements) == 0)

    page = root.findall('.//*[@class="eipa-page"]/a')[-1].text
    if '.' in page:
        page = page.replace('.', '')

    return int(page)


def get_ratings_from_page(username: str, page_id: int,
                          collection: str = 'film'):
    """
    Return movie ratings from a given `page_id`-th page for `username`.

    :username: Your username
    :page_id: Specific page
    :collection: 'film' or 'tv'
    """

    if collection == 'film':
        action = 'done'
        choice = 'films'
    else:
        action = 'rating'
        choice = 'series'

    url = (USER_URL % username
           + '/collection/%s' % action
           + '/%s/all/all/all/all/all/all/list' % choice
           + '/page-%d' % page_id)

    restart = True
    while restart:
        with urllib.request.urlopen(url) as f:
            data = f.read()
            parser = etree.XMLParser(recover=True)
            root = ET.fromstring(data, parser=parser)

            elements = root.findall('.//*[@class="elco-collection-item"]')

        restart = (len(elements) == 0)

    notes = root.findall('.//*[@class="elrua-useraction-action "]')

    titles, years = [], []
    for elem in root.findall('.//*[@class="elco-product-detail"]'):
        original_title = elem.find('*[@class="elco-original-title"]')
        french_title = elem.find('*[@class="d-heading2 elco-title"]/a')

        if original_title is not None:
            titles.append(original_title)
        else:
            titles.append(french_title)

        year = elem.find('*[@class="d-heading2 elco-title"]*[@class='
                         '"elco-date"]')

        if year is not None:
            years.append(year)
        else:
            years.append(None)

    results = []
    for n, t, y in zip(notes, titles, years):
        _n = n.find('span').text.lstrip().rstrip()
        note = None if _n == '' else int(_n)

        if y is not None:
            year = y.text.replace('(', '').replace(')', '')
        else:
            year = y

        title = t.text

        results.append({'Title': title, 'Year': year, 'Rating10': note})

    return results


def write_csv(path: str, data: List[Dict[str, str]], limit: int = 1900):
    """
    Write the CSV.

    :path: Output path
    :data: List of dictionaries containing the data
    :limit: Letterboxd has a limit of 1900 movies.
    """

    import csv

    labels = data[0].keys()
    num_elements = len(data)
    parts = num_elements//limit

    for i in track(range(1, parts+2), 'Writing CSV parts...'):
        if parts == 0:
            output_path = path
        else:
            output_path = path.replace('.csv', '_%d.csv' % i)

        with open(output_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=labels)
            writer.writeheader()

            for elem in data[(i-1)*limit:i*limit]:
                writer.writerow(elem)


if __name__ == '__main__':
    import argparse
    from rich import print

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--username',
        type=str,
        required=True,
        default=None,
        help='Your username')
    parser.add_argument(
        '--add_tv',
        default=False,
        action='store_true',
        help='Add TV shows')
    parser.add_argument(
        '--output',
        type=str,
        required=False,
        default='output.csv',
        help='Output CSV path')
    p_args = parser.parse_args()

    print('Checking your username ([bold violet]%s[/bold violet])...'
          % p_args.username)

    if not is_valid_profile(p_args.username):
        raise ValueError('The username is not valid')
    if is_private_profile(p_args.username):
        raise ValueError('The account is private')

    if p_args.add_tv:
        collections = ['film', 'tv']
        collection_names = ['films', 'TV shows']
    else:
        collections = ['film']
        collection_names = ['films']

    results = []
    for collection, collection_name in zip(collections, collection_names):
        print('Parsing your %s collection...' % collection_name)
        num_pages = get_number_of_pages(
            p_args.username, collection=collection)
        print('Number of pages to parse: %d' % num_pages)

        result = []
        for page_id in track(range(1, num_pages+1), 'Parsing pages...'):
            result += get_ratings_from_page(
                p_args.username, page_id, collection=collection)

        print('Number of %s: %d' % (collection_name, len(result)))
        results += result[::-1]

    write_csv(p_args.output, results)
    print('[bold green]Done![/bold green]')
