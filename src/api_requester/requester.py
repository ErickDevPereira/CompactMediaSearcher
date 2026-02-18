import aiohttp
from typing import Dict

class Requester:

    def __init__(self, song_api_key: str, movie_api_key: str, game_api_key: Dict[str, str], book_api_key: str):
        self.__song_api_key: str = song_api_key #api from last.fm
        self.__movie_api_key: str = movie_api_key #omdb API
        self.__game_api_key: str = game_api_key #api from Twitch
        self.__book_api_key: str = book_api_key  #api from Google
    
