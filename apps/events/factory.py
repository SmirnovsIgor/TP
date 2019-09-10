import factory
import factory.fuzzy

from faker import Factory as FakeFactory
from django.contrib.contenttypes.models import ContentType

from apps.users.models import User
from apps.locations.models import Address
from apps.events.models import Event


faker = FakeFactory.create()


class EventAbstractFactory(factory.django.DjangoModelFactory):
    """Abstract Event factory"""
    name = factory.LazyAttribute(lambda x: faker.catch_phrase()[:64])
    description = factory.LazyAttribute(lambda x: faker.text(max_nb_chars=200, ext_word_list=None))
    organizer_id = factory.SelfAttribute('organizer.id')
    organizer_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.organizer)
    )
    address = factory.Iterator(Address.objects.all().order_by('?'))
    date = factory.LazyAttribute(lambda x: faker.past_datetime(start_date="-30d"))
    duration = factory.LazyAttribute(lambda x: faker.time())
    age_rate = factory.LazyAttribute(lambda x: faker.pyint(min_value=0, max_value=50, step=1))
    max_members = factory.LazyAttribute(lambda x: faker.pyint(min_value=10, max_value=10000, step=1))
    is_top = factory.LazyAttribute(lambda x: faker.boolean(chance_of_getting_true=50))
    is_hot = factory.LazyAttribute(lambda x: faker.boolean(chance_of_getting_true=50))
    status = factory.fuzzy.FuzzyChoice(Event.STATUS_TYPES, getter=lambda c: c[0])

    class Meta:
        exclude = ['organizer']
        abstract = True


class EventFactory(EventAbstractFactory):
    organizer = factory.Iterator(User.objects.all())

    class Meta:
        model = Event
