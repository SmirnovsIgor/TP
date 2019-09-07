from django.core.management.base import BaseCommand, CommandError
from tools.populate import Populate


DEFAULT_NUMBER = 20


class Command(BaseCommand):
    help = 'Populate DB'

    def add_arguments(self, parser):
        parser.add_argument('user_number', nargs='?', type=int)
        parser.add_argument('company_number', nargs='?', type=int)
        parser.add_argument('address_number', nargs='?', type=int)
        parser.add_argument('place_number', nargs='?', type=int)
        parser.add_argument('event_number', nargs='?', type=int)

    def handle(self, *args, **options):
        data = [options[key] for key in options if key.endswith('number')]
        for i in range(len(data)):
            data[i] = DEFAULT_NUMBER if data[i] is None else data[i]
        p = Populate(*data)
        p.populate_user()
        p.populate_company()
        p.populate_address()
        p.populate_place()
        p.populate_event()
        self.stdout.write(self.style.SUCCESS('DB was successfully populated'))
