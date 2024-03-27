import argon2.exceptions
from argon2 import PasswordHasher

ph = PasswordHasher()


async def hash_password(password: str):
    hash_password = ph.hash(password)
    print(hash_password)
    return hash_password


async def verify_hashed_password(password: str, hashed_password: str):
    try:
        is_password_valid = ph.verify(hashed_password, password)
        print(is_password_valid)
        return is_password_valid
    except argon2.exceptions.VerifyMismatchError:
        return False
