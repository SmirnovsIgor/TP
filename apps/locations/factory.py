import factory

from faker import Factory as FakeFactory

from apps.locations.models import Address, Place


faker = FakeFactory.create()


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
