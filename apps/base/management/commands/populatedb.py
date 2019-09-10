from django.core.management.base import BaseCommand
from tools.populate import (UserFactory, OrganizationFactory,
                            MembersListFactory, AddressFactory,
                            PlaceFactory, EventFactory)


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
        big_batch_number = 50
        small_batch_number = 30

        # UserFactory.create_batch(size=big_batch_number)
        # OrganizationFactory.create_batch(size=small_batch_number)
        # MembersListFactory.create_batch(size=small_batch_number)
        # AddressFactory.create_batch(size=big_batch_number)
        # PlaceFactory.create_batch(size=small_batch_number)
        EventFactory.create_batch(size=small_batch_number)
        self.stdout.write(self.style.SUCCESS('DB was successfully populated'))
