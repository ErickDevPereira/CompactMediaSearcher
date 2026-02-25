from .conn import Connection
from mysql.connector.errors import ProgrammingError
import os

class DataBase:

    @staticmethod
    def automate_db(user: str, password: str, database: str = 'media_searcher') -> None:
        CONN: Connection = Connection()
        #Creating the database
        with CONN.WeakConnection(
            user = user,
            password = password
        ) as wcnx:
            with CONN.CursorManager(wcnx) as cursor:
                cursor.execute(
                    f'CREATE DATABASE IF NOT EXISTS {database}'
                )
        #Creating the tables
        with CONN.StrongConnection(
            user = user,
            password = password,
            database = database
        ) as scnx:
            with CONN.CursorManager(scnx) as cursor:
                cursor.execute(
                                """
                                CREATE TABLE IF NOT EXISTS users (
                                    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                                    user_token VARCHAR(500) NOT NULL,
                                    fname VARCHAR(50) NOT NULL,
                                    lname VARCHAR(50) NOT NULL,
                                    email VARCHAR(50) NOT NULL,
                                    CONSTRAINT uemail UNIQUE(email),
                                    CONSTRAINT auth_email CHECK( email LIKE '%_@_%.com' )
                                )
                                """
                               )
            #Detail: all resource tables must have title columns and similarity_coef
            #This idea will be used inside the dql.py file.
            with CONN.CursorManager(scnx) as cursor:
                cursor.execute(
                                f"""
                                CREATE TABLE IF NOT EXISTS {os.getenv('BOOK_TABLE')} (
                                    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                                    uid INT UNSIGNED NOT NULL,
                                    {os.getenv('TITLE')} VARCHAR(200) NOT NULL,
                                    {os.getenv('AUTHOR')} VARCHAR(100) NOT NULL,
                                    similarity_coef DECIMAL(5, 4) NOT NULL,
                                    FOREIGN KEY(uid) REFERENCES users(id)
                                )
                                """
                               )
            with CONN.CursorManager(scnx) as cursor:
                cursor.execute(
                                f"""
                                CREATE TABLE IF NOT EXISTS {os.getenv('SONG_TABLE')} (
                                    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                                    uid INT UNSIGNED NOT NULL,
                                    {os.getenv('TITLE')} VARCHAR(200) NOT NULL,
                                    {os.getenv('AUTHOR')} VARCHAR(100) NOT NULL,
                                    similarity_coef DECIMAL(5, 4) NOT NULL,
                                    FOREIGN KEY(uid) REFERENCES users(id)
                                )
                                """
                               )
            with CONN.CursorManager(scnx) as cursor:
                cursor.execute(
                                f"""
                                CREATE TABLE IF NOT EXISTS {os.getenv('GAME_TABLE')} (
                                    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                                    uid INT UNSIGNED NOT NULL,
                                    {os.getenv('TITLE')} VARCHAR(200) NOT NULL,
                                    similarity_coef DECIMAL(5, 4) NOT NULL,
                                    FOREIGN KEY(uid) REFERENCES users(id)
                                )
                                """
                               )
            #Creating the indexes
            for media in (os.getenv('BOOK_TABLE'), os.getenv('SONG_TABLE'), os.getenv('GAME_TABLE')):
                with CONN.CursorManager(scnx) as cursor:
                    try:
                        cursor.execute(f'CREATE INDEX token_ind_{media} ON {media}(user_token)')
                    except ProgrammingError:
                        pass #It means that the index already exists