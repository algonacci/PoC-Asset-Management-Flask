import os
from flask_httpauth import HTTPTokenAuth

secret_key = os.getenv("SECRET_KEY", "secret")
print(secret_key)

auth = HTTPTokenAuth(scheme="Bearer")


@auth.error_handler
def unauthorized():
    print(secret_key)
    return {
        "status": {
            "code": 401,
            "message": "Unauthorized Access!"
        },
        "data": None,
    }, 401


@auth.verify_token
def verify_token(token):
    return secret_key == token
