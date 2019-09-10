from django.core.management.base import BaseCommand

from apps.users.factory import UserFactory, OrganizationFactory, MembersListFactory
from apps.locations.factory import AddressFactory, PlaceFactory
from apps.events.factory import EventFactory


DEFAULT_NUMBER = 50
COEF = 75


class Command(BaseCommand):
    help = 'Populate DB'

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='?', type=int)
        parser.add_argument('percent', nargs='?', type=int)

    def handle(self, *args, **options):
        # big_batch_number = DEFAULT_NUMBER if not options['number'] else options['number']
        # coef = COEF if not options['percent'] else options['percent']
        # small_batch_number = int(big_batch_number * coef / 100)
        big_batch_number = 5
        small_batch_number = 3
        delta = big_batch_number - small_batch_number

        # ----------- with iterator --------------
        # UserFactory.create_batch(size=big_batch_number)
        # OrganizationFactory.create_batch(size=small_batch_number)
        # MembersListFactory.create_batch(size=small_batch_number)
        # AddressFactory.create_batch(size=big_batch_number)
        # PlaceFactory.create_batch(size=small_batch_number)
        # EventFactory.create_batch(size=small_batch_number)
        # -------- with subfactory --------------
        EventFactory.create_batch(size=small_batch_number)
        # MembersListFactory.create_batch(size=small_batch_number)
        # UserFactory.create_batch(size=delta)
        # PlaceFactory.create_batch(size=small_batch_number)
        # AddressFactory.create_batch(size=delta)
        self.stdout.write(self.style.SUCCESS('DB was successfully populated'))
