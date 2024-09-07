from httpx import AsyncClient

from tests.auth.conftest import user_data_login


class TestAuthRegister:
    async def test_user_register(self, async_client: AsyncClient):
        user_data = {
            "username": "glitch",
            "email": "glitch@fortress.com",
            "first_name": "Glitch",
            "last_name": "Developer",
            "hashed_password": "glitch123"
        }

        response = await async_client.post(
            '/auth/register',
            json=user_data,
        )

        assert response.status_code == 201
        assert response.json()['username'] == 'glitch'
        assert response.json()['email'] == 'glitch@fortress.com'

    async def test_user_register_with_unique_username(self, async_client: AsyncClient):
        user_data = {
            "username": "david",
            "email": "david@fortress.com",
            "first_name": "David",
            "last_name": "Peterson",
            "hashed_password": "david123"
        }

        response = await async_client.post('/auth/register', json=user_data)

        assert response.status_code == 201
        assert response.json()['username'] == 'david'

        user_data = {
            "username": "david",
            "email": "monarch@fortress.com",
            "first_name": "Mike",
            "last_name": "Monarch",
            "hashed_password": "mike123"
        }

        response = await async_client.post('/auth/register', json=user_data)

        assert response.status_code == 409
        assert response.json()['detail'] == "User with this username is already exist."

    async def test_user_register_with_unique_email(self, async_client: AsyncClient):
        user_data = {
            "username": "jordan",
            "email": "jordan@fortress.com",
            "first_name": "Jordan",
            "last_name": "Hunter",
            "hashed_password": "jordan123"
        }

        response = await async_client.post('/auth/register', json=user_data)

        assert response.status_code == 201
        assert response.json()['username'] == 'jordan'
        assert response.json()['email'] == 'jordan@fortress.com'

        user_data = {
            "username": "rodger",
            "email": "jordan@fortress.com",
            "first_name": "Rodger",
            "last_name": "Rodger",
            "hashed_password": "rodger123"
        }

        response = await async_client.post('/auth/register', json=user_data)

        assert response.status_code == 409
        assert response.json()['detail'] == "User with this email is already exist."


class TestAuthLogin:
    async def test_user_login(self, async_client: AsyncClient):
        user_data = {
            "username": "master",
            "email": "master@fortress.com",
            "first_name": "Master",
            "last_name": "Python",
            "hashed_password": "master123",
        }

        response = await async_client.post(
            '/auth/register',
            json=user_data,
        )

        assert response.status_code == 201
        assert response.json()['username'] == 'master'

        user_data = {
            "username": "master",
            "password": "master123",
            "grand_type": "password",
        }

        response = await async_client.post(
            '/auth/login',
            data=user_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )

        assert response.status_code == 200
        assert 'access_token' in response.json()
        assert 'refresh_token' in response.json()
        assert 'token_type' in response.json()

    async def test_user_login_with_wrong_username(self, async_client: AsyncClient):
        user_data = {
            'username': 'roman',
            'password': 'roman123',
            'grand_type': 'password',
        }

        response = await async_client.post(
            '/auth/login',
            data=user_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )

        assert response.status_code == 401
        assert response.json()['detail'] == 'Incorrect username or password.'

    async def test_user_login_with_wrong_password(self, async_client: AsyncClient):
        user_data = {
            "username": "king",
            "email": "king@fortress.com",
            "first_name": "King",
            "last_name": "Pirates",
            "hashed_password": "king123",
        }

        response = await async_client.post(
            '/auth/register',
            json=user_data,
        )

        assert response.status_code == 201
        assert response.json()['username'] == 'king'

        user_data = {
            'username': 'king',
            'password': 'kingsman',
            'grand_type': 'password',
        }

        response = await async_client.post(
            '/auth/login',
            data=user_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )

        assert response.status_code == 401
        assert response.json()['detail'] == 'Incorrect username or password.'

    async def test_change_user_password(self, async_client: AsyncClient, user_data_register: dict, user_data_login: dict, user_new_password_list: list):
        response = await async_client.post(
            '/auth/register',
            json=user_data_register,
        )

        assert response.status_code == 201

        response = await async_client.post(
            '/auth/login',
            data=user_data_login,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )

        assert response.status_code == 200
        assert 'access_token' in response.json()
        assert 'refresh_token' in response.json()

        for old_password, new_password, expected_status, expected_detail in user_new_password_list:
            response = await async_client.post(
                '/auth/change-password',
                json={
                    'old_password': old_password if old_password else user_data_login['password'],
                    'new_password': new_password,
                },
            )

            assert response.status_code == expected_status
            assert response.json()['detail'] == expected_detail
