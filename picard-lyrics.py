PLUGIN_NAME = 'lyrics'
PLUGIN_AUTHOR = 'goncalor'
PLUGIN_DESCRIPTION = 'Fetch lyrics from AZLyrics.com'
PLUGIN_VERSION = '0.1'
PLUGIN_API_VERSIONS = ['2.0']
PLUGIN_LICENSE = 'GPL-2.0'
PLUGIN_LICENSE_URL = 'https://www.gnu.org/licenses/gpl-2.0.html'

from picard import config, log
from picard.track import Track
from picard.file import register_file_post_addition_to_track_processor
from picard.ui.itemviews import (
    BaseAction,
    register_track_action,
)
from .lyrics import download_lyrics


def process_file(track, file):
    if 'lyrics' in file.metadata or 'lyrics:description' in file.metadata:
        return

    artist = track.metadata['artist']
    title = track.metadata['title']
    lyrics = download_lyrics(artist, title)
    if not lyrics:
        log.warning('No lyrics found for "{}" by "{}"'.format(title, artist))
        return

    file.metadata['lyrics:description'] = lyrics


class AddLyrics(BaseAction):
    NAME = 'Add lyrics tag'

    def callback(self, objs):
        for track in (t for t in objs if isinstance(t, Track)):
            # add empty lyrics tag
            track.files[0].metadata.update({'lyrics:description': ''})
            track.tagger.window.refresh_metadatabox()


# if you want to load lyrics to any loaded file, replace with register_file_post_load_processor
register_file_post_addition_to_track_processor(process_file)
register_track_action(AddLyrics())
