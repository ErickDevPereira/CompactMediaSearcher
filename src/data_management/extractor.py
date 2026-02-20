from typing import Any, Dict, List, Callable
from src.custom_error.err_broken_json import BrokenJsonStructureException
from collections.abc import Iterator #Used to type the generator. Iterator[yeld type] is the type hint for simple generators.

class Extractor:

    std_msg: Callable[[str], str] = lambda msg : f'Bad structure for json extracted from {msg}'

    @staticmethod
    def extract_song_data(song_json: Dict[str, Any]) -> List[str]:
        """
        This method is responsible for getting JSON from the last.fm API and
        return a list with the title of the tracks concatenated together with the
        artist name as a string. For example: 'Dan Bull@The God Father' could be an
        item of such list. The text before @ is the artist name while the text after @
        is the track's title.

        song_json >> JSON dictionary that came from last.fm api.

        return >> List with 'artist@title' strings extracted from the JSON.
        """
        songs_data: List[str] = list()

        try:
            tracks: List[Dict[str, str | List[Dict[str, str]]]] = song_json['results']['trackmatches']['track']
            gen_filtered_data: Iterator[str] = ('@'.join([info_media['artist'], info_media['name']]) for info_media in tracks)
            for data in gen_filtered_data:
                    songs_data.append(data)
        except Exception as err:
            raise BrokenJsonStructureException(Extractor.std_msg('last.fm') + f'{err}')
        else:
            return songs_data
    
    @staticmethod
    def extract_movie_data(movie_json: Dict[str, str] | None) -> str | None:
        '''
        This method is responsible for getting JSON from the omdb API and
        return a string with the title of the movie concatenated together with the
        director name. For example: 'Dan Bull@The God Father' could be a result.
        The text before @ is the director name while the text after @
        is the title.

        movie_json >> JSON dictionary that came from omdb api.

        return >> string 'director@title' extracted from the JSON. None will be returned
        if the inputed JSON is None (it is possible in some contexts).
        '''
        if movie_json is None:
            return None

        try:
            director: str = movie_json['Director']
            title: str = movie_json['Title']
            result = '@'.join([
                            director if director != 'N/A' else '',
                            title if title != "N/A" else ""
                            ])
        except Exception as err:
            raise BrokenJsonStructureException(Extractor.std_msg('omdbAPI') + f'{err}')
        else:
            return result