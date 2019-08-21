from apps.base.models import IDModel, CreateModifyModel


class BaseModel(CreateModifyModel, IDModel):
    class Meta:
        abstract = True
