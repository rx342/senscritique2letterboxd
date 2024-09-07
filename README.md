<div align="center">

SensCritique2Letterboxd (s2l) 🍿📊
==================================

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

And you can run any commands with

```bash
poetry run s2l ...
```

### Nix

Make sure you enabled flakes and you can run any commands with

```bash
nix run github:rx342/senscritique2letterboxd#s2l ...
```

## Usage

Please replace every `{USERNAME}` with your username.

### Watched

To export your movies:

```bash
s2l --username {USERNAME} --output movies.csv
```

If you also want to add your TV shows, please run:

```bash
s2l --username {USERNAME} --output movies.csv --add_tv
```

Finally if you want add your reviews:

```bash
s2l --username {USERNAME} --output movies.csv --add_reviews
```

### Watchlist

To export the movies you *want* to watch (named "Watchlist" on Letterboxd):

```bash
s2l --username {USERNAME} --output watchlist.csv --watchlist_only
```

And [import](https://letterboxd.com/import/) your CSV ✨.
