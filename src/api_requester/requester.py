from asyncio import create_task
import aiohttp
from typing import Dict, Any, Callable, Coroutine
from src.custom_error import AsyncHttpRequestProblem

class Requester:

    def __init__(self, song_api_key: str, movie_api_key: str, game_api_key: Dict[str, str], book_api_key: str):
        
        self.__song_api_key: str = song_api_key #api from last.fm
        self.__movie_api_key: str = movie_api_key #OMDB API
        self.__game_api_key: str = game_api_key #api from Twitch
        self.__book_api_key: str = book_api_key  #api from Google
        self.__err_msg: Callable[[int, str], str] = lambda status, api_name : f'Something went wrong during a request to {api_name}. Status >> {status}'
    
    async def __fetch_song(self, song_name: str) -> Dict[str, Any]:
        '''
        This is a coroutine that fetches song data based on the name of the track. The data is returned as a dictionary.

        song_name >> string with the track name.
        return >> returns a dicitonary with the data of that searched song.
        '''
        self.__BASE_URL_SONG: str = f"http://ws.audioscrobbler.com/2.0/?method=track.search&format=json&api_key={self.__song_api_key}&"
        self.__URL: Callable[[str], str] = lambda track : self.__BASE_URL_SONG + f'track={track}'

        async with aiohttp.ClientSession() as session:
            async with session.get(self.__URL(song_name)) as resp:
                if resp.status == 200:
                    return await resp.json()
                raise AsyncHttpRequestProblem(self.__err_msg(resp.status, 'last.fm'))
    
    async def __fetch_movie(self, movie_title: str) -> Dict[str, str]:
        self.__BASE_URL_MOVIE: str = f"http://www.omdbapi.com/?apikey={self.__movie_api_key}&t={movie_title}"

        async with aiohttp.ClientSession() as session:
            async with session.get(self.__BASE_URL_MOVIE) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data['Response'] == 'False':
                        raise AsyncHttpRequestProblem(self.__err_msg(404, 'omdbAPI'))
                raise AsyncHttpRequestProblem(self.__err_msg(resp.status, 'omdbAPI'))

    async def fetch_all(self, title: str) -> Dict[str, Any]:
        '''
        This function will fetch data of movies, songs, books and games based
        on a title. All fetched data will be returned.

        title >> title of the media. This title will be used to search the medias in the external apis.
        return >> dictionary with data from the medias.
        '''
        self.__all_data: Dict[str, Any] = dict()
        #Coroutines:
        self.__coroutines: Dict[str, Coroutine[Any, Any, Dict[str, Any]]] = {
            'songs': self.__fetch_song(title),
            'movies': self.__fetch_movie(title)
            }
        #Tasks:
        for media, crt in self.__coroutines.items():
            try:
                self.__task: Dict[str, Any] = await create_task(crt)
            except AsyncHttpRequestProblem:
                self.__all_data.update({media: None})
            else:
                self.__all_data.update({media: self.__task})
        #Fetched data
        return self.__all_data