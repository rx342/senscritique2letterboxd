import csv
import json
import requests
from typing import Any, Dict, List
from rich import print
from rich.table import Table
from rich.progress import Progress, track


def get_data_batch(username: str, offset: int = 0,
                   universe: str = 'movie', action: str = 'DONE') \
                    -> Dict[str, Any]:
    """
    Send POST request

    :username: Senscritique username
    :offset: Offset value
    :universe: 'movie' or 'tvShow'
    :action: 'DONE' or 'WISH'
    """

    if universe == 'movie':
        int_univ = 1
    elif universe == 'tvShow':
        int_univ = 4
    else:
        raise ValueError("`universe` is neither 'movie' nor 'tvShow'")

    if action not in ['DONE', 'WISH']:
        raise ValueError("`action` is neither 'DONE' nor 'WISH'")

    int_univ = 1 if universe == 'movie' else 4

    url = 'https://www.senscritique.com/%s/collection?universe=%d' % (
        username,
        int_univ)

    query = ('{\"query\":\"query UserCollection($action: ProductAction, '
             '$categoryId: Int, $gameSystemId: Int, $genreId: Int, $isAgenda: '
             'Boolean, $keywords: String, $limit: Int, $month: Int, $offset: '
             'Int, $order: CollectionSort, $showTvAgenda: Boolean, '
             '$universe: String, $username: String, '
             '$versus: Boolean, $year: Int, $yearDateDone: Int, '
             '$yearDateRelease: Int) { user(username: $username) { '
             '...UserMinimal ...ProfileStats notificationSettings '
             '{ alertAgenda __typename } collection( '
             'action: $action categoryId: $categoryId gameSystemId: '
             '$gameSystemId genreId: $genreId isAgenda: '
             '$isAgenda keywords: $keywords limit: $limit '
             'month: $month offset: $offset order: $order '
             'showTvAgenda: $showTvAgenda universe: $universe '
             'versus: $versus year: $year yearDateDone: '
             '$yearDateDone yearDateRelease: $yearDateRelease ) '
             '{ total filters { action { count label value __typename '
             '} category { count label value __typename } gamesystem { '
             'count label value __typename } genre { count label '
             'value __typename } monthDateDone { count label '
             'value __typename } releaseDate { count label value __typename '
             '} universe { count label value __typename } yearDateDone { '
             'count label value __typename } __typename } products { '
             '...ProductList episodeNumber seasonNumber '
             'totalEpisodes preloadedParentTvShow { '
             '...ProductList __typename } scoutsAverage '
             '{ average count __typename } '
             ' currentUserInfos { ...ProductUserInfos '
             '__typename } otherUserInfos(username: $username) '
             '{ ...ProductUserInfos lists { id label listSubtype url '
             '__typename } review { id title url __typename } '
             ' __typename } __typename } tvProducts { infos { channel { '
             'id label __typename } showTimes { id dateEnd '
             'dateStart __typename } __typename '
             '} product { ...ProductList __typename '
             '} __typename } __typename } __typename }}'
             'fragment UserMinimal on User { ...UserNano settings { '
             'about birthDate country dateLastSession '
             'displayedName email firstName gender lastName '
             'privacyName privacyProfile showAge showProfileType '
             'urlWebsite username zipCode __typename } __typename}'
             'fragment UserNano on User { following id isBlocked isScout '
             'name url username medias { avatar __typename } '
             '__typename}fragment ProductList on Product { category channel '
             'dateRelease dateReleaseEarlyAccess dateReleaseJP '
             'dateReleaseOriginal dateReleaseUS displayedYear duration '
             'frenchReleaseDate id numberOfSeasons originalRun '
             'originalTitle rating slug subtitle title universe url '
             'yearOfProduction tvChannel { name url __typename } '
             'countries { id name __typename } gameSystems { '
             'id label __typename } medias { picture __typename '
             '} genresInfos { label __typename } artists { name '
             'person_id url __typename } authors { name '
             'person_id url __typename } creators { name '
             'person_id url __typename } developers { name '
             'person_id url __typename } directors { name '
             'person_id url __typename } pencillers { name '
             'person_id url __typename } __typename}fragment '
             'ProductUserInfos on ProductUserInfos { dateDone '
             'hasStartedReview isCurrent id isDone isListed isRecommended '
             'isRejected isReviewed isWished productId rating userId '
             'numberEpisodeDone lastEpisodeDone { episodeNumber id '
             'season { seasonNumber id episodes { '
             'title id episodeNumber __typename } '
             ' __typename } __typename } gameSystem { id label '
             '__typename } review { url __typename } __typename}'
             'fragment ProfileStats on User { likePositiveCountStats { '
             'contact feed list paramIndex review total '
             '__typename } stats { collectionCount diaryCount '
             'listCount followerCount ratingCount reviewCount '
             'scoutCount __typename } __typename}\"')
    query += (', \"variables\":{'
              f'\"action\": \"{action}\", '
              f'\"offset\": {offset}, '
              f'\"universe\": \"{universe}\", '
              f'\"username\": \"{username}\"'
              '}}')

    x = requests.post(
        url,
        data=query,
        headers={
            'Host': 'apollo.senscritique.com',
            'Content-Type': 'application/json',
            'Referer': url,
            'Accept': 'application/json'})

    d = json.loads(x.text)
    if d['data']['user'] is None:
        raise ValueError(f'Member named `{username}` does not exist')

    collection = d['data']['user']['collection']

    if collection['total'] == 0:
        return {'num_total': 0, 'collection': []}

    items = []
    for x in collection['products']:
        item = {
            'Title': x['originalTitle'] if x['originalTitle'] else x['title'],
            'Year': str(x['yearOfProduction']),
            'Rating10': str(x['otherUserInfos']['rating']),
        }

        if action == 'DONE':
            date = str(x['otherUserInfos']['dateDone']).split('T')[0]
            item.update({'WatchedDate': date})

        items.append(item)

    results = {
        'num_total': collection['total'],
        'collection': items,
    }

    return results


def get_data(username: str, universe: str = 'movie', action: str = 'DONE') \
        -> List[Dict[str, Any]]:
    """
    Send POST request

    :username: Senscritique username
    :universe: 'movie' or 'tvShow'
    :action: 'DONE' or 'WISH'
    """

    results = []
    offset = 0
    data = get_data_batch(username, offset, universe, action)
    num_total = data['num_total']
    len_data = len(data['collection'])
    results += data['collection']
    offset += len_data

    str_el = 'films' if universe == 'movie' else 'TV shows'

    with Progress() as progress:
        task = progress.add_task(
            f'Collecting [bold violet]{str_el}[/bold violet]',
            total=num_total)
        while offset < num_total:
            data = get_data_batch(username, offset, universe, action)
            len_data = len(data['collection'])
            results += data['collection']
            offset += len_data
            progress.update(task, advance=len_data)

    return results


def write_csv(path: str, data: List[Dict[str, str]], limit: int = 1900):
    """
    Write the CSV.

    :path: Output path
    :data: List of dictionaries containing the data
    :limit: Letterboxd has a limit of 1900 movies.
    """

    if len(data) > 0:
        labels = data[0].keys()
        num_elements = len(data)
        parts = num_elements//limit

        for i in track(range(1, parts+2), 'Writing CSV parts'):
            if parts == 0:
                output_path = path
            else:
                output_path = path.replace('.csv', f'_{i}.csv')

            with open(output_path, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=labels)
                writer.writeheader()

                for elem in data[(i-1)*limit:i*limit]:
                    writer.writerow(elem)


def pretty_table(data: List[Dict[str, str]], num_elements: int = 5,
                 action: str = 'DONE'):
    """
    Pretty print table with `rich`

    :data: List of dictionaries containing the data
    :num_elements: Number of elements to print
    :action: 'DONE' or 'WISH'
    """

    if action not in ['DONE', 'WISH']:
        raise ValueError("`action` is neither 'DONE' nor 'WISH'")

    table = Table(title=f'{num_elements} last elements', show_header=True)
    table.add_column("Title")
    table.add_column("Date")
    table.add_column("Rating")

    if action == 'DONE':
        table.add_column("Watched")

    for x in data[:num_elements]:
        if action == 'DONE':
            table.add_row(
                x['Title'], x['Year'], x['Rating10'], x['WatchedDate'])
        else:
            table.add_row(x['Title'], x['Year'], x['Rating10'])

    print(table)


if __name__ == '__main__':
    import argparse

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
    parser.add_argument(
        '--watchlist_only',
        default=False,
        action='store_true',
        help='Extract only watchlist items')
    p_args = parser.parse_args()

    item_action = 'WISH' if p_args.watchlist_only else 'DONE'
    universes = ['movie', 'tvShow'] if p_args.add_tv else ['movie']
    results = []

    for universe in universes:
        results += get_data(p_args.username, universe, item_action)

    if len(results) > 0:
        print(f'[bold green]Done:[/bold green] found {len(results)} elements!')
        pretty_table(results, 5, item_action)
        write_csv(p_args.output, results)
    else:
        print(f'[bold red]Done:[/bold red] found {len(results)} element :(')
