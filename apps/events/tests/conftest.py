import pytest
from apps.events import factories
from pytest_factoryboy import register


register(factories.EventOrganizerWithPlaceFactory)
