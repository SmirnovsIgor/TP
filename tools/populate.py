from faker import Factory as FakeFactory
from faker import Faker as Fake

from apps.users.models import User, Organization
from apps.locations.models import Address, Place
from apps.events.models import Event


class Populate:
    def __init__(self, *args, **kwargs):
        keys = ('user', 'company', 'address', 'place', 'event')
        vals = tuple([args[i] for i in range(len(args)) if i < len(keys)] + [10]*(5-len(args)))
        data = dict(zip(keys, vals))
        if kwargs:
            for key in keys:
                data[key] = kwargs[key] if key in kwargs else data[key]
        self.user_number = data['user']
        self.company_number = data['company']
        self.address_number = data['address']
        self.place_number = data['place']
        self.event_number = data['event']

    def populate_user(self):
        pass

    def populate_company(self):
        pass

    def populate_address(self):
        pass

    def populate_place(self):
        pass

    def populate_event(self):
        pass

