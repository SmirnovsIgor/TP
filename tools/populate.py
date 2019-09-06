from faker import Faker
from django.contrib.contenttypes.models import ContentType

from apps.users.models import User, Organization, MembersList
from apps.locations.models import Address, Place
from apps.events.models import Event


class Populate:

    faker = Faker()

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
        for _ in range(self.user_number):
            data = dict()
            data['username'] = ''.join(self.faker.name().split()).lower()
            data['email'] = self.faker.email()
            data['date_of_birth'] = self.faker.date()
            data['first_name'], data['last_name'] = tuple(self.faker.name().split())
            User.objects.create(**data)

    def populate_company(self):
        for _ in range(self.company_number):
            data, data_m = {}, {}
            data['name'] = self.faker.company()
            data['email'] = self.faker.email()
            data['description'] = self.faker.text()
            data_m['organization'] = Organization.objects.get_or_create(**data)[0]
            data_m['member'] = User.objects.filter(membership__isnull=True).order_by('-created')[0]
            MembersList.objects.get_or_create(**data_m)

    def populate_address(self):
        for _ in range(self.address_number):
            data = {}
            data['country'] = self.faker.country()[:30]
            data['city'] = self.faker.city()[:30]
            Address.objects.create(**data)

    def populate_place(self):
        addresses = Address.objects.order_by('-created')[:self.address_number]
        for i in range(self.place_number):
            data = {}
            data['name'] = ''.join(self.faker.name().split())[:75]
            data['address'] = addresses[i] if i <= self.address_number-1 else None
            data['status'] = 'Working'
            Place.objects.create(**data)

    def populate_event(self):
        users = User.objects.all().order_by('-created')
        addresses = Address.objects.all().order_by('-created')
        places = Place.objects.all().order_by('-created')
        model_type = ContentType.objects.get_for_model(User)
        for i in range(self.event_number):
            data = {}
            data['name'] = ''.join(self.faker.name().split())[:64]
            data['description'] = self.faker.text()
            data['organizer_type'] = model_type
            data['organizer_id'] = users[i].id
            data['place'] = places[i] if i <= self.place_number-1 else None
            data['address'] = addresses[i]
            data['date'] = self.faker.date_time()
            data['duration'] = self.faker.time()
            data['age_rate'] = self.faker.random_number(digits=2)
            data['max_members'] = self.faker.random_number(digits=3)
            Event.objects.create(**data)
