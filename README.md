SensCritique2Letterboxd 🍿📊
============================

If you want to export your movies from [SensCritique](https://senscritique.com) to [Letterboxd](https://letterboxd.com).

(It also works for *private* members!)

## Requirements

Please use one of these methods to install the requirements:

### Poetry

Please install the requirements with:

```bash
poetry install
```

Do not forget to activate your virtual environment with `poetry shell` (or use `poetry run`).

### Nix

If you have `nix` installed, there is a `flake.nix` with its `flake.lock` you can use.

Either use `direnv` integration _or_ run

```bash
nix develop
```

and you will get a shell with everything installed.

### Pip

Please install the requirements with `pip`:

```bash
pip3 install -r requirements.txt
```

## Usage

To export your movies:

```bash
python3 main.py --username {USERNAME} --output movies.csv
```

If you also want to add your TV shows, please run:

```bash
python3 main.py --username {USERNAME} --output movies.csv --add_tv
```

And [import](https://letterboxd.com/import/) your CSV ✨.
