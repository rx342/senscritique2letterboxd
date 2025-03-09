#!/usr/bin/env python3

from rich import print

from .utils import get_data, get_user_inputs, pretty_table, write_csv


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive mode"
    )
    parser.add_argument("--username", type=str, default=None, help="Your username")
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

    if p_args.interactive:
        user_inputs = get_user_inputs()
        item_action = "WISH" if user_inputs["watchlist"] else "DONE"
        universes = ["movie", "tvShow"] if user_inputs["tv"] else ["movie"]
        username = user_inputs["username"]
        add_reviews = user_inputs["reviews"]
    else:
        if p_args.username is None:
            parser.error("--username is required unless --interactive is set.")

        item_action = "WISH" if p_args.watchlist_only else "DONE"
        universes = ["movie", "tvShow"] if p_args.add_tv else ["movie"]
        username = p_args.username
        add_reviews = p_args.add_reviews

    results = []

    for universe in universes:
        results += get_data(
            username,  # type: ignore
            p_args.user_agent,
            universe,
            add_reviews,  # type: ignore
            item_action,
        )

    if len(results) > 0:
        print(f"[bold green]Done:[/bold green] found {len(results)} elements!")
        pretty_table(results, num_elements=5, lim_review=70)
        write_csv(p_args.output, results)
    else:
        print(f"[bold red]Done:[/bold red] found {len(results)} element :(")
