PLUGIN_NAME = 'lyrics'
PLUGIN_AUTHOR = 'goncalor'
PLUGIN_DESCRIPTION = 'Fetch lyrics from AZLyrics.com'
PLUGIN_VERSION = '0.1'
PLUGIN_API_VERSIONS = ['2.0']
PLUGIN_LICENSE = 'GPL-2.0'
PLUGIN_LICENSE_URL = 'https://www.gnu.org/licenses/gpl-2.0.html'

import time
import random
from picard import config, log
from picard.track import Track
from picard.file import register_file_post_addition_to_track_processor
from picard.ui.itemviews import (
    BaseAction,
    register_track_action,
    register_album_action,
)
from picard.util.webbrowser2 import open as browse
from PyQt5.QtWidgets import QInputDialog

from .lyrics import download_lyrics

MAX_DOWNLOAD_DELAY = 3.5


def add_lyrics(file):
    if 'lyrics' in file.metadata or 'lyrics:description' in file.metadata:
        return

    time.sleep(random.uniform(0, MAX_DOWNLOAD_DELAY))
    artist = file.metadata['artist']
    title = file.metadata['title']
    lyrics = download_lyrics(artist, title)
    if not lyrics:
        log.warning('No lyrics found for "{}" by "{}"'.format(title, artist))
        return

    file.metadata['lyrics:description'] = lyrics


class AddLyrics(BaseAction):
    NAME = 'Auto-add lyrics'

    def callback(self, objs):
        for album_or_track in objs:
            for file in album_or_track.iterfiles():
                add_lyrics(file)

        album_or_track.tagger.window.refresh_metadatabox()


class AddEmptyLyrics(BaseAction):
    NAME = 'Add lyrics tag'

    def callback(self, objs):
        for track in (t for t in objs if isinstance(t, Track)):
            if not len(track.files):
                return
            # add empty lyrics tag
            track.files[0].metadata.update({'lyrics:description': ' '})
            track.tagger.window.refresh_metadatabox()


class BrowseLyrics(BaseAction):
    NAME = 'Browse for lyrics'

    def callback(self, objs):
        for track in (t for t in objs if isinstance(t, Track)):
            artist = track.metadata['artist']
            title = track.metadata['title']
            browse('https://duckduckgo.com/?q={} {} lyrics'.format(
                artist, title))

            if not len(track.files):
                return
            # TODO: open browser after dialog, not the other way around
            text, ok = QInputDialog.getMultiLineText(None, 'Add lyrics',
                                                     'Lyrics:')
            if ok:
                track.files[0].metadata.update({'lyrics:description': text})
                track.tagger.window.refresh_metadatabox()


register_track_action(AddLyrics())
register_album_action(AddLyrics())
register_track_action(BrowseLyrics())
# register_track_action(AddEmptyLyrics())
