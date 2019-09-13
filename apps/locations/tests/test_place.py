import pytest
import faker


@pytest.mark.django_db
class TestPlaces:
    def test_detail(self, client, place):
        res = client.get(f'/api/places/{place.id}/')
        assert res.status_code == 200
        place_dict = res.json()
        assert place_dict.get('name')
        assert place_dict.get('address')
        assert place_dict.get('photo')
        assert place_dict.get('description')
        assert place_dict.get('status')

    @pytest.mark.parametrize('place_qty', [0, 1, 10, 100])
    def test_list(self, client, places, place_qty):
        res = client.get('/api/places/')
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        assert len(res.json()) == place_qty

    def test_detail_error(self, client):
        res = client.get(f'api/places/{faker.Faker().random_number()}/')
        assert res.status_code == 404
