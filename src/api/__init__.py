from .endpoints import HTTP
import os

from src.db.ddl import DataBase
DataBase.automate_db(
    user = os.getenv('MYSQL_USER'),
    password = os.getenv('MYSQL_PW')
    )