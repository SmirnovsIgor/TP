from faker import Faker
from django.contrib.contenttypes.models import ContentType

from apps.users.models import User, Organization, MembersList
from apps.locations.models import Address, Place
from apps.events.models import Event


class Populate:

    DEFAULT_NUMBER = 20
    NONE_COEF = 0.25
    faker = Faker()

    def __init__(self, *args, **kwargs):
        keys = ('user', 'company', 'address', 'place', 'event')
        vals = tuple([args[i] for i in range(len(args)) if i < len(keys)] + [self.DEFAULT_NUMBER]*(5-len(args)))
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
            data['username'] = self.faker.user_name()
            data['password'] = self.faker.password()
            data['email'] = self.faker.email()
            data['date_of_birth'] = self.faker.date_of_birth()
            data['first_name'], data['last_name'] = self.faker.first_name(), self.faker.last_name()
            User.objects.create(**data)

    def populate_company(self):
        users = User.objects.order_by('-created')
        if self.company_number >= self.user_number:
            self.company_number = self.user_number
        null_objects = int(self.user_number * self.NONE_COEF)
        self.company_number -= null_objects
        for i in range(self.company_number):
            data, data_m = {}, {}
            data['name'] = self.faker.company()
            data['email'] = self.faker.email()
            data['approved'] = self.faker.boolean(chance_of_getting_true=60)
            data['description'] = self.faker.text(max_nb_chars=200, ext_word_list=None)
            data_m['organization'] = Organization.objects.create(**data)
            data_m['member'] = users[i]
            MembersList.objects.create(**data_m)

    def populate_address(self):
        for _ in range(self.address_number):
            data = {}
            data['country'] = self.faker.country()[:30]
            data['city'] = self.faker.city()[:30]
            data['street'] = self.faker.street_name()[:30]
            data['house'] = self.faker.building_number()[:10]
            data['floor'] = self.faker.pyint(min_value=1, max_value=50, step=1)
            data['apartments'] = self.faker.pyint(min_value=1, max_value=1000, step=1)
            Address.objects.create(**data)

    def populate_place(self):
        null_objects = int(self.address_number * self.NONE_COEF)
        self.place_number -= null_objects
        addresses = Address.objects.order_by('-created')[:self.place_number]
        status = [Place.STATUS_TEMPORARILY_CLOSED, Place.STATUS_WORKING, Place.STATUS_CLOSED]
        for i in range(self.place_number):
            data = {}
            data['name'] = self.faker.company()[:75]
            data['address'] = addresses[i]
            data['description'] = self.faker.text(max_nb_chars=200, ext_word_list=None)
            data['status'] = status[i % len(status)]
            Place.objects.create(**data)

    def populate_event(self):
        users = User.objects.all().order_by('-created')
        addresses = Address.objects.all().order_by('-created')
        places = Place.objects.all().order_by('-created')
        model_type = ContentType.objects.get_for_model(User)
        for i in range(self.event_number):
            data = {}
            data['name'] = self.faker.catch_phrase()[:64]
            data['description'] = self.faker.text(max_nb_chars=200, ext_word_list=None)
            data['organizer_type'] = model_type
            data['organizer_id'] = users[i].id
            data['place'] = places[i] if i < len(places) else None
            data['address'] = addresses[i]
            data['date'] = self.faker.past_datetime(start_date="-30d")
            data['duration'] = self.faker.time()
            data['age_rate'] = self.faker.pyint(min_value=0, max_value=50, step=1)
            data['max_members'] = self.faker.pyint(min_value=10, max_value=10000, step=1)
            data['is_top'] = self.faker.boolean(chance_of_getting_true=50)
            data['is_hot'] = self.faker.boolean(chance_of_getting_true=50)
            Event.objects.create(**data)
