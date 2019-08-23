from apps.base.models.UUID_model import UUIDAbstractModel
from apps.base.models.timestamped_model import TimestampModel


class BaseModel(TimestampModel, UUIDAbstractModel):
    class Meta:
        abstract = True
