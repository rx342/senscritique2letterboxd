<div align="center">

# SensCritique2Letterboxd (s2l) 🍿📊

A script to export your movies from [SensCritique](https://senscritique.com) to [Letterboxd](https://letterboxd.com).

(It also works for _private_ members!)

Supports: <b>watched</b> items (with <i>ratings</i>, <i>watched date</i>, <i>reviews</i>) and <b>watchlist</b>

![Screenshot](assets/screenshot.png)

</div>

## Installation

Please use one of these methods to install the package.

### Pip

Install the package with:

```bash
pip install s2l
```

## Usage

### 🌟 New feature (+0.2.0): interactive mode

```bash
s2l -i
```

### CLI

Please replace every `{USERNAME}` with your username.

#### Watched

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

#### Watchlist

To export the movies you _want_ to watch (named "Watchlist" on Letterboxd):

```bash
s2l --username {USERNAME} --output watchlist.csv --watchlist_only
```

And [import](https://letterboxd.com/import/) your CSV ✨.

## Development

You can spawn a shell with all dependencies with the following method

### Poetry

```bash
poetry env activate
```

### Nix

```bash
nix-shell
```
