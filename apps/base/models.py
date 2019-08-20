import uuid

from django.db import models


class CreateModifyModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class IDModel(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    class Meta:
        abstract = True


class BaseModel(CreateModifyModel, IDModel):
    pass
