import factory

from faker import Factory as FakeFactory
from django.contrib.contenttypes.models import ContentType

from apps.users.models import User, Organization, MembersList
from apps.locations.models import Address, Place
from apps.events.models import Event


faker = FakeFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory"""
    username = factory.LazyAttribute(lambda x: faker.user_name())
    password = factory.LazyAttribute(lambda x: faker.password())
    email = factory.LazyAttribute(lambda x: faker.email())
    date_of_birth = factory.LazyAttribute(lambda x: faker.date_of_birth())
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())

    class Meta:
        model = User
        abstract = False


class OrganizationFactory(factory.django.DjangoModelFactory):
    """Organization factory"""
    name = factory.LazyAttribute(lambda x: faker.company())
    email = factory.LazyAttribute(lambda x: faker.email())
    approved = factory.LazyAttribute(lambda x: faker.boolean(chance_of_getting_true=60))
    description = factory.LazyAttribute(lambda x: faker.text(max_nb_chars=200, ext_word_list=None))

    class Meta:
        model = Organization
        abstract = False


class MembersListFactory(factory.django.DjangoModelFactory):
    """Organization and user connection"""
    member = factory.Iterator(User.objects.all())
    organization = factory.Iterator(Organization.objects.all())

    class Meta:
        model = MembersList
        abstract = False


class AddressFactory(factory.django.DjangoModelFactory):
    """Address factory"""
    country = factory.LazyAttribute(lambda x: faker.country()[:30])
    city = factory.LazyAttribute(lambda x: faker.city()[:30])
    street = factory.LazyAttribute(lambda x: faker.street_name()[:30])
    house = factory.LazyAttribute(lambda x: faker.building_number()[:10])
    floor = factory.LazyAttribute(lambda x: faker.pyint(min_value=1, max_value=50, step=1))
    apartments = factory.LazyAttribute(lambda x: faker.pyint(min_value=1, max_value=1000, step=1))

    class Meta:
        model = Address
        abstract = False


class PlaceFactory(factory.django.DjangoModelFactory):
    """Place factory"""
    name = factory.LazyAttribute(lambda x: faker.company()[:75])
    address = factory.Iterator(Address.objects.all())
    description = factory.LazyAttribute(lambda x: faker.text(max_nb_chars=200, ext_word_list=None))
    status = factory.LazyAttribute(lambda x: Place.STATUS_WORKING)

    class Meta:
        model = Place
        abstract = False


# Problem with generic field in event model
class EventFactory(factory.django.DjangoModelFactory):
    """Event factory"""
    name = factory.LazyAttribute(lambda x: faker.catch_phrase()[:64])
    description = factory.LazyAttribute(lambda x: faker.text(max_nb_chars=200, ext_word_list=None))
    organizer_id = factory.SelfAttribute('organizer.id')
    organizer_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )
    address = factory.Iterator(Address.objects.all().order_by('-created'))
    date = factory.LazyAttribute(lambda x: faker.past_datetime(start_date="-30d"))
    duration = factory.LazyAttribute(lambda x: faker.time())
    age_rate = factory.LazyAttribute(lambda x: faker.pyint(min_value=0, max_value=50, step=1))
    max_members = factory.LazyAttribute(lambda x: faker.pyint(min_value=10, max_value=10000, step=1))
    is_top = factory.LazyAttribute(lambda x: faker.boolean(chance_of_getting_true=50))
    is_hot = factory.LazyAttribute(lambda x: faker.boolean(chance_of_getting_true=50))

    class Meta:
        model = Event
        abstract = False
