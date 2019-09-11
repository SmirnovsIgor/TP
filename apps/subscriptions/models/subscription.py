from django.db import models

from apps.base.models import BaseAbstractModel
from apps.events.models import Event
from apps.users.models import User


class Subscription(BaseAbstractModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='subscription')
