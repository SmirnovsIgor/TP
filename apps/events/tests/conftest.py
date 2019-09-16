import pytest

from apps.events.factories import (
    EventUserWithoutPlaceFactory,
    EventUserWithPlaceFactory,
    EventOrganizerWithoutPlaceFactory,
    EventOrganizerWithPlaceFactory
)


@pytest.fixture
def event_u():
    return EventUserWithoutPlaceFactory()


@pytest.fixture
def event_u_p():
    return EventUserWithPlaceFactory()


@pytest.fixture
def event_o():
    return EventOrganizerWithoutPlaceFactory()


@pytest.fixture
def event_o_p():
    return EventOrganizerWithPlaceFactory()


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
