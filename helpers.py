from hashlib import sha256

def hash_password(text):
    return sha256((text).encode('utf-8')).hexdigest()