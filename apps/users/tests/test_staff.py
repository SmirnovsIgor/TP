from datetime import datetime

import pytest
import iso8601


@pytest.mark.django_db
class TestStaff:
    """Test user details for staff

    * check for valid data
    * check for staff/usual users
    """
    def test_user_details_for_staff_true(self, client, request_user, user, token):
        request_user.is_staff = True
        request_user.save()
        response = client.get(f'/api/user/{user.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        response_dict = response.json()
        assert response.status_code == 200
        assert response_dict.get('username') == user.username
        assert response_dict.get('email') == user.email
        assert response_dict.get('id') == str(user.id)
        assert iso8601.parse_date(response_dict.get('created')) == user.created
        assert iso8601.parse_date(response_dict.get('updated')) == user.updated
        assert response_dict.get('first_name') == user.first_name
        assert response_dict.get('last_name') == user.last_name
        assert datetime.strptime(response_dict.get('date_of_birth'), '%Y-%m-%d').date() == user.date_of_birth
        assert response_dict.get('password') is None
        assert response_dict.get('is_staff') is False
        assert response_dict.get('is_active') is True
        assert response_dict.get('profile_image') is None

    def test_user_details_for_staff_false(self, client, request_user, user, token):
        response = client.get(f'/api/user/{user.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert response.status_code == 403
