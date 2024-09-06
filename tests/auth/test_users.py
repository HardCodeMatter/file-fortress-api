from httpx import AsyncClient


class TestUsers:
    async def test_get_user_by_username(self, async_client: AsyncClient, user_data_register: dict, user_data_login: dict):
        response = await async_client.post(
            '/auth/register',
            json=user_data_register,
        )

        assert response.status_code == 201

        response = await async_client.post(
            '/auth/login',
            data=user_data_login,
        )

        assert response.status_code == 200
        assert 'access_token' in response.json()
        assert 'refresh_token' in response.json()
        assert 'token_type' in response.json()

        response = await async_client.get(
            '/users',
            params={'username': 'king'},
        )

        assert response.status_code == 200
        assert response.json()['username'] == 'king'

        response = await async_client.get(
            '/users',
            params={'username': 'royal'},
        )

        assert response.status_code == 404
        assert response.json()['detail'] == 'User not found.'

    async def test_user_password_validation(self, async_client: AsyncClient, user_password_validation_list: list):
        for data, expected_status, expected_detail in user_password_validation_list:
            response = await async_client.post(
                '/auth/register',
                json=data,
            )

            assert response.status_code == expected_status

            if 'detail' in response.json():
                assert response.json()['detail'] == expected_detail

    async def test_user_name_validation(self, async_client: AsyncClient, user_name_validation_list: list):
        for data, expected_status, expected_detail in user_name_validation_list:
            response = await async_client.post(
                '/auth/register',
                json=data,
            )

            assert response.status_code == expected_status

            if 'detail' in response.json():
                assert response.json()['detail'] == expected_detail
