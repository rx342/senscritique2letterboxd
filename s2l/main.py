#!/usr/bin/env python3

import csv
import json
from typing import Any, Dict, List

import requests
from rich import print
from rich.progress import Progress, track
from rich.table import Table


def get_review(review_url: str, user_agent: str) -> str:
    """
    Return the HTML review

    :review_url: The review URL
    :user_agent: User agent
    """

    from urllib.request import Request, urlopen

    from bs4 import BeautifulSoup, Tag

    result = ""

    url = f"https://www.senscritique.com{review_url}"
    request = Request(url=url, headers={"User-Agent": user_agent})

    with urlopen(request) as f:
        data = f.read()
        soup = BeautifulSoup(data, "html.parser")

    title = soup.find("h1", attrs={"data-testid": "review-title"})
    if title is not None:
        title = title.get_text()
        result = f"<b>{title}</b>"

    review = soup.find("div", attrs={"data-testid": "review-content"})
    if review is not None and isinstance(review, Tag):
        for elem in review.find_all("br"):
            elem.replace_with("\n\n" + elem.text)

        for elem in review.find_all("strong"):
            new_tag = soup.new_tag("b")
            new_tag.string = elem.get_text()
            elem.replace_with(new_tag)

        for elem in review.find_all("a", href=True):
            del elem["rel"], elem["target"]

        review = "".join(map(str, review.contents))
        result += "\n\n" + str(review)

    return result


def get_data_batch(
    username: str,
    user_agent: str,
    offset: int = 0,
    add_review: bool = False,
    universe: str = "movie",
    action: str = "DONE",
) -> Dict[str, Any]:
    """
    Send POST request

    :username: Senscritique username
    :user_agent: User agent
    :offset: Offset value
    :add_review: Add review
    :universe: 'movie' or 'tvShow'
    :action: 'DONE' or 'WISH'
    """

    if universe == "movie":
        int_univ = 1
    elif universe == "tvShow":
        int_univ = 4
    else:
        raise ValueError("`universe` is neither 'movie' nor 'tvShow'")

    if action not in ["DONE", "WISH"]:
        raise ValueError("`action` is neither 'DONE' nor 'WISH'")

    int_univ = 1 if universe == "movie" else 4

    url = "https://www.senscritique.com/%s/collection?universe=%d" % (
        username,
        int_univ,
    )

    query = (
        '{"query":"query UserCollection($action: ProductAction, '
        "$categoryId: Int, $gameSystemId: Int, $genreId: Int, $isAgenda: "
        "Boolean, $keywords: String, $limit: Int, $month: Int, $offset: "
        "Int, $order: CollectionSort, $showTvAgenda: Boolean, "
        "$universe: String, $username: String, "
        "$versus: Boolean, $year: Int, $yearDateDone: Int, "
        "$yearDateRelease: Int) { user(username: $username) { "
        "...UserMinimal ...ProfileStats notificationSettings "
        "{ alertAgenda __typename } collection( "
        "action: $action categoryId: $categoryId gameSystemId: "
        "$gameSystemId genreId: $genreId isAgenda: "
        "$isAgenda keywords: $keywords limit: $limit "
        "month: $month offset: $offset order: $order "
        "showTvAgenda: $showTvAgenda universe: $universe "
        "versus: $versus year: $year yearDateDone: "
        "$yearDateDone yearDateRelease: $yearDateRelease ) "
        "{ total filters { action { count label value __typename "
        "} category { count label value __typename } gamesystem { "
        "count label value __typename } genre { count label "
        "value __typename } monthDateDone { count label "
        "value __typename } releaseDate { count label value __typename "
        "} universe { count label value __typename } yearDateDone { "
        "count label value __typename } __typename } products { "
        "...ProductList episodeNumber seasonNumber "
        "totalEpisodes preloadedParentTvShow { "
        "...ProductList __typename } scoutsAverage "
        "{ average count __typename } "
        " currentUserInfos { ...ProductUserInfos "
        "__typename } otherUserInfos(username: $username) "
        "{ ...ProductUserInfos lists { id label listSubtype url "
        "__typename } review { id title url __typename } "
        " __typename } __typename } tvProducts { infos { channel { "
        "id label __typename } showTimes { id dateEnd "
        "dateStart __typename } __typename "
        "} product { ...ProductList __typename "
        "} __typename } __typename } __typename }}"
        "fragment UserMinimal on User { ...UserNano settings { "
        "about birthDate country dateLastSession "
        "displayedName email firstName gender lastName "
        "privacyName privacyProfile showAge showProfileType "
        "urlWebsite username zipCode __typename } __typename}"
        "fragment UserNano on User { following id isBlocked isScout "
        "name url username medias { avatar __typename } "
        "__typename}fragment ProductList on Product { category channel "
        "dateRelease dateReleaseEarlyAccess dateReleaseJP "
        "dateReleaseOriginal dateReleaseUS displayedYear duration "
        "frenchReleaseDate id numberOfSeasons originalRun "
        "originalTitle rating slug subtitle title universe url "
        "yearOfProduction tvChannel { name url __typename } "
        "countries { id name __typename } gameSystems { "
        "id label __typename } medias { picture __typename "
        "} genresInfos { label __typename } artists { name "
        "person_id url __typename } authors { name "
        "person_id url __typename } creators { name "
        "person_id url __typename } developers { name "
        "person_id url __typename } directors { name "
        "person_id url __typename } pencillers { name "
        "person_id url __typename } __typename}fragment "
        "ProductUserInfos on ProductUserInfos { dateDone "
        "hasStartedReview isCurrent id isDone isListed isRecommended "
        "isRejected isReviewed isWished productId rating userId "
        "numberEpisodeDone lastEpisodeDone { episodeNumber id "
        "season { seasonNumber id episodes { "
        "title id episodeNumber __typename } "
        " __typename } __typename } gameSystem { id label "
        "__typename } review { url __typename } __typename}"
        "fragment ProfileStats on User { likePositiveCountStats { "
        "contact feed list paramIndex review total "
        "__typename } stats { collectionCount diaryCount "
        "listCount followerCount ratingCount reviewCount "
        'scoutCount __typename } __typename}"'
    )
    query += (
        ', "variables":{'
        f'"action": "{action}", '
        f'"offset": {offset}, '
        f'"universe": "{universe}", '
        f'"username": "{username}"'
        "}}"
    )

    x = requests.post(
        url,
        data=query,
        headers={
            "Host": "apollo.senscritique.com",
            "Content-Type": "application/json",
            "Referer": url,
            "Accept": "application/json",
            "User-Agent": user_agent,
        },
    )

    d = json.loads(x.text)
    if d["data"]["user"] is None:
        raise ValueError(f"Member named `{username}` does not exist")

    collection = d["data"]["user"]["collection"]

    if collection["total"] == 0:
        return {"num_total": 0, "collection": []}

    items = []
    for x in collection["products"]:
        item = {
            "Title": x["originalTitle"] if x["originalTitle"] else x["title"],
            "Year": str(x["yearOfProduction"]),
            "Rating10": str(x["otherUserInfos"]["rating"]),
        }

        if action == "DONE":
            date = x["otherUserInfos"]["dateDone"]

            if date is None:
                date = ""
            else:
                date = str(date).split("T")[0]

            item.update({"WatchedDate": date})

            if add_review:
                if x["otherUserInfos"]["isReviewed"]:
                    review_url = x["otherUserInfos"]["review"]["url"]
                    review = get_review(review_url, user_agent)
                    item.update({"Review": review})
                else:
                    item.update({"Review": ""})

        items.append(item)

    results = {
        "num_total": collection["total"],
        "collection": items,
    }

    return results


def get_data(
    username: str,
    user_agent: str,
    universe: str = "movie",
    add_review: bool = False,
    action: str = "DONE",
) -> List[Dict[str, Any]]:
    """
    Send POST request

    :username: Senscritique username
    :user_agent: User agent
    :universe: 'movie' or 'tvShow'
    :add_review: Add review
    :action: 'DONE' or 'WISH'
    """

    results = []
    offset = 0
    data = get_data_batch(username, user_agent, offset, add_review, universe, action)
    num_total = data["num_total"]
    len_data = len(data["collection"])
    results += data["collection"]
    offset += len_data

    str_el = "films" if universe == "movie" else "TV shows"

    with Progress() as progress:
        task = progress.add_task(
            f"Collecting [bold violet]{str_el}[/bold violet]", total=num_total
        )
        while offset < num_total:
            data = get_data_batch(
                username, user_agent, offset, add_review, universe, action
            )

            len_data = len(data["collection"])
            results += data["collection"]
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
        parts = num_elements // limit

        for i in track(range(1, parts + 2), "Writing CSV parts"):
            if parts == 0:
                output_path = path
            else:
                output_path = path.replace(".csv", f"_{i}.csv")

            with open(output_path, "w") as f:
                writer = csv.DictWriter(f, fieldnames=labels)
                writer.writeheader()

                for elem in data[(i - 1) * limit : i * limit]:
                    writer.writerow(elem)


def pretty_table(
    data: List[Dict[str, str]], num_elements: int = 5, lim_review: int = 70
):
    """
    Pretty print table with `rich`

    :data: List of dictionaries containing the data
    :num_elements: Number of elements to print
    :lim_review: Number of maximal characters in the review
    """

    if len(data):
        add_watched_date = False
        add_review = False

        table = Table(title=f"{num_elements} last elements", show_header=True)
        table.add_column("Title")
        table.add_column("Date")
        table.add_column("Rating")

        add_watched_date = "WatchedDate" in data[0]
        if add_watched_date:
            table.add_column("Watched")
        add_review = "Review" in data[0]
        if add_review:
            table.add_column("Review")

        for x in data[:num_elements]:
            items = [x["Title"], x["Year"], x["Rating10"]]

            if add_watched_date:
                items.append(x["WatchedDate"])
            if add_review:
                review = x["Review"]
                if len(review) > lim_review:
                    short_review = review[:lim_review] + "..."
                else:
                    short_review = review

                items.append(short_review)

            table.add_row(*items)

        print(table)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--username", type=str, required=True, default=None, help="Your username"
    )
    parser.add_argument(
        "--add_tv", default=False, action="store_true", help="Add TV shows"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        default="output.csv",
        help="Output CSV path",
    )
    parser.add_argument(
        "--add_reviews", default=False, action="store_true", help="Add reviews or not"
    )
    parser.add_argument(
        "--watchlist_only",
        default=False,
        action="store_true",
        help="Extract only watchlist items",
    )
    parser.add_argument(
        "--user_agent",
        type=str,
        required=False,
        default="Mozilla/5.0",
        help="User agent",
    )
    p_args = parser.parse_args()

    item_action = "WISH" if p_args.watchlist_only else "DONE"
    universes = ["movie", "tvShow"] if p_args.add_tv else ["movie"]
    results = []

    for universe in universes:
        results += get_data(
            p_args.username,
            p_args.user_agent,
            universe,
            p_args.add_reviews,
            item_action,
        )

    if len(results) > 0:
        print(f"[bold green]Done:[/bold green] found {len(results)} elements!")
        pretty_table(results, num_elements=5, lim_review=70)
        write_csv(p_args.output, results)
    else:
        print(f"[bold red]Done:[/bold red] found {len(results)} element :(")
