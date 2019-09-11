from django.core.management.base import BaseCommand

from apps.users.factories import UserFactory, OrganizationFactory
from apps.locations.factories import AddressFactory, PlaceFactory
from apps.events.factories import (
    EventUserWithoutPlaceFactory,
    EventUserWithPlaceFactory,
    EventOrganizerWithoutPlaceFactory,
    EventOrganizerWithPlaceFactory
)


DEFAULT_BIG_NUMBER = 100
DEFAULT_SMALL_NUMBER = 75


class Command(BaseCommand):
    help = 'Populate DB'

    def add_arguments(self, parser):
        parser.add_argument('great_count', nargs='?', type=int, help='maximum is 100 objects')
        parser.add_argument('less_count', nargs='?', type=int, help='maximum is 80 objects')

    def handle(self, *args, **options):
        big_batch_number = DEFAULT_BIG_NUMBER if not options['great_count'] else options['great_count']
        small_batch_number = DEFAULT_SMALL_NUMBER if not options['less_count'] else options['less_count']

        UserFactory.create_batch(size=small_batch_number)
        OrganizationFactory.create_batch(size=small_batch_number)
        AddressFactory.create_batch(size=small_batch_number)
        PlaceFactory.create_batch(size=small_batch_number)
        EventUserWithPlaceFactory.create_batch(size=small_batch_number)
        EventUserWithoutPlaceFactory.create_batch(size=small_batch_number)
        EventOrganizerWithPlaceFactory.create_batch(size=small_batch_number)
        EventOrganizerWithoutPlaceFactory.create_batch(size=small_batch_number)
        self.stdout.write(self.style.SUCCESS('DB was successfully populated'))
