from mysql.connector import CMySQLConnection, MySQLConnection
from typing import Any
from numpy import float64

class DataBaseManager:

    @staticmethod
    def load_users(cursor: Any,
                   cnx: CMySQLConnection | MySQLConnection,
                   token: str,
                   fname: str,
                   lname: str,
                   email: str) -> None:
        cursor.execute(
                """
                    INSERT INTO users (user_token, fname, lname, email)
                    VALUES (%s, %s, %s, %s)
                """, (token, fname, lname, email)
                )
        cnx.commit()

    @staticmethod
    def load_books(cursor: Any,
                   cnx: CMySQLConnection | MySQLConnection,
                   uid: int,
                   title: str,
                   author: str,
                   sim_coef: float | float64) -> None:
        cursor.execute(
                """
                    INSERT INTO books (uid, title, author, similarity_coef)
                    VALUES (%s, %s, %s, %s)
                """, (uid, title, author, sim_coef)
                )
        cnx.commit()
    
    @staticmethod
    def load_songs(cursor: Any,
                    cnx: CMySQLConnection | MySQLConnection,
                    uid: int,
                    track: str,
                    artist: str,
                    sim_coef: float | float64) -> None:
        cursor.execute(
            """
                INSERT INTO songs (uid, track, artist, similarity_coef)
                VALUES (%s, %s, %s, %s)
            """, (uid, track, artist, sim_coef)
            )
        cnx.commit()
    
    @staticmethod
    def load_games(cursor: Any,
                   cnx: CMySQLConnection | MySQLConnection,
                   uid: int,
                   title: str,
                   sim_coef: float | float64) -> None:
        cursor.execute(
            """
                INSERT INTO games (uid, title, similarity_coef)
                VALUES (%s, %s, %s)
            """, (uid, title, sim_coef))
        cnx.commit()