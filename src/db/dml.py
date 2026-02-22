from mysql.connector import CMySQLConnection, MySQLConnection, MySQLCursor
from numpy import float64

class DataBaseManager:

    @staticmethod
    def load_books(cursor: MySQLCursor,
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
    def load_songs(cursor: MySQLCursor,
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
    def load_movies(cursor: MySQLCursor,
                    cnx: CMySQLConnection | MySQLConnection,
                    uid: int,
                    title: str,
                    director: str,
                    sim_coef: float | float64) -> None:
        cursor.execute(
            """
                INSERT INTO movies (uid, title, director, similarity_coef)
                VALUES (%s, %s, %s, %s)
            """, (uid, title, director, sim_coef)
            )
        cnx.commit()
    
    @staticmethod
    def load_games(cursor: MySQLCursor,
                   cnx: CMySQLConnection | MySQLConnection,
                   uid: int,
                   title: str,
                   sim_coef: float | float64) -> None:
        cursor.execute(
            """
                INSERT INTO games (uid, title, similarity_coef)
                VALUES (%s, %s, %s, %s)
            """, (uid, title, sim_coef))
        cnx.commit()