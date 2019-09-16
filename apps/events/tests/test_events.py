import faker
import uuid
import datetime
import pytest

from django.contrib.contenttypes.models import ContentType
from rest_framework import status

from apps.users.models import User, Organization
from apps.events.models import Event


@pytest.mark.django_db
class TestEvents:
    """
    poster in Event is always None,
    because we do not generate it

    """
    def test_detail_event_by_user_without_place(self, client, event_u):
        """Test event created by user without place"""
        res = client.get(f'/api/events/{event_u.id}/')
        assert res.status_code == status.HTTP_200_OK
        event_dict = res.json()
        assert isinstance(event_dict.get('name'), str)
        assert isinstance(event_dict.get('description'), str)
        assert event_dict['poster'] is None
        assert event_dict.get('organizer_type') == ContentType.objects.get_for_model(User).id
        assert uuid.UUID(event_dict.get('organizer_id'))
        assert isinstance(event_dict.get('organizer'), dict)
        assert event_dict['place'] is None
        assert isinstance(event_dict.get('address'), dict)
        # assert datetime.datetime.isoformat(datetime.datetime.fromisoformat(event_dict.get('date')))
        assert event_dict.get('date')
        assert datetime.datetime.strptime(event_dict.get('duration'), '%H:%M:%S')
        assert isinstance(event_dict.get('age_rate'), int)
        assert event_dict.get('age_rate') > 0
        assert isinstance(event_dict.get('is_approved'), bool)
        assert isinstance(event_dict.get('is_hot'), bool)
        assert isinstance(event_dict.get('is_top'), bool)
        assert isinstance(event_dict.get('max_members'), int)
        assert event_dict.get('max_members') > 0
        assert event_dict.get('status') in (Event.SOON, Event.SUCCEED, Event.REJECTED)

    def test_detail_event_by_user_with_place(self, client, event_u_p):
        """Test event created by user with place"""
        res = client.get(f'/api/events/{event_u_p.id}/')
        assert res.status_code == status.HTTP_200_OK
        event_dict = res.json()
        assert isinstance(event_dict.get('name'), str)
        assert isinstance(event_dict.get('description'), str)
        assert event_dict['poster'] is None
        assert event_dict.get('organizer_type') == ContentType.objects.get_for_model(User).id
        assert uuid.UUID(event_dict.get('organizer_id'))
        assert isinstance(event_dict.get('organizer'), dict)
        assert isinstance(event_dict['place'], dict)
        assert isinstance(event_dict.get('address'), dict)
        assert event_dict.get('date')
        assert datetime.datetime.strptime(event_dict.get('duration'), '%H:%M:%S')
        assert isinstance(event_dict.get('age_rate'), int)
        assert event_dict.get('age_rate') > 0
        assert isinstance(event_dict.get('is_approved'), bool)
        assert isinstance(event_dict.get('is_hot'), bool)
        assert isinstance(event_dict.get('is_top'), bool)
        assert isinstance(event_dict.get('max_members'), int)
        assert event_dict.get('max_members') > 0
        assert event_dict.get('status') in (Event.SOON, Event.SUCCEED, Event.REJECTED)

    def test_detail_event_by_org_without_place(self, client, event_o):
        """Test event created by organization without place"""
        res = client.get(f'/api/events/{event_o.id}/')
        assert res.status_code == status.HTTP_200_OK
        event_dict = res.json()
        assert isinstance(event_dict.get('name'), str)
        assert isinstance(event_dict.get('description'), str)
        assert event_dict['poster'] is None
        assert event_dict.get('organizer_type') == ContentType.objects.get_for_model(Organization).id
        assert uuid.UUID(event_dict.get('organizer_id'))
        assert isinstance(event_dict.get('organizer'), dict)
        assert event_dict['place'] is None
        assert isinstance(event_dict.get('address'), dict)
        assert event_dict.get('date')
        assert datetime.datetime.strptime(event_dict.get('duration'), '%H:%M:%S')
        assert isinstance(event_dict.get('age_rate'), int)
        assert event_dict.get('age_rate') > 0
        assert isinstance(event_dict.get('is_approved'), bool)
        assert isinstance(event_dict.get('is_hot'), bool)
        assert isinstance(event_dict.get('is_top'), bool)
        assert isinstance(event_dict.get('max_members'), int)
        assert event_dict.get('max_members') > 0
        assert event_dict.get('status') in (Event.SOON, Event.SUCCEED, Event.REJECTED)

    def test_detail_event_by_org_with_place(self, client, event_o_p):
        """Test event created by organization with place"""
        res = client.get(f'/api/events/{event_o_p.id}/')
        assert res.status_code == status.HTTP_200_OK
        event_dict = res.json()
        assert isinstance(event_dict.get('name'), str)
        assert isinstance(event_dict.get('description'), str)
        assert event_dict['poster'] is None
        assert event_dict.get('organizer_type') == ContentType.objects.get_for_model(Organization).id
        assert uuid.UUID(event_dict.get('organizer_id'))
        assert isinstance(event_dict.get('organizer'), dict)
        assert isinstance(event_dict['place'], dict)
        assert isinstance(event_dict.get('address'), dict)
        assert event_dict.get('date')
        assert datetime.datetime.strptime(event_dict.get('duration'), '%H:%M:%S')
        assert isinstance(event_dict.get('age_rate'), int)
        assert event_dict.get('age_rate') > 0
        assert isinstance(event_dict.get('is_approved'), bool)
        assert isinstance(event_dict.get('is_hot'), bool)
        assert isinstance(event_dict.get('is_top'), bool)
        assert isinstance(event_dict.get('max_members'), int)
        assert event_dict.get('max_members') > 0
        assert event_dict.get('status') in (Event.SOON, Event.SUCCEED, Event.REJECTED)

    def test_detail_negative(self, client):
        """Negative test checks access to uncreated event by random uuid"""
        res = client.get(f'/api/events/{faker.Faker().uuid4()}/')
        assert res.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize('event_qty', [0, 1, 10, 100])
    def test_list_user_without_place(self, client, events_user_without_place, event_qty):
        """Collection of events created by user with place"""
        res = client.get(f'/api/events/')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) == event_qty

    @pytest.mark.parametrize('event_qty', [0, 1, 10, 100])
    def test_list_user_with_place(self, client, events_user_with_pace, event_qty):
        """Collection of events created by user without place"""
        res = client.get(f'/api/events/')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) == event_qty

    @pytest.mark.parametrize('event_qty', [0, 1, 10, 100])
    def test_list_org_without_place(self, client, events_org_without_place, event_qty):
        """Collection of events created by organization without place"""
        res = client.get(f'/api/events/')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) == event_qty

    @pytest.mark.parametrize('event_qty', [0, 1, 10, 100])
    def test_list_org_with_place(self, client, events_org_with_place, event_qty):
        """Collection of events created by organization with place"""
        res = client.get(f'/api/events/')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) == event_qty
