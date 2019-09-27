import factory
import factory.fuzzy
from faker import Factory as FakeFactory
from django.contrib.contenttypes.models import ContentType

from apps.events.factories import EventUserWithPlaceFactory
from apps.feedbacks.models import Comment
from apps.users.factories import OrganizationFactory, UserFactory
from apps.locations.factories import PlaceFactory


faker = FakeFactory.create()


class CommentAbstractFactory(factory.django.DjangoModelFactory):
    text = factory.Faker('text', max_nb_chars=200, ext_word_list=None)
    topic_id = factory.SelfAttribute('topic.id')
    topic_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.topic)
    )
    parent_id = factory.SelfAttribute('parent.id')
    parent_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.parent)
    )
    status = factory.fuzzy.FuzzyChoice(Comment.OK)
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        exclude = ['topic', 'parent']
        abstract = True


class CommentToOrganizationFactory(CommentAbstractFactory):
    topic = factory.SubFactory(OrganizationFactory)
    parent = factory.LazyAttribute(lambda o: o.topic)

    class Meta:
        model = Comment


class CommentToPlaceFactory(CommentAbstractFactory):
    topic = factory.SubFactory(PlaceFactory)
    parent = factory.LazyAttribute(lambda o: o.topic)

    class Meta:
        model = Comment


class CommentToEventFactory(CommentAbstractFactory):
    topic = factory.SubFactory(EventUserWithPlaceFactory)
    parent = factory.LazyAttribute(lambda o: o.topic)

    class Meta:
        model = Comment


# class CommentToReviewFactory(CommentAbstractFactory):
#     topic = factory.SubFactory(Organization)
#     parent = factory.LazyAttribute(lambda o: o.topic)
#
#     class Meta:
#         model = Comment
