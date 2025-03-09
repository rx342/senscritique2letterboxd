import pytest


def test_get_data_batch():
    from s2l.utils import get_data_batch

    with pytest.raises(ValueError):
        # No account
        get_data_batch("fdqsbuiofazbuebfqlsbdfq", "Mozilla/5.0")
        # Neither `movies` nor `tvShow`
        get_data_batch(
            "fdqsuiflazbazdfqs", "Mozilla/5.0", universe="neithermoviesnortvshow"
        )
        # Neither `DONE` nor `WISH`
        get_data_batch("fdzubazea", "Mozilla/5.0", action="neitherdonenorwish")


def test_movies():
    from s2l.utils import get_data

    item_action = "DONE"
    universes = ["movie"]

    results = []
    for universe in universes:
        results += get_data("vsv", "Mozilla/5.0", universe, False, item_action)

    assert len(results) > 0


def test_movies_and_tvshows():
    from s2l.utils import get_data

    item_action = "DONE"
    universes = ["movie", "tvShow"]

    results = []
    for universe in universes:
        results += get_data("vsv", "Mozilla/5.0", universe, False, item_action)

    assert len(results) > 0


def test_movies_with_reviews():
    from s2l.utils import get_data

    item_action = "DONE"
    universes = ["movie"]

    results = []
    for universe in universes:
        results += get_data("vsv", "Mozilla/5.0", universe, True, item_action)

    assert len(results) > 0


def test_movies_and_tvshows_with_reviews():
    from s2l.utils import get_data

    item_action = "DONE"
    universes = ["movie", "tvShow"]

    results = []
    for universe in universes:
        results += get_data("vsv", "Mozilla/5.0", universe, True, item_action)

    assert len(results) > 0


def test_watchlist_movies():
    from s2l.utils import get_data

    item_action = "WISH"
    universes = ["movie"]

    results = []
    for universe in universes:
        results += get_data("vsv", "Mozilla/5.0", universe, False, item_action)

    assert len(results) > 0


def test_watchlist_movies_and_tvshows():
    from s2l.utils import get_data

    item_action = "WISH"
    universes = ["movie", "tvShow"]

    results = []
    for universe in universes:
        results += get_data("vsv", "Mozilla/5.0", universe, False, item_action)

    assert len(results) > 0
