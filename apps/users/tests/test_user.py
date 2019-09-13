import pytest
import iso8601
from datetime import datetime


@pytest.mark.django_db
class TestUsers:
    """test user self details

    * check for valid data
    * check for authorized/not authorized users
    """
    def test_self_details_authorized_true(self, client, request_user, token):
        response = client.get('/api/user/me/', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert response.status_code == 200
        response_dict = response.json()
        assert response_dict.get('username') == request_user.username
        assert response_dict.get('email') == request_user.email
        assert response_dict.get('id') == str(request_user.id)
        assert iso8601.parse_date(response_dict.get('created')) == request_user.created
        assert iso8601.parse_date(response_dict.get('updated')) == request_user.updated
        assert response_dict.get('first_name') == request_user.first_name
        assert response_dict.get('last_name') == request_user.last_name
        assert datetime.strptime(response_dict.get('date_of_birth'), '%Y-%m-%d').date() == request_user.date_of_birth
        assert response_dict.get('password') is None
        assert response_dict.get('is_staff') is False
        assert response_dict.get('is_active') is True
        assert response_dict.get('profile_image') is None

    def test_self_details_authorized_false(self, client):
        response = client.get('/api/user/me/')
        assert response.status_code == 401

