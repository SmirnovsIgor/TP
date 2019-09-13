import pytest
from pytest_factoryboy import register

from apps.events.factories import (
    EventUserWithoutPlaceFactory,
    EventUserWithPlaceFactory,
    EventOrganizerWithoutPlaceFactory,
    EventOrganizerWithPlaceFactory
)


register(EventUserWithoutPlaceFactory, 'ev_us_ad')
register(EventUserWithPlaceFactory, 'ev_us_ad_pl')
register(EventOrganizerWithoutPlaceFactory, 'ev_or_ad')
register(EventOrganizerWithPlaceFactory, 'ev_or_ad_pl')


@pytest.fixture
def event_qty():
    return 1


@pytest.fixture
def events_user_address(event_qty):
    return EventUserWithoutPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def events_user_address_place(event_qty):
    return EventUserWithPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def events_org_address(event_qty):
    return EventOrganizerWithoutPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def events_org_address_place(event_qty):
    return EventOrganizerWithoutPlaceFactory.create_batch(size=event_qty)
