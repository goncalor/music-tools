#!/usr/bin/env python3
import os
import sys
import eyed3
import logging
import lyrics as lyr

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %z',
                    level=logging.INFO)

for mp3 in sys.argv[1:]:
    logging.debug("Loading {}".format(mp3))
    tag = eyed3.load(mp3).tag
    artist = tag.artist
    title = tag.title
    logging.info("Getting lyrics for '{}' by '{}'".format(title, artist))

    try:
        lyrics = lyr.download_lyrics(artist, title)
    except Exception as e:
        logging.error("Failed with error {}".format(e))
        continue
    if not lyrics:
        logging.warning("No lyrics found for '{}' by '{}'".format(title, artist))
        continue

    (root, ext) = os.path.splitext(mp3)
    out_path = root + ".txt"

    logging.debug("Writing to {}".format(out_path))
    with open(out_path, "w") as f:
        f.write(lyrics)
