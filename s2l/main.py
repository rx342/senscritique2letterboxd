#!/usr/bin/env python3

from rich import print

from .utils import get_data, pretty_table, write_csv


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
