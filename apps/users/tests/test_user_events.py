import pytest
from rest_framework import status


@pytest.mark.django_db
class TestUserEvents:
    @pytest.mark.parametrize('event_qty', [0, 1, 10, 50])
    def test_user_events_list_authorized_true(self, client, request_user, token, events, event_qty):
        for event in events:
            event.organizer = request_user
            event.save()
        response = client.get('/api/users/me/events/',  **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) == event_qty

    def test_self_events_list_authorized_false(self, client):
        response = client.get('/api/users/me/events/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserEventByID:
    def test_user_event_by_id_authorized_true(self, client, request_user, token, event):
        event.organizer = request_user
        event.save()
        response = client.get(f'/api/users/me/events/{event.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        response_dict = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_dict.get('organizer_id') == str(event.organizer_id)

    def test_user_event_by_id_authorized_false(self, client, event):
        response = client.get(f'/api/users/me/events/{event.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
