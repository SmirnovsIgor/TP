import factory

from faker import Factory as FakeFactory

from apps.users.models import User, Organization, MembersList


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
    member = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)

    class Meta:
        model = MembersList
        abstract = False
