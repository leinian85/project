import hashlib

def pwd(password):
    hs = hashlib.md5()
    hs.update(password.encode())
    return hs.hexdigest()