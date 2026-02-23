import jwt
import datetime
from typing import Dict, Any

class JwtGenerator:

    def __init__(self, sec_key: str, algorithm: str, exp_time_min: int):
        self.__sec_key: str = sec_key
        self.__alg: str = algorithm
        self.__exp_time_min: int = exp_time_min
    
    def __create_token(self, uid: int) -> str:
        self.__jwt: str = jwt.encode(
            {
                'uid': uid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = self.__exp_time_min)
            }, key = self.__sec_key, algorithm = self.__alg
        )
        return self.__jwt #Creating a token

    def get_token(self, uid: int) -> str:
        return self.__create_token(uid)

    def refresh_token(self, token: str, max_time_min: int = 15) -> str:
        self.__payload: Dict[str, Any] = jwt.decode(
            jwt = token,
            key = self.__sec_key,
            algorithms = self.__alg
        ) #Extracting payload
        if datetime.datetime.utcfromtimestamp(self.__payload['exp']) - datetime.datetime.utcnow() < datetime.timedelta(minutes = max_time_min):
            return self.__create_token(self.__payload['uid']) #Return a new token if expiration is near
        return token #Return the token if the expiration will take a lot of minutes