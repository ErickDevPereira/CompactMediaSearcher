from flask_restful import Resource, abort, reqparse, Api
from flask import request, Flask
from werkzeug.security import check_password_hash, generate_password_hash
from typing import Dict, Tuple, Any, Callable
from src.db.dml import DataBaseManager
from src.db.ddl import Connection
import os
from mysql.connector.errors import IntegrityError
from src.custom_error import LackingCredentialError
from src.db.dql import QueryBuilder
from src.api.jwt.singleton import jwt_heart
import datetime

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
                    }, 200
    
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
