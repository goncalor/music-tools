music-tools
===========

A set of tools to work with and manage music files.

`picard-lyrics.py`
------------------

Lazy Lyrics [MusicBrainz Picard][picard] plugin to automatically add lyrics to songs. Build the plugin with `picard-lyrics-build.sh`, or download it ready to install from [releases][releases].

The plugin adds an "Auto-add lyrics" action to albums and tracks on Picard. Clicking this action attempts to automatically find and add lyrics for the selected tracks.

An additional "Browse for lyrics" action is also added which looks up lyrics for the selected tracks in a browser. Once you find the right lyrics it allows you to quickly add them to the track.

`download-lyrics.py <file ...>`
-------------------------------

Download lyrics for a set of ID3 tagged files and save them to `.txt` files.


[picard]: https://picard.musicbrainz.org/
[releases]: https://github.com/goncalor/music-tools/releases
