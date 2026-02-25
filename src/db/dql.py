from mysql.connector import CMySQLConnection, MySQLConnection
from typing import Dict, List, Tuple, Any
import os

class QueryBuilder:

    @staticmethod
    def get_user_by_email(cursor: Any,
                        email: str) -> Dict[str, int | str] | None:
        cursor.execute("SELECT id, user_token FROM users WHERE email = %s", (email,))
        data: List[Tuple[int, str]] = cursor.fetchall()
        if len(data) == 0:
            return None #None means that this email isn't present inside the database.
        return {
                'id': data[0][0],
                'werkzeug_token': data[0][1]
                } #Real id and token of the user with such email
    
    @staticmethod
    def get_ranked_data(cursor: Any,
                        uid: int,
                        table_name: str,
                        limit_val: int = 5) -> List[Dict[str, str | float]]:
        #Detail: all resource tables must have title columns and similarity_coef
        if table_name == 'games':
            sql = f"""
                    SELECT
                        {os.getenv('TITLE')}, similarity_coef
                    FROM
                        {table_name}
                    WHERE
                        uid = {uid}
                    ORDER BY
                        similarity_coef DESC
                    LIMIT {limit_val}
                """
        else:
            sql = f"""
                    SELECT
                        {os.getenv('TITLE')}, {os.getenv('AUTHOR')}, similarity_coef
                    FROM
                        {table_name}
                    WHERE
                        uid = {uid}
                    ORDER BY
                        similarity_coef DESC
                    LIMIT {limit_val}
                """
        cursor.execute(sql)
        ranked_dataset: List[Tuple[str, float]] = cursor.fetchall()
        if table_name != "games":
            ogn_rkd_ds: List[Dict[str, str | float]] = [
                        {
                        'title': ranked_dataset[pos][0],
                        'author': ranked_dataset[pos][1],
                        'coef': ranked_dataset[pos][2]
                        } for pos in range(len(ranked_dataset))
                    ]
        else:
            ogn_rkd_ds: List[Dict[str, str | float]] = [
                        {
                        'title': ranked_dataset[pos][0],
                        'coef': ranked_dataset[pos][1]
                        } for pos in range(len(ranked_dataset))
                    ]
        return ogn_rkd_ds