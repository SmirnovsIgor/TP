import pytest

from apps.users.tests.factories.users import UserFactory
from pytest_factoryboy import register
from rest_auth.models import TokenModel

token_model = TokenModel
register(UserFactory, 'user')
register(UserFactory, 'staff')


@pytest.fixture
def token(staff):
    token, _ = token_model.objects.get_or_create(user=staff)
    return token
