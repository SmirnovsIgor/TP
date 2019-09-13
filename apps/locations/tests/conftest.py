import pytest
from pytest_factoryboy import register

from apps.locations.factories import PlaceFactory


register(PlaceFactory, 'place')


@pytest.fixture
def place_qty():
    return 1


@pytest.fixture
def places(place_qty):
    return PlaceFactory.create_batch(size=place_qty)
