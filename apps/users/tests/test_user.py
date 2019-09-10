import pytest
from apps.users.tests.factories.users import UserFactory
from pytest_factoryboy import register
from rest_auth.models import TokenModel

token_model = TokenModel
register(UserFactory, 'user')


@pytest.fixture
def token(user):
    token, _ = token_model.objects.get_or_create(user=user)
    return token


@pytest.mark.django_db
class TestUsers:
    def test_self_details(self, client, user, token):
        """
        test user self details
            * check basic structure
            * check for authorized/not authorized users
        """
        response = client.get('/api/user/me/', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert response.status_code == 200
        response_dict = response.json()
        assert response_dict.get('username')
        assert response_dict.get('email')
        assert response_dict.get('id')
        assert response_dict.get('created')
        assert response_dict.get('updated')
        assert response_dict.get('first_name')
        assert response_dict.get('last_name')
        assert response_dict.get('date_of_birth')
        assert response_dict.get('password') is None
        assert response_dict.get('is_staff') is False
        assert response_dict.get('is_active') is True
        assert response_dict.get('profile_image') is None

