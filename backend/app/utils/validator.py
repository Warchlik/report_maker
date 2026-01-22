from passlib.context import CryptContext


context = CryptContext(schemes=["bcript"], deprecated="auto")


def hash_value(value: str) -> str:
    return context.hash(value)


def validate_hashed_value(value: str, value_hash: str) -> bool:
    return context.verify(secret=value, hash=value_hash)
