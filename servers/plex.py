from plexapi.server import PlexServer

from servers.base import _ServerHook

# Todo: remove these to settings


class PlexHook(_ServerHook):
    def __init__(self, plex_host, plex_token):
        self._plex = PlexServer(plex_host, plex_token)

    def find_movie(self, criteria, mediatype='movie'):
        ret = []
        for video in self._plex.search(criteria, mediatype=mediatype):
            print(video)
            ret.append(video)
        return ret

    def update_library(self, name='Recommended'):
        library = self._plex.library.section(name)
        library.update()
