#!/usr/bin/env python3
import os
import sys
import eyed3
import lyrics as lyr

for mp3 in sys.argv[1:]:
    tag = eyed3.load(mp3).tag
    artist = tag.artist
    title = tag.title

    lyrics = lyr.download_lyrics(artist, title)

    (root, ext) = os.path.splitext(mp3)
    out_path = root + ".txt"

    with open(out_path, "w") as f:
        f.write(lyrics)
