
from picard.plugin3.api import PluginApi

from picard.plugin3.api import (
    BaseAction,
    Track,
)

import time
import random


from picard.util.webbrowser2 import open as browse
from PyQt6.QtWidgets import QInputDialog

from .lyrics import download_lyrics

MAX_DOWNLOAD_DELAY = 3.5


def add_lyrics(api, file):
    if 'lyrics' in file.metadata or 'lyrics:description' in file.metadata:
        return

    time.sleep(random.uniform(1, MAX_DOWNLOAD_DELAY))
    artist = file.metadata['artist']
    title = file.metadata['title']
    lyrics = download_lyrics(artist, title)
    if not lyrics:
        api.logger.warning('No lyrics found for "{}" by "{}"'.format(title, artist))
        return

    file.metadata['lyrics:description'] = lyrics


class AddLyrics(BaseAction):
    TITLE = "Auto-add lyrics"

    def callback(self, objs):
        for album_or_track in objs:
            for file in album_or_track.iterfiles():
                add_lyrics(self.api, file)

        album_or_track.tagger.window.refresh_metadatabox()


class AddEmptyLyrics(BaseAction):
    TITLE = "Add lyrics tag"

    def callback(self, objs):
        for track in (t for t in objs if isinstance(t, Track)):
            if not len(track.files):
                return
            # add empty lyrics tag
            track.files[0].metadata.update({'lyrics:description': ' '})
            track.tagger.window.refresh_metadatabox()


class BrowseLyrics(BaseAction):
    TITLE = "Browse for lyrics"

    def callback(self, objs):
        for track in (t for t in objs if isinstance(t, Track)):
            artist = track.metadata['artist']
            title = track.metadata['title']
            browse('https://duckduckgo.com/?q={} {} lyrics'.format(
                artist, title))

            if not len(track.files):
                return
            # TODO: open browser after dialog, not the other way around
            text, ok = QInputDialog.getMultiLineText(
                None, 'Add lyrics',
                'Lyrics for "{}" by "{}":'.format(title, artist))
            if ok:
                track.files[0].metadata.update({'lyrics:description': text})
                track.tagger.window.refresh_metadatabox()


# register_track_action(AddEmptyLyrics())


def enable(api: PluginApi):
    """Called when plugin is enabled."""
    api.register_track_action(AddLyrics)
    api.register_album_action(AddLyrics)
    api.register_track_action(BrowseLyrics)
