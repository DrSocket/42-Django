#!/usr/bin/env python3

import requests
import json
import dewiki
import sys


def request_wikipedia(page: str):
    try:
        page = requests.get("https://en.wikipedia.org/w/api.php", params={
        "action": "parse",
        "page": page,
        "prop": "wikitext",
        "format": "json",
        "redirects": "true"
        })
        page.raise_for_status()
    except requests.HTTPError as e:
        raise e
    try:
        data = page.json()
    except ValueError as e:
        raise e
    if data.get("error") is not None:
        raise Exception(data["error"]["info"])
    return (dewiki.from_string(data["parse"]["wikitext"]["*"]))


def main():
    if (len(sys.argv) == 2):
        try:
            wiki_data = request_wikipedia(sys.argv[1])
        except Exception as e:
            raise e
        try:
            f = open("{}.wiki".format(sys.argv[1]), "w")
            f.write(wiki_data.strip())
            f.close()
        except Exception as e:
            return print(e)
    elif len(sys.argv) == 1:
        print("Need one argument! : search_term")
    else:
        print("wrong argument count!")


if __name__ == '__main__':
    main()