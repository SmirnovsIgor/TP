import pytest
from pytest_factoryboy import register

from apps.events.factories import (
    EventUserWithoutPlaceFactory,
    EventUserWithPlaceFactory,
    EventOrganizerWithoutPlaceFactory,
    EventOrganizerWithPlaceFactory
)
from apps.subscriptions.factories import SubscriptionFactory
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
register(SubscriptionFactory, 'subscription')


@pytest.fixture
def place_qty():
    return 1


@pytest.fixture
def places(place_qty):
    return PlaceFactory.create_batch(size=place_qty)
