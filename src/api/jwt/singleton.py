from .gen_jwt import JwtGenerator
import os

jwt_heart: JwtGenerator = JwtGenerator(
    sec_key = os.getenv('SECRET_KEY_JWT'),
    algorithm = os.getenv('ALGORITHM'),
    exp_time_min = int(os.getenv('EXP_TIME_MIN'))
)