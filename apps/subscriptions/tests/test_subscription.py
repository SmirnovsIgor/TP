import pytest
from rest_framework import status

from apps.subscriptions.models import Subscription


@pytest.mark.django_db
class TestUserSubscriptions:
    @pytest.mark.parametrize('subscription_qty', [0, 1, 10, 50])
    def test_user_subscriptions_for_staff_true(self, client, request_user, user, token, subscriptions, subscription_qty):
        request_user.is_staff = True
        request_user.save()
        for subscription in subscriptions:
            subscription.user = user
            subscription.save()
        res = client.get(f'/api/users/{user.id}/subscriptions/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) == subscription_qty

    def test_user_subscriptions_for_staff_false(self, client, request_user, user, token):
        res = client.get(f'/api/users/{user.id}/subscriptions/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestSubscriptions:
    @pytest.mark.parametrize('subscription_qty', [0, 1, 10, 50])
    def test_get_subscriptions_for_staff(self, client, request_user, token, subscriptions, subscription_qty):
        request_user.is_staff = True
        request_user.save()
        res = client.get(f'/api/subscriptions/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) == subscription_qty

    @pytest.mark.parametrize('subscription_qty', [0, 1, 10, 50])
    def test_get_subscriptions_for_regular_user(self, client, request_user, token, subscriptions, subscription_qty):
        res = client.get(f'/api/subscriptions/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_get_subscriptions_detail_for_staff(self, client, request_user, owner, token, subscription):
        request_user.is_staff = True
        request_user.save()
        subscription.user = owner
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        res = client.get(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        sub = res.json()
        assert res.status_code == status.HTTP_200_OK
        assert sub.get('event') == str(subscription.event.id)
        assert sub.get('status') == subscription.status

    def test_get_subscriptions_detail_for_regular_user(self, client, request_user, owner, token, subscription):
        subscription.user = owner
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        res = client.get(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_get_subscriptions_detail_for_owner(self, client, request_user, token, subscription, subscription_qty):
        subscription.user = request_user
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        res = client.get(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        sub = res.json()
        assert res.status_code == status.HTTP_200_OK
        assert sub.get('user') == str(request_user.id)
        assert sub.get('event') == str(subscription.event.id)
        assert sub.get('status') == subscription.status

    def test_get_subscriptions_detail_for_deleted_subscription(self, client, request_user, token, subscription):
        subscription.user = request_user
        subscription.status = Subscription.STATUS_CANCELLED
        subscription.save()
        res = client.get(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_get_subscriptions_detail_for_random_id(self, client, request_user, token, subscription):
        subscription.user = request_user
        subscription.status = Subscription.STATUS_CANCELLED
        subscription.save()
        res = client.get(f'/api/subscriptions/ghjklasfg/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_404_NOT_FOUND
