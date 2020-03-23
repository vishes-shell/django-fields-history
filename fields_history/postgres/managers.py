from typing import Iterable, Type

from django.contrib.contenttypes.models import ContentType
from django.db import models


class FieldsHistoryManager(models.Manager):
    def get_for_model(self, obj: Type[models.Model]):
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(object_id=obj.pk, content_type=content_type)

    def get_for_model_and_field(self, obj: models.Model, field: str):
        return self.get_for_model(obj).filter(history__has_key=field)

    def get_for_model_and_fields(self, obj: models.Model, fields: Iterable[str]):
        return self.get_for_model(obj).filter(history__has_keys=fields)
