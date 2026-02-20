from asyncio import gather
import aiohttp
from typing import Dict, Any, Callable, List
from src.custom_error import AsyncHttpRequestProblem

class Requester:

    def __init__(self, song_api_key: str, movie_api_key: str, game_api_key: Dict[str, str], book_api_key: str):
        
        self.__song_api_key: str = song_api_key #api from last.fm
        self.__movie_api_key: str = movie_api_key #OMDB API
        self.__game_api_key: Dict[str, str] = game_api_key #api from Twitch
        self.__book_api_key: str = book_api_key  #api from Google
        self.__err_msg: Callable[[int, str], str] = lambda status, api_name : f'Something went wrong during a request to {api_name}. Status >> {status}'
    
    async def __fetch_song(self, song_name: str) -> Dict[str, Any]:
        '''
        This is a coroutine that fetches song data based on the name of the track. The data is returned as a dictionary.

        song_name >> string with the track name.
        return >> returns a dicitonary with the data of that searched song.
        '''
        print('start')
        self.__BASE_URL_SONG: str = f"http://ws.audioscrobbler.com/2.0/?method=track.search&format=json&api_key={self.__song_api_key}&"
        self.__URL: Callable[[str], str] = lambda track : self.__BASE_URL_SONG + f'track={track}'

        async with aiohttp.ClientSession() as session:
            async with session.get(self.__URL(song_name)) as resp:
                if resp.status == 200:
                    print('end')
                    return await resp.json()
                raise AsyncHttpRequestProblem(self.__err_msg(resp.status, 'last.fm'))
    
    async def __fetch_movie(self, movie_title: str) -> Dict[str, str] | None:
        '''
        This is a coroutine that fetches data about movies based on the title. The data is returned as a dictionary.

        movie_title >> string with the title.
        returned value >> returns a dicitonary with the data of that searched movie.
        '''
        print('start')
        self.__BASE_URL_MOVIE: str = f"http://www.omdbapi.com/?apikey={self.__movie_api_key}&t={movie_title}"
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__BASE_URL_MOVIE) as resp:
                if resp.status == 200:
                    data: Dict[str, str] = await resp.json()
                    print('end')
                    if data['Response'] == 'False':
                        return None #Can't finde such movie
                    return data #Everithing went fine
                raise AsyncHttpRequestProblem(self.__err_msg(resp.status, 'omdbAPI'))
    
    async def __fetch_book(self, book_title: str) -> Dict[str, Any]:
        '''
        This is a coroutine that fetches data about books based on the title. The data is returned as a dictionary.

        book_title >> string with the title.
        return >> returns a dicitonary with the data of that searched book.
        '''
        print('start')
        self.__BASE_URL_BOOK: str = f'https://www.googleapis.com/books/v1/volumes?key={self.__book_api_key}&q={book_title}'
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__BASE_URL_BOOK) as resp:
                if resp.status == 200:
                    print('end')
                    return await resp.json()
                raise AsyncHttpRequestProblem(self.__err_msg(resp.status, 'googleapi'))

    async def __fetch_game(self, game_title: str) -> List[Any]:
        """
        This is a coroutine that fetches data about games based on the title of a game. The data is returned as a list.

        game_title >> string with the title.
        returned value >> returns a list with games.
        """
        print('start')
        self.__BASE_URL_GAME1: str = f'https://id.twitch.tv/oauth2/token?client_id={self.__game_api_key['client_id']}&client_secret={self.__game_api_key['client_secret']}&grant_type=client_credentials'
        async with aiohttp.ClientSession() as session:
            async with session.post(self.__BASE_URL_GAME1) as resp:
                if resp.status == 200:
                    self.__game_data: Dict[str, Any] = await resp.json()
                    self.__access_token: str = self.__game_data['access_token']
                else:
                    raise AsyncHttpRequestProblem(self.__err_msg(resp.status, 'twitchapi'))
        self.__BASE_URL_GAME2: str = 'https://api.igdb.com/v4/games'
        async with aiohttp.ClientSession() as session:
            async with session.post(self.__BASE_URL_GAME2, headers = {
                'Client-ID': self.__game_api_key['client_id'],
                'Authorization': f'Bearer {self.__access_token}'
            }, data = f'fields id,name,summary; search "{game_title}";') as resp:
                if resp.status == 200:
                    print('end')
                    return await resp.json()
                raise AsyncHttpRequestProblem(self.__err_msg(resp.status, 'twitchapi'))

    async def fetch_all(self, title: str) -> Dict[str, Dict[str, Any] | List[Any]]:
        '''
        This function will fetch data of movies, songs, books and games based
        on a title. All fetched data will be returned.

        title >> title of the media. This title will be used to search the medias in the external apis.
        return >> dictionary with data from the medias.
        '''
        #Tasks:
        self.__results: List[Dict[str, Any] | List[Any] | None] = await gather(*[
            self.__fetch_song(title),
            self.__fetch_movie(title),
            self.__fetch_book(title),
            self.__fetch_game(title)
        ])
        self.__data: Dict[str, Dict[str, Any] | List[Any] | None] = dict()
        for ind, media in enumerate(('songs', 'movies', 'books', 'games')):
            self.__data.update({media: self.__results[ind]})
        #Fetched data:
        return self.__data