import factory

from faker import Factory as FakeFactory
from django.contrib.contenttypes.models import ContentType

from apps.users.models import User, Organization, MembersList
from apps.locations.models import Address, Place
from apps.events.models import Event

from apps.locations.factory import AddressFactory, PlaceFactory


faker = FakeFactory.create()


# Problem with generic field, place and address in event model
class EventFactory(factory.django.DjangoModelFactory):
    """Event factory"""
    name = factory.LazyAttribute(lambda x: faker.catch_phrase()[:64])
    description = factory.LazyAttribute(lambda x: faker.text(max_nb_chars=200, ext_word_list=None))
    # organizer_id = factory.SelfAttribute('organizer.id')
    # organizer_type = factory.LazyAttribute(
    #     lambda o: ContentType.objects.get_for_model(o.content_object)
    # )
    address = factory.Iterator(Address.objects.all())
    # place = factory.RelatedFactory(AddressFactory, '')
    # address = factory.SubFactory(AddressFactory)
    date = factory.LazyAttribute(lambda x: faker.past_datetime(start_date="-30d"))
    duration = factory.LazyAttribute(lambda x: faker.time())
    age_rate = factory.LazyAttribute(lambda x: faker.pyint(min_value=0, max_value=50, step=1))
    max_members = factory.LazyAttribute(lambda x: faker.pyint(min_value=10, max_value=10000, step=1))
    is_top = factory.LazyAttribute(lambda x: faker.boolean(chance_of_getting_true=50))
    is_hot = factory.LazyAttribute(lambda x: faker.boolean(chance_of_getting_true=50))

    class Meta:
        model = Event
        # abstract = False
