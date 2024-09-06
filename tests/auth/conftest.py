import pytest

from auth.schemas import UserCreate


@pytest.fixture
def user_data_register() -> dict:
    return {
        'username': 'king',
        'email': 'king@fortress.com',
        'first_name': 'King',
        'last_name': 'Pirates',
        'hashed_password': 'King1234',
    }


@pytest.fixture
def user_data_login() -> dict:
    return {
        'username': 'king',
        'password': 'King1234',
        'grand_type': 'password',
    }


@pytest.fixture
def user_password_validation_list(limit: int = 10) -> list[tuple[dict, int | None, str | None]]:
    users: list[tuple[dict, int | None, str | None]] = [
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "Developer", "hashed_password": "Clo wn 228"}, 400, 'Password cannot contain spaces.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "Developer", "hashed_password": ""}, 400, 'Password must be between 8 and 32 characters in length, inclusive.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "Developer", "hashed_password": "master"}, 400, 'Password must be between 8 and 32 characters in length, inclusive.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "Developer", "hashed_password": "124"}, 400, 'Password must be between 8 and 32 characters in length, inclusive.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "Developer", "hashed_password": "password123password123password123"}, 400, 'Password must be between 8 and 32 characters in length, inclusive.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "Developer", "hashed_password": "fortress"}, 400, 'Password must contain at least one uppercase letter, one lowercase letter, and one number.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "Developer", "hashed_password": "12345678"}, 400, 'Password must contain at least one uppercase letter, one lowercase letter, and one number.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "Developer", "hashed_password": "password123"}, 400, 'Password must contain at least one uppercase letter, one lowercase letter, and one number.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "Developer", "hashed_password": "Password123"}, 201, None),
        ({"username": "justice", "email": "justice@fortress.com", "first_name": "Justice", "last_name": "Minister", "hashed_password": "1pASSWRD"}, 201, None),
    ]

    return users[:limit]


@pytest.fixture
def user_name_validation_list(limit: int = 10) -> list[tuple[dict, int | None, str | None]]:
    users: list[tuple[dict, int | None, str | None]] = [
        ({"username": "master", "email": "master@fortress.com", "first_name": "123456", "last_name": "Developer", "hashed_password": "Password123"}, 400, 'Name must only contain letters.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "123456", "hashed_password": "Password123"}, 400, 'Name must only contain letters.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master1", "last_name": "Developer", "hashed_password": "Password123"}, 400, 'Name must only contain letters.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "Developer2", "hashed_password": "Password123"}, 400, 'Name must only contain letters.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "", "last_name": "Developer", "hashed_password": "Password123"}, 400, 'Name must be between 2 and 30 characters in length, inclusive.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "", "hashed_password": "Password123"}, 400, 'Name must be between 2 and 30 characters in length, inclusive.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master Dangerous Magnetic Touristico", "last_name": "Developer", "hashed_password": "Password123"}, 400, 'Name must be between 2 and 30 characters in length, inclusive.'),
        ({"username": "master", "email": "master@fortress.com", "first_name": "Master", "last_name": "Developer", "hashed_password": "Password123"}, 201, None),
    ]

    return users[:limit]
