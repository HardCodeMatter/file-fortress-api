import random
import string


def generate_hash(length: int = 6) -> str:
    if length < 3:
        raise ValueError('Length must be at least 3.')

    characters = string.ascii_uppercase + string.digits

    return ''.join([random.choice(characters) for _ in characters])
