from flask_restful import Resource, abort, reqparse, Api
from flask import request, Flask
from werkzeug.security import check_password_hash, generate_password_hash
from typing import Dict, Tuple, Any, Callable, List
from src.db.dml import DataBaseManager
from src.db.ddl import Connection
import os
from mysql.connector.errors import IntegrityError
from src.custom_error import LackingCredentialError
from src.db.dql import QueryBuilder
from src.api.jwt.singleton import jwt_heart
from src.api.jwt.auth_jwt import auth_jwt
import datetime
from src.api_requester import requester_sgt
from src.data_management.extractor import Extractor
from asyncio import run
from src.data_management.similarity import DocumentFilter
from pprint import pprint

class HTTP:

    app: Flask = Flask(__name__)
    api: Api = Api(app)
    user_args: Any = reqparse.RequestParser()
    login_args: Any = reqparse.RequestParser()
    msg_help: Callable[[str], str] = lambda msg : f'problem at \'{msg}\' field'

    @classmethod
    def __set_rsrc(cls) -> None:
        cls.user_args.add_argument('first_name', type = str, help = cls.msg_help('first_name'))
        cls.user_args.add_argument('last_name', type = str, help = cls.msg_help('last_name'))
        cls.user_args.add_argument('email', type = str, help = cls.msg_help('email'))
        cls.login_args.add_argument('email', type = str, help = cls.msg_help('email'))
        cls.login_args.add_argument('token', type = str, help = cls.msg_help('token'))
        cls.api.add_resource(cls.Register, '/register')
        cls.api.add_resource(cls.Login, '/login')
        cls.api.add_resource(cls.Searcher, '/search')
    
    @classmethod
    def start_server(cls) -> None:
        cls.__set_rsrc()
        cls.app.run(debug = True)

    class Register(Resource):

        def post(self) -> Tuple[Dict[str, str], int]:

            self.new_user_data: Dict[str, str] = HTTP.user_args.parse_args()
            self.__fields: Tuple[str, ...] = ('first_name', 'last_name', 'email')

            for field in self.__fields:
                if self.new_user_data[field] is None:
                    abort(400, message = f'Problem >> you must fill the field "{field}"')
            
            self.__mysql_user: str | None= os.getenv('MYSQL_USER')
            self.__mysql_pw: str | None = os.getenv('MYSQL_PW')
            self.__mysql_db: str | None = os.getenv('DATABASE_NAME')

            self.__mysql_cred: Tuple[str, str] = (self.__mysql_user, self.__mysql_pw)
            for cred in self.__mysql_cred:
                if cred is None:
                    raise LackingCredentialError(
                        """MySQL credentials must be inside a .env file at the root of the project.' \
                        The needed variables are: MYSQL_USER, MYSQL_PW"""
                    )

            try:
                CONN: Connection = Connection()
                with CONN.StrongConnection(
                    user = self.__mysql_user,
                    password = self.__mysql_pw,
                    database = self.__mysql_db
                ) as cnx:
                    with CONN.CursorManager(cnx) as cursor:
                        self.__token: str = os.urandom(8).hex() #Token with 8 bytes
                        self.__werkzeugged_token: str = generate_password_hash(self.__token) #Protecting the token
                        DataBaseManager.load_users(
                            cnx=cnx,
                            cursor=cursor,
                            token=self.__werkzeugged_token,
                            fname=self.new_user_data['first_name'],
                            lname=self.new_user_data['last_name'],
                            email=self.new_user_data['email']
                        )
            except IntegrityError:
                abort(422, message = 'The email has a bad format or already exists on the database')
            else:
                return {
                    'message': 'You are a new user. Save your token with you!',
                    'token': self.__token
                    }, 201
    
    class Login(Resource):

        def get(self) -> Tuple[Dict[str, str], int]:
            self.__login_json: Any = HTTP.login_args.parse_args()

            if self.__login_json['email'] is None or self.__login_json['token'] is None:
                abort(400, message = 'Please, provide data for the fields "email" and "token"')
            
            try:
                CONN: Connection = Connection()
                with CONN.StrongConnection(
                    user = os.getenv('MYSQL_USER'),
                    password = os.getenv('MYSQL_PW'),
                    database = os.getenv('DATABASE_NAME')
                ) as cnx:
                    with CONN.CursorManager(cnx) as cursor:
                        self.__udata: Dict[str, int | str] | None = QueryBuilder.get_user_by_email(cursor, self.__login_json['email'])
                        if self.__udata is None:
                            abort(403, message = 'This email is not registered. Create an account at the /register route')
                        if not check_password_hash(self.__udata['werkzeug_token'], self.__login_json['token']):
                            abort(403, message = 'Unauthorized token')
                        self.__JWT: str = jwt_heart.get_token(int(self.__udata['id']))
            except Exception as err:
                abort(500, message = f'Internal Server Error: {err}')
            
            return {'message': f'You can use this token to access the main endpoints during the next: {datetime.timedelta(minutes = int(os.getenv('EXP_TIME_MIN')))}',
                    'access_token': self.__JWT}, 200
    
    class Searcher(Resource):

        def get(self) -> Tuple[Dict[str, Any], int]:
            self.__uid, self.__rt = auth_jwt()
            self.__creator: str | None = request.args.get('creator', type = str)
            self.__title: str | None = request.args.get('title', type = str)

            if self.__title is None or self.__creator is None:
                abort(400, message = 'You must provide the \'creator\' and \'title\' parameters')
            
            self.__ovr_data: Dict[str, Any] = run(requester_sgt.fetch_all(self.__title)) #Searching with title from web apis
            #Dirty data:
            self.__dbooks: Dict[str, Any] = self.__ovr_data['books']
            self.__dgames: List[Dict[str, Any]] = self.__ovr_data['games']
            self.__dmovies: Dict[str, Any] | None = self.__ovr_data['movies']
            self.__dsongs: Dict[str, Any] = self.__ovr_data['songs']
            #Organized data:
            self.__books: List[str] = Extractor.extract_book_data(self.__dbooks)
            self.__games: List[str] = Extractor.extract_game_data(self.__dgames)
            self.__movies: str | None = Extractor.extract_movie_data(self.__dmovies)
            self.__songs: List[str] = Extractor.extract_song_data(self.__dsongs)
            #Organized documents
            self.__doc_books: List[str] = [text.replace('@', ' ') for text in self.__books] #format of the items will be 'author title'
            self.__doc_games: List[str] = self.__games # Just titles
            self.__doc_movies: None | str = None if self.__movies is None else self.__movies.replace('@', ' ') #format of the items will be 'author title'
            self.__doc_songs: List[str] = [text.replace('@', ' ') for text in self.__songs] #format of the items will be author 'title'
            #Getting similar documents in the format "author title" or just 'title' for the 'games' field
            self.__df_books: List[Dict[str, str | float ]] = DocumentFilter(' '.join([self.__creator, self.__title]),
                                            docs = self.__doc_books).similar_docs
            if self.__movies is not None:
                self.__df_movies: List[Dict[str, str | float ]] = DocumentFilter(' '.join([self.__creator, self.__title]),
                                            docs = [
                                                self.__doc_movies
                                            ], precision = 0.5).similar_docs
            else:
                self.__df_movies: None = None
            self.__df_songs: List[Dict[str, str | float ]] = DocumentFilter(' '.join([self.__creator, self.__title]),
                                            docs = self.__doc_songs).similar_docs
            self.__df_games: List[Dict[str, str | float ]] = DocumentFilter(self.__title,
                                            docs = self.__doc_games).similar_docs
            #Inserting data on the database.
            CONN: Connection = Connection()
            for book in self.__df_books:
                for at_book in self.__books:
                    if book['doc'] == at_book.replace('@', ' '):
                        self.__parts: List[str] = at_book.split('@')
                        self.__author: str = self.__parts[0]
                        self.__title: str = self.__parts[1]
                        with CONN.StrongConnection(
                            user = os.getenv('MYSQL_USER'),
                            password = os.getenv('MYSQL_PW'),
                            database = os.getenv('DATABASE_NAME')
                        ) as cnx:
                            with CONN.CursorManager(cnx) as cursor:
                                DataBaseManager.load_books(
                                    cnx=cnx,
                                    cursor=cursor,
                                    uid=self.__uid,
                                    author=self.__author,
                                    title=self.__title,
                                    sim_coef=book['cos']
                                )
            for song in self.__df_songs:
                for at_song in self.__songs:
                    if song['doc'] == at_song.replace('@', ' '):
                        self.__parts: List[str] = at_song.split('@')
                        self.__artist: str = self.__parts[0]
                        self.__track: str = self.__parts[1]
                        with CONN.StrongConnection(
                            user = os.getenv('MYSQL_USER'),
                            password = os.getenv('MYSQL_PW'),
                            database = os.getenv('DATABASE_NAME')
                        ) as cnx:
                            with CONN.CursorManager(cnx) as cursor:
                                DataBaseManager.load_songs(
                                    cnx=cnx,
                                    cursor=cursor,
                                    uid=self.__uid,
                                    track=self.__track,
                                    artist=self.__artist,
                                    sim_coef=song['cos']
                                )
            #Querying ranked data for each one of the three media tables.
            for game in self.__df_games:
                with CONN.StrongConnection(
                    user = os.getenv('MYSQL_USER'),
                    password = os.getenv('MYSQL_PW'),
                    database = os.getenv('DATABASE_NAME')
                    ) as cnx:
                    with CONN.CursorManager(cnx) as cursor:
                        DataBaseManager.load_games(
                                cnx=cnx,
                                cursor=cursor,
                                uid=self.__uid,
                                title=game['doc'],
                                sim_coef=game['cos']
                            )
            with CONN.StrongConnection(
                user = os.getenv('MYSQL_USER'),
                password = os.getenv('MYSQL_PW'),
                database = os.getenv('DATABASE_NAME')
                ) as cnx:
                with CONN.CursorManager(cnx) as cursor:
                    self.__ranked_books: List[Dict[str, str | float]] = QueryBuilder.get_ranked_data(cursor, uid = self.__uid, table_name = os.getenv('BOOK_TABLE'))
                    self.__ranked_songs: List[Dict[str, str | float]] = QueryBuilder.get_ranked_data(cursor, uid = self.__uid, table_name = os.getenv('SONG_TABLE'))
                    self.__ranked_games: List[Dict[str, str | float]] = QueryBuilder.get_ranked_data(cursor, uid = self.__uid, table_name = os.getenv('GAME_TABLE'))
            
            #Removing data requested by the user from MySQL
            for table in (os.getenv('SONG_TABLE'), os.getenv('GAME_TABLE'), os.getenv('BOOK_TABLE')):
                with CONN.StrongConnection(
                    user = os.getenv('MYSQL_USER'),
                    password = os.getenv('MYSQL_PW'),
                    database = os.getenv('DATABASE_NAME')
                    ) as cnx:
                    with CONN.CursorManager(cnx) as cursor:
                        DataBaseManager.rm_media(cursor, cnx, uid = self.__uid, table_name=table)
            
            #Getting the data of the books that have been chosen by TF-IDF.
            #Searching the ranked data inside the JSON given by the google api
            self.__info_books: List[Dict[str, Any]] = list()
            self.__items_books: List[Dict[str, Any]] = self.__dbooks['items']
            for book in self.__ranked_books:
                for external_book in self.__items_books:
                    if external_book['volumeInfo']['title'].upper() == book['title'] and external_book['volumeInfo']['authors'][0].upper() == book['author']:
                        self.__internal_book: Dict[str, Any] = {}
                        for field in ('title', 'subtitle', 'authors', 'categories', 'description', 'pageCount', 'publisher', 'publishedDate'):
                            try:
                                self.__internal_book.update({field : external_book['volumeInfo'][field]})
                            except KeyError:
                                self.__internal_book.update({field : None})
                        self.__info_books.append(self.__internal_book)
            #Searching the ranked data inside the JSON given by the last.fm api
            self.__info_songs: List[Dict[str, Any]] = list()
            self.__items_songs: List[Dict[str, Any]] = self.__dsongs['results']['trackmatches']['track']
            for song in self.__ranked_songs:
                for external_song in self.__items_songs:
                    if external_song['name'].upper() == song['title'] and external_song['artist'].upper() == song['author']:
                        self.__internal_song: Dict[str, Any] = {}
                        for field in ('name', 'artist', 'listeners', 'url'):
                            try:
                                self.__internal_song.update({field : external_song[field]})
                            except KeyError:
                                self.__internal_song.update({field : None})
                        self.__info_songs.append(self.__internal_song)

            #Searching the ranked data inside the JSON given by the OMDB api
            if self.__df_movies is None:
                self.__info_movies: None = None
            else:
                if bool(self.__df_movies):
                    self.__adjust_emptiness: Callable[[str], None | str] = lambda data : data if data != 'N/A' else None
                    self.__info_movies: Dict[str, str | None] = {
                        'title': self.__adjust_emptiness(self.__dmovies['Title']),
                        'actors': self.__adjust_emptiness(self.__dmovies['Actors']),
                        'awards': self.__adjust_emptiness(self.__dmovies['Awards']),
                        'release_date': self.__adjust_emptiness(self.__dmovies['Released']),
                        'runtime': self.__adjust_emptiness(self.__dmovies['Runtime']),
                        'description': self.__adjust_emptiness(self.__dmovies['Plot']),
                        'metascore': self.__adjust_emptiness(int(self.__dmovies['Metascore'])),
                        'genre': self.__adjust_emptiness(self.__dmovies['Genre'])
                        }
                else:
                    self.__info_movies: None = None
            #Searching the ranked data inside the JSON given by the twitch api
            self.__info_games: List[Dict[str, str]] = list()
            for game in self.__ranked_games:
                self.__game_title: str = game['title']
                for ext_game in self.__dgames:
                    if ext_game['name'].upper() == self.__game_title:
                        self.__info_games.append(
                            {
                                'name': ext_game['name'],
                                'summary': ext_game['summary']
                            }
                            )
                        break
            #Returning the final JSON
            return {
                'movies': self.__info_movies,
                'songs': self.__info_songs,
                'games': self.__info_games,
                'books': self.__info_books,
                'exp_remaining_time': self.__rt
            }, 200