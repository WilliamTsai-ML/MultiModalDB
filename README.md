# expDB
Experimental implementation of knowledge database

## Setup
```bash
pip install .  # to build and install as a package, or
pip install -e .  # to build and install EDITABLE library
```

## Test run
```bash
run_createDB_api  # to run automatic flow to build entire database
run_searchDB_api [search_query_sentance]  # to search entire database with keyword
```

Example output:
```shell
$ run_searchDB_api "smartphone"
```
```text
Searching for matching news articles about smartphone
Top document results:
0: news_apple_3 {'doc-chunk': 3, 'doc-id': 'news_apple'} Iphone is the most popular smartphone in the world.
1: news_google_2 {'doc-chunk': 2, 'doc-id': 'news_google'} Android is the most popular MobileOS in terms of number of users.
2: news_google_0 {'doc-chunk': 0, 'doc-id': 'news_google'} Google has released their new pixel phone as one of the most popular Android phone.
Top image results:
0: iphone15 (0.7597850459604857)
1: galaxy (0.7694114265391094)
2: ipad (0.7960707200732159)
```