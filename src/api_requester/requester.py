from asyncio import gather
import aiohttp
from typing import Dict, Any, List
from src.custom_error import AsyncHttpRequestProblem

class Requester:

    def __init__(self, song_api_key: str, movie_api_key: str, game_api_key: Dict[str, str], book_api_key: str):
        
        self.__song_api_key: str = song_api_key #api from last.fm
        self.__movie_api_key: str = movie_api_key #OMDB API
        self.__game_api_key: str = game_api_key #api from Twitch
        self.__book_api_key: str = book_api_key  #api from Google
        self.__err_msg = lambda status, api_name : f'Something went wrong during a request to {api_name}. Status >> {status}'
    
    async def __fetch_song(self, song_name: str) -> Dict[str, Any]:
        self.__BASE_URL: str = f"http://ws.audioscrobbler.com/2.0/?method=track.search&format=json&api_key={self.__song_api_key}&"
        self.__URL = lambda track : self.__BASE_URL + f'track={track}'

        async with aiohttp.ClientSession() as session:
            async with session.get(self.__URL(song_name)) as resp:
                if resp.status == 200:
                    return await resp.json()
                raise AsyncHttpRequestProblem(self.__err_msg(resp.status, 'last.fm'))
    
    async def fetch_all(self, title: str) -> Dict[str, Any]:
        self.__req_coroutines: List[Any] = [
            self.__fetch_song(title)
        ]
        self.__tasks = await gather(*self.__req_coroutines)
        return self.__tasks