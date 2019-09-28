import factory.fuzzy
from django.db.models.signals import pre_save
from faker import Factory as FakeFactory

from apps.events.factories import EventUserWithoutPlaceFactory
from apps.events.models import Event
from apps.subscriptions.models import Subscription
from apps.users.factories import UserFactory
from apps.users.models import User

faker = FakeFactory.create()


@factory.django.mute_signals(pre_save)
class SubscriptionFactory(factory.django.DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    event = factory.Iterator(Event.objects.all())
    status = factory.fuzzy.FuzzyChoice(Subscription.STATUS_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Subscription


@factory.django.mute_signals(pre_save)
class ForTestsSubscriptionFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    event = factory.SubFactory(EventUserWithoutPlaceFactory)
    status = factory.fuzzy.FuzzyChoice(Subscription.STATUS_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Subscription
