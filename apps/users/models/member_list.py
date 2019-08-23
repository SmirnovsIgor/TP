from django.db import models
from apps.users.models import Organization, User


class MembersList(models.Model):
    member_id = models.OneToOneField(User.id, primary_key=True)
    organization_id = models.OneToOneField(Organization.id)
