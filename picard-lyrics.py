PLUGIN_NAME = 'lyrics'
PLUGIN_AUTHOR = 'goncalor'
PLUGIN_DESCRIPTION = 'Fetch lyrics from AZLyrics.com'
PLUGIN_VERSION = '0.1'
PLUGIN_API_VERSIONS = ['2.0']
PLUGIN_LICENSE = 'GPL-2.0'
PLUGIN_LICENSE_URL = 'https://www.gnu.org/licenses/gpl-2.0.html'


from picard import config, log
from picard.metadata import register_track_metadata_processor
from .lyrics import download_lyrics


def process_track(album, metadata, track, release):
    artist = metadata['artist']
    title = metadata['title']
    lyrics = download_lyrics(artist, title)
    if not lyrics:
        log.warning('No lyrics found for "{}" by "{}"'.format(title, artist))
        return
    
    metadata['lyrics:description'] = lyrics

register_track_metadata_processor(process_track)
