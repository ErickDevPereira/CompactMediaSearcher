from flask_restful import Resource, abort, reqparse, Api
from flask import request, Flask
from werkzeug.security import check_password_hash, generate_password_hash
from typing import Dict, Tuple, Any
from src.db.dml import DataBaseManager
from src.db.ddl import Connection
import os
from mysql.connector.errors import IntegrityError
from src.custom_error import LackingCredentialError

class HTTP:

    app: Flask = Flask(__name__)
    api: Api = Api(app)
    user_args: Any = reqparse.RequestParser()

    @classmethod
    def __set_rsrc(cls) -> None:
        cls.user_args.add_argument('first_name', type = str, help = 'problem at \'first_name\' field')
        cls.user_args.add_argument('last_name', type = str, help = 'problem at the \'last_name\' field')
        cls.user_args.add_argument('email', type = str, help = 'problem at \'email\' field')
        cls.api.add_resource(cls.Register, '/register')
    
    @classmethod
    def start_server(cls) -> None:
        cls.__set_rsrc()
        cls.app.run(debug = True)

    class Register(Resource):

        def post(self):

            self.new_user_data: Dict[str, str] = HTTP.user_args.parse_args()
            self.__fields: Tuple[str, ...] = ('first_name', 'last_name', 'email')

            for field in self.__fields:
                if self.new_user_data[field] is None:
                    abort(400, message = f'Problem >> you must fill the field "{field}"')
            
            self.__mysql_user: str | None= os.getenv('MYSQL_USER')
            self.__mysql_pw: str | None = os.getenv('MYSQL_PW')
            self.__mysql_db: str | None = 'media_searcher'

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