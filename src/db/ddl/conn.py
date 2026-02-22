from mysql.connector import connect as cnx, CMySQLConnection, MySQLConnection, MySQLCursor

class Connecion:

    #Context Manager used to connect with MySQL server, not with a database.
    class WeakConnection:

        def __init__(self, user: str, password: str):
            self.__user: str = user
            self.__password: str = password
        
        def __enter__(self) -> CMySQLConnection | MySQLConnection:
            self.__cnx: CMySQLConnection | MySQLConnection = cnx(
                host = 'localhost',
                user = self.__user,
                password = self.__password
            )
            return self.__cnx
        
        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.__cnx.close()
    
    #Context Manager used to connect with a specific database inside MySQL.
    class StrongConnection:

        def __init__(self, user: str, password: str, database: str):
            self.__user: str = user
            self.__password: str = password
            self.__database: str = database
        
        def __enter__(self) -> CMySQLConnection | MySQLConnection:
            self.__cnx: CMySQLConnection | MySQLConnection = cnx(
                host = 'localhost',
                user = self.__user,
                password = self.__password,
                database = self.__database
            )
            return self.__cnx

        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.__cnx.close()

    class CursorManager:

        def __init__(self, cnx: CMySQLConnection | MySQLConnection):
            self.__cnx: CMySQLConnection | MySQLConnection = cnx
        
        def __enter__(self) -> MySQLCursor:
            self.__cursor: MySQLCursor = self.__cnx.cursor()
            return self.__cursor
        
        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.__cursor.close()