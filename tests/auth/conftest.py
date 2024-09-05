import pytest


@pytest.fixture
def user_data_register() -> dict:
    return {
        'username': 'king',
        'email': 'king@fortress.com',
        'first_name': 'King',
        'last_name': 'Pirates',
        'hashed_password': 'king123',
    }


@pytest.fixture
def user_data_login() -> dict:
    return {
        'username': 'king',
        'password': 'king123',
        'grand_type': 'password',
    }
