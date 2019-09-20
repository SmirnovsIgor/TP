import pytest
from pytest_factoryboy import register
from rest_auth.models import TokenModel
from rest_auth.app_settings import create_token, TokenSerializer

from apps.events.factories import (
    EventUserWithoutPlaceFactory,
    EventUserWithPlaceFactory,
    EventOrganizerWithoutPlaceFactory,
    EventOrganizerWithPlaceFactory
)
from apps.locations.factories import AddressFactory, PlaceFactory
from apps.users.factories import UserFactory, OrganizationFactory

register(UserFactory, 'user')
register(PlaceFactory, 'place')
register(AddressFactory, 'address')
register(OrganizationFactory, 'organization')
register(EventUserWithoutPlaceFactory, 'event_created_by_user_without_place')
register(EventUserWithPlaceFactory, 'event_created_by_user_with_place')
register(EventOrganizerWithoutPlaceFactory, 'event_created_by_organization_without_place')
register(EventOrganizerWithPlaceFactory, 'event_created_by_organization_with_place')


@pytest.fixture
def event_qty():
    return 1


@pytest.fixture
def events_user_without_place(event_qty):
    return EventUserWithoutPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def events_user_with_pace(event_qty):
    return EventUserWithPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def events_org_without_place(event_qty):
    return EventOrganizerWithoutPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def events_org_with_place(event_qty):
    return EventOrganizerWithPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def events_batch_for_filtering_and_ordering(event_qty):
    number = event_qty // 4
    query = EventUserWithoutPlaceFactory.create_batch(size=number)
    query += EventUserWithPlaceFactory.create_batch(size=number)
    query += EventOrganizerWithoutPlaceFactory.create_batch(size=number)
    query += EventOrganizerWithPlaceFactory.create_batch(size=number)
    return query


@pytest.fixture
def place_dict():
    return {
        "name": "Vargas-Simpson",
        "photo": None,
        "description": "Wall fall yard maintain writer reveal thousand. Different during television history quite. Shake mouth his speech.",
        "status": "WORKING"
    }


@pytest.fixture
def token(user):
    return create_token(TokenModel, user, TokenSerializer)


@pytest.fixture
def event_create_with_not_allowed_to_specify_fields():
    return {
        "place": None,
        "address": {
            "country": "Bosnia and Herzegovina",
            "city": "Henrytown",
            "street": "Manning Land",
            "house": "238",
            "floor": 16,
            "apartments": "264",
            "description": None
        },
        "name": "Secured holistic flexibility",
        "description": "Test represent keep. Population this right break. Hundred lose concern wife represent operation bank year.\nMust example news too. Chance amount any individual. Whose cup tend with card visit.",
        "poster": None,
        "date": "2019-09-13T01:28:31Z",
        "duration": "20:07:54",
        "age_rate": 34,
        "is_approved": True,
        "is_hot": True,
        "is_top": True,
        "max_members": 1504,
        "status": "SOON"
    }


@pytest.fixture
def event_create_without_place_and_with_address_id_in_one_field():
    return None


@pytest.fixture
def event_create_without_place_and_with_address_id_in_dict():
    pass


@pytest.fixture
def event_create_without_place_and_with_creating_address():
    pass


@pytest.fixture
def event_create_with_place_null_and_with_address_id_in_one_field():
    pass


@pytest.fixture
def event_create_with_place_null_and_with_address_id_in_dict():
    pass


@pytest.fixture
def event_create_with_place_null_and_with_creating_address():
    pass


@pytest.fixture
def event_create_with_place_id_in_one_field_and_no_address():
    pass


@pytest.fixture
def event_create_with_place_id_in_one_field_and_address_id():
    pass


@pytest.fixture
def event_create_with_place_id_in_one_field_and_any_address_data():
    pass


@pytest.fixture
def event_create_with_place_id_in_dict_and_no_address():
    pass


@pytest.fixture
def event_create_with_place_id_in_dict_and_address_id():
    pass


@pytest.fixture
def event_create_with_place_id_in_dict_and_any_address_data():
    pass
