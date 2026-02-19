from .requester import Requester
import os
import dotenv

dotenv.load_dotenv('.env')

requester_sgt: Requester = Requester(
    song_api_key = os.getenv('SONG_KEY'),
    movie_api_key = os.getenv('MOVIES_KEY'),
    game_api_key = {'client_id': os.getenv('CLIENT_ID_GAMES'), 'client_secret': os.getenv('SECRET_KEY_GAMES')},
    book_api_key = os.getenv('BOOKS_KEY')
    )
