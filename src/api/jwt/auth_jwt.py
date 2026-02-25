import jwt
from flask import request
from flask_restful import abort
import os
import datetime
from typing import Any, Dict, Tuple

def auth_jwt() -> Tuple[int, str]:
    token: str | None = request.headers.get('X-Access-Token')
    if token is None:
        abort(400, message = 'The token must be given to the \'X-Access-Token\' field inside the header')

    try:
        payload: Dict[str, Any] = jwt.decode(token,
                                            key = os.getenv('SECRET_KEY_JWT'),
                                            algorithms = os.getenv('ALGORITHM'))
    except jwt.ExpiredSignatureError:
        abort(403, message = 'Unauthorized access: your token has expired. Go to the GET /login endpoint to obtain a new one')
    except jwt.InvalidSignatureError:
        abort(403, message = 'Unauthorized access: your token is malformed')
    except Exception as err:
        abort(500, message = f'Internal Server Error: {err}')
    else:
        uid: int = int(payload['uid'])
        remaining_time: str = str(datetime.datetime.utcfromtimestamp(payload['exp']) - datetime.datetime.utcnow())
        return uid, remaining_time