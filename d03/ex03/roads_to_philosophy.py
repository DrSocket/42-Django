#!/usr/bin/env python3

import requests
import sys
from bs4 import BeautifulSoup


def main():
    response = requests.get(f"https://en.wikipedia.org/wiki/{sys.argv[1]}")
    seen = []
    if response.ok and response is not None:
        try:
            html = BeautifulSoup(response.text, 'html.parser')
            title = html.select("#firstHeading")[0].text
            seen.append(title)
            while title != 'Philosophy':
                for para in html.find_all('p'):
                    link = ""
                    for l in para.find_all('a', href=True):
                        if '/wiki/Help:' in l['href'] or '/wiki/File' in l['href']:
                            continue
                        if '/wiki/' not in l['href']:
                            continue
                        if (l is not None):
                            link = l
                            break
                    if link != "":
                        break
                if link == "":
                    return "It's a dead end !"
                # print(link)
                response = requests.get(
                    f"https://en.wikipedia.org/{link.get('href')}")
                html = BeautifulSoup(response.text, 'html.parser')
                title = html.select("#firstHeading")[0].text
                if (title in seen):
                    return ("It leads to an infinite loop !")
                else:
                    seen.append(title)
        except Exception as e:
            return f"Error {e}"
    return seen


if __name__ == "__main__":
    if (len(sys.argv) == 2):
        seen = main()
        if isinstance(seen, list):
            for elem in seen:
                print(elem)
            print(f'{len(seen)} roads from {sys.argv[1]} to philosophy !')
        else:
            print(seen)
