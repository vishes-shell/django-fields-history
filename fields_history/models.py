from datetime import datetime
from typing import Any, NamedTuple

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import FieldsHistoryManager


class FieldHistoryValue(NamedTuple):
    name: str
    value: Any
    changed_at: datetime


OBJECT_ID_TYPE_SETTING = "FIELDS_HISTORY_OBJECT_ID_TYPE_SETTING"


def _init_object_id_field(object_id_class_or_tuple) -> models.fields.Field:
    if isinstance(object_id_class_or_tuple, (list, tuple)):
        object_id_class, object_id_kwargs = object_id_class_or_tuple
    else:
        object_id_class = object_id_class_or_tuple
        object_id_kwargs = {}

    if not issubclass(object_id_class, models.fields.Field):
        raise TypeError()
    elif not isinstance(object_id_kwargs, dict):
        raise TypeError()

    return object_id_class(db_index=True, **object_id_kwargs)


class FieldsHistory(models.Model):
    object_id = _init_object_id_field(
        getattr(settings, OBJECT_ID_TYPE_SETTING, models.TextField)
    )
    content_type = models.ForeignKey(
        "contenttypes.ContentType", db_index=True, on_delete=models.CASCADE
    )
    content_object = GenericForeignKey()

    history = JSONField(verbose_name=_("history"))

    changed_at = models.DateTimeField(
        verbose_name=_("changed at"), auto_now_add=True, db_index=False
    )

    objects = FieldsHistoryManager()

    class Meta:
        app_label = "fields_history"
        get_latest_by = "changed_at"

    def __str__(self):
        return f"{self.changes.keys()} are changed for {self.content_object}"
