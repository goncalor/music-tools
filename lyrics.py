#!/usr/bin/env python3
import sys
import string
import lxml.html
import requests
import xml.etree.ElementTree as ET

BASE_URL = "https://www.azlyrics.com/lyrics/"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"


def extract_lyrics(page):
    html = lxml.html.fromstring(page)

    for div in html.findall(".//*div"):
        if not div.attrib:
            lyrics = ET.tostringlist(div, encoding="unicode", method="text")
            lyrics = [s.strip() for s in lyrics]

            tmp = list()
            start = 0
            end = len(lyrics)
            for l in lyrics:
                if l == "":
                    start += 1
                else:
                    break
            for l in lyrics[::-1]:
                if l == "":
                    end -= 1
                else:
                    break
            return "\n".join(lyrics[start:end])


def normalise(name):
    name = name.lower()
    name = "".join(
        [a for a in name if a in string.ascii_letters + string.digits])

    return name


def download_lyrics(artist, title):
    artist = normalise(artist)
    title = normalise(title)

    url = "{}{}/{}.html".format(BASE_URL, artist, title)

    r = requests.get(url, headers={'user-agent': USER_AGENT})
    r.raise_for_status()

    lyrics = extract_lyrics(r.text)

    return lyrics


if __name__ == "__main__":
    print(download_lyrics(sys.argv[1], sys.argv[2]))
