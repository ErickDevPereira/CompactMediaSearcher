from mysql.connector import CMySQLConnection, MySQLConnection, MySQLCursor
from typing import Dict, List, Tuple

class QueryBuilder:

    @staticmethod
    def get_user_by_email(cursor: MySQLCursor,
                        email: str) -> Dict[str, int | str]:
        cursor.execute("SELECT id, user_token FROM users WHERE email = %s", (email,))
        data: List[Tuple[int, str]] = cursor.fetchall()
        if len(data) == 0:
            return None #None means that this email isn't present inside the database.
        return {
                'id': data[0][0],
                'werkzeug_token': data[0][1]
                } #Real id and token of the user with such email
    
    @staticmethod
    def get_ranked_data(cursor: MySQLCursor,
                        uid: int,
                        table_name: str) -> List[Dict[str, str | float]]:
        #Detail: all resource tables must have title columns and similarity_coef
        cursor.execute("""
                            SELECT
                                title, similarity_coef
                            FROM
                                %s
                            WHERE
                                uid = %s
                            ORDER BY
                                similarity_coef DESC
                        """)
        ranked_dataset: List[Tuple[str, float]] = cursor.fetchall()
        ogn_rkd_ds: List[Dict[str, str | float]] = [
                    {
                    'title': ranked_dataset[pos][0],
                    'coef': ranked_dataset[pos][1]
                    } for pos in range(len(ranked_dataset))
                ]
        return ogn_rkd_ds