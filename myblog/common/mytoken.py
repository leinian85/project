import hashlib
import jwt
import time
import common.config as cnf


def pwd(password):
    hs = hashlib.md5()
    hs.update(password.encode())
    return hs.hexdigest()


def token(username):
    payload = {"username": username, "exp": time.time() + 3000}
    token = jwt.encode(payload=payload, key=cnf.key, algorithm="HS256")
    return token.decode()


def username_for_token(token):
    payload = jwt.decode(token, key=cnf.key, algorithm="HS256")
    return payload["username"]

