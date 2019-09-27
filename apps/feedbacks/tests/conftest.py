import pytest
from pytest_factoryboy import register
from rest_auth.models import TokenModel
from rest_auth.app_settings import create_token, TokenSerializer

from apps.events.factories import EventUserWithPlaceFactory
from apps.feedbacks.models import Comment
from apps.locations.factories import AddressFactory, PlaceFactory
from apps.users.factories import UserFactory, OrganizationFactory
from apps.feedbacks.factories import (
    CommentToOrganizationFactory,
    CommentToEventFactory,
    CommentToPlaceFactory,
)

register(UserFactory, 'user')
register(PlaceFactory, 'place')
register(AddressFactory, 'address')
register(OrganizationFactory, 'organization')
register(EventUserWithPlaceFactory, 'event')
register(CommentToOrganizationFactory, 'comment_to_organization')
register(CommentToEventFactory, 'comment_to_event')
register(CommentToPlaceFactory, 'comment_to_place')


@pytest.fixture
def token(user):
    return create_token(TokenModel, user, TokenSerializer)


@pytest.fixture
def comment_qty():
    return 1


@pytest.fixture
def comment_dict():
    return {
        "parent": None,
        "topic": None,
        "text": "Just a comment",
    }


@pytest.fixture
def comments_batch(comment_qty):
    number = comment_qty // 3
    query = CommentToOrganizationFactory.create_batch(size=number, status=Comment.OK)
    query += CommentToPlaceFactory.create_batch(size=number, status=Comment.OK)
    query += CommentToEventFactory.create_batch(size=number, status=Comment.OK)
    return query
