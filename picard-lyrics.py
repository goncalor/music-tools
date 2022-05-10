PLUGIN_NAME = 'lyrics'
PLUGIN_AUTHOR = 'goncalor'
PLUGIN_DESCRIPTION = 'Fetch lyrics from AZLyrics.com'
PLUGIN_VERSION = '0.1'
PLUGIN_API_VERSIONS = ['2.0']
PLUGIN_LICENSE = 'GPL-2.0'
PLUGIN_LICENSE_URL = 'https://www.gnu.org/licenses/gpl-2.0.html'

from picard import config, log
from picard.track import Track
from picard.metadata import register_track_metadata_processor
from picard.ui.itemviews import (
    BaseAction,
    register_track_action,
)
from .lyrics import download_lyrics


# TODO: download lyrics only if track has no lyrics
def process_track(album, metadata, track, release):
    # if 'lyrics' in metadata or 'lyrics:description' in metadata:
    #     return

    artist = metadata['artist']
    title = metadata['title']
    lyrics = download_lyrics(artist, title)
    if not lyrics:
        log.warning('No lyrics found for "{}" by "{}"'.format(title, artist))
        return

    metadata['lyrics:description'] = lyrics


class AddLyrics(BaseAction):
    NAME = 'Add lyrics tag'

    def callback(self, objs):
        for track in (t for t in objs if isinstance(t, Track)):
            # add empty lyrics tag
            track.files[0].metadata.update({'lyrics:description': ''})
            track.tagger.window.refresh_metadatabox()


register_track_metadata_processor(process_track)
register_track_action(AddLyrics())
