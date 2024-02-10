<div align="center">

SensCritique2Letterboxd 🍿📊
============================

A script to export your movies from [SensCritique](https://senscritique.com) to [Letterboxd](https://letterboxd.com).

(It also works for *private* members!)

Supports: <b>watched</b> items (with <i>ratings</i>, <i>watched date</i>, <i>reviews</i>) and <b>watchlist</b>

![Screenshot](assets/screenshot.png)

</div>

## Requirements

Please use one of these methods to install the requirements:

### Poetry

Install the requirements with:

```bash
poetry install
```

Do not forget to activate your virtual environment with `poetry shell` (or use `poetry run`).

### Nix

If you have `nix` installed, there is a `flake.nix` with its `flake.lock` you can use.
Python packages are managed with `poetry2nix`.

Either use `direnv` integration _or_ run

```bash
nix develop github:rx342/senscritique2letterboxd
```

without the need to clone the repo.

### Pip

Install the requirements with `pip`:

```bash
pip3 install -r requirements.txt
```

## Usage

Please replace every `{USERNAME}` with your username.

### Watched

To export your movies:

```bash
python3 main.py --username {USERNAME} --output movies.csv
```

If you also want to add your TV shows, please run:

```bash
python3 main.py --username {USERNAME} --output movies.csv --add_tv
```

Finally if you want add your reviews:

```bash
python3 main.py --username {USERNAME} --output movies.csv --add_reviews
```

### Watchlist

To export the movies you *want* to watch (named "Watchlist" on Letterboxd):

```bash
python3 main.py --username {USERNAME} --output watchlist.csv --watchlist_only
```

And [import](https://letterboxd.com/import/) your CSV ✨.

### Nix

If you use Nix you do not need to clone the repo, just replace the `python3 main.py` with `nix run github:rx342/senscritique2letterboxd --`.
For instance:

```bash
nix run github:rx342/senscritique2letterboxd -- --username {USERNAME} --output movies.csv --add_tv
```
