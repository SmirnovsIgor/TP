from django.core.management.base import BaseCommand

from apps.users.factories import UserFactory, OrganizationFactory, MembersListFactory
from apps.locations.factories import AddressFactory, PlaceFactory
from apps.events.factories import EventFactory


DEFAULT_BIG_NUMBER = 100
DEFAULT_SMALL_NUMBER = 75


class Command(BaseCommand):
    help = 'Populate DB'

    def add_arguments(self, parser):
        parser.add_argument('big_number', nargs='?', type=int, help='maximum is 100 objects')
        parser.add_argument('small_number', nargs='?', type=int, help='maximum is 100 objects')

    def handle(self, *args, **options):
        big_batch_number = DEFAULT_BIG_NUMBER if not options['big_number'] else options['big_number']
        small_batch_number = DEFAULT_SMALL_NUMBER if not options['small_number'] else options['small_number']

        UserFactory.create_batch(size=big_batch_number)
        OrganizationFactory.create_batch(size=small_batch_number)
        MembersListFactory.create_batch(size=small_batch_number)
        AddressFactory.create_batch(size=big_batch_number)
        PlaceFactory.create_batch(size=small_batch_number)
        EventFactory.create_batch(size=big_batch_number)
        self.stdout.write(self.style.SUCCESS('DB was successfully populated'))
