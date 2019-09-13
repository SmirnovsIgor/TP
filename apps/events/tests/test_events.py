import faker
import pytest


@pytest.mark.django_db
class TestEvents:
    # @pytest.mark.parametrize()
    def test_detail(self, client, ev_us_ad):
        res = client.get(f'/api/events/{ev_us_ad.id}')
        assert res.status_code == 200
        event_dict = res.json()
        assert event_dict.get('name')
        assert event_dict.get('description')
        assert event_dict.get('poster')
        assert event_dict.get('organizer_type')
        assert event_dict.get('organizer_id')
        assert event_dict.get('organizer')
        assert event_dict.get('place')
        assert event_dict.get('address')
        assert event_dict.get('date')
        assert event_dict.get('duration')
        assert event_dict.get('age_rate')
        assert event_dict.get('is_approved')
        assert event_dict.get('is_hot')
        assert event_dict.get('is_top')
        assert event_dict.get('max_members')
        assert event_dict.get('status')

    @pytest.mark.parametrize('event_qty', [0, 1, 10, 100])
    def test_list(self, client, events_user_address, event_qty):
        res = client.get(f'/api/events/')
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        assert len(res.json()) == event_qty
