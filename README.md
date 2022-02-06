SensCritique2Letterboxd 🍿📊
============================

If you want to export your movies from [SensCritique](https://senscritique.com) to [Letterboxd](https://letterboxd.com).

## Requirements

**Your SensCritique account needs to be public.**

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
