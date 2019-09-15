import pytest
from pytest_factoryboy import register

from apps.events.factories import (
    EventUserWithoutPlaceFactory,
    EventUserWithPlaceFactory,
    EventOrganizerWithoutPlaceFactory,
    EventOrganizerWithPlaceFactory
)


register(EventUserWithoutPlaceFactory, 'event')
register(EventUserWithPlaceFactory, 'event2')
register(EventOrganizerWithoutPlaceFactory, 'event3')
register(EventOrganizerWithPlaceFactory, 'event4')


@pytest.fixture
def event_qty():
    return 1


@pytest.fixture
def eventsUser1(event_qty):
    return EventUserWithoutPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def eventsUser2(event_qty):
    return EventUserWithPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def eventsOrg1(event_qty):
    return EventOrganizerWithoutPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def eventsOrg2(event_qty):
    return EventOrganizerWithoutPlaceFactory.create_batch(size=event_qty)
