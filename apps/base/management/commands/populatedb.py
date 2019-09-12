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
DEFAULT_SMALL_NUMBER = 60


class Command(BaseCommand):
    help = 'Populate DB'

    def add_arguments(self, parser):
        parser.add_argument('great_count', nargs='?', type=int, help='maximum is 100 objects for User, Address, Event')
        parser.add_argument('less_count', nargs='?', type=int, help='maximum is 80 objects for Organizer, Memberslist, Place')

    def handle(self, *args, **options):
        big = DEFAULT_BIG_NUMBER if not options['great_count'] else options['great_count']
        small = DEFAULT_SMALL_NUMBER if not options['less_count'] else options['less_count']
        a = int((big-small)/2)
        b = (big-small) - a
        c = int(small/2)
        d = small - c
        numbers = {
            "EventUserAddrPlace": a,
            "EventUserAddr": b,
            "EventOrgAddrPlace": c,
            "EventOrgAddr": d,
        }

        EventUserWithoutPlaceFactory.create_batch(size=numbers["EventUserAddrPlace"])
        EventUserWithPlaceFactory.create_batch(size=numbers["EventUserAddr"])
        EventOrganizerWithoutPlaceFactory.create_batch(size=numbers["EventOrgAddrPlace"])
        EventOrganizerWithPlaceFactory.create_batch(size=numbers["EventOrgAddr"])
        self.stdout.write(self.style.SUCCESS("DB was successfully populated"))
