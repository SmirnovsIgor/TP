from django.core.management.base import BaseCommand

from apps.base.management.commands.cleardb import Command as ClearDb
from apps.events.factories import (
    EventUserWithoutPlaceFactory,
    EventUserWithPlaceFactory,
    EventOrganizerWithoutPlaceFactory,
    EventOrganizerWithPlaceFactory
)
from apps.feedbacks.factories import ReviewFactory
from apps.locations.factories import AddressFactory, PlaceFactory
from apps.subscriptions.factories import SubscriptionFactory
from apps.users.factories import UserFactory, MemberListFactory
from apps.users.models import User

DEFAULT_BIG_NUMBER = 60
DEFAULT_SMALL_NUMBER = 40


class Command(BaseCommand):
    help = 'Populate DB'

    def add_arguments(self, parser):
        parser.add_argument('great_count', nargs='?', type=int, help='maximum is 100 objects for ')
        parser.add_argument('less_count', nargs='?', type=int, help='maximum is 80 objects')

    def handle(self, *args, **options):
        ClearDb().handle()
        big = options.get('great_count') or DEFAULT_BIG_NUMBER
        small = options.get('less_count') or DEFAULT_SMALL_NUMBER
        event_user_addr_place = (big - small) // 2
        event_user_addr = (big - small) - event_user_addr_place
        event_org_addr_place = small // 2
        event_org_addr = small - event_org_addr_place
        instances_without_event = small // 4
        User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        EventUserWithPlaceFactory.create_batch(size=event_user_addr_place)
        EventUserWithoutPlaceFactory.create_batch(size=event_user_addr)
        EventOrganizerWithPlaceFactory.create_batch(size=event_org_addr_place)
        EventOrganizerWithoutPlaceFactory.create_batch(size=event_org_addr)
        MemberListFactory.create_batch(size=small)
        UserFactory.create_batch(size=instances_without_event)
        AddressFactory.create_batch(size=instances_without_event)
        PlaceFactory.create_batch(size=instances_without_event)
        SubscriptionFactory.create_batch(size=small)
        ReviewFactory.create_batch(size=small)
        self.stdout.write(self.style.SUCCESS('DB was successfully populated'))
