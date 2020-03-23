from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields.jsonb import KeyTransform
from django.db import models
from django.utils.translation import gettext_lazy as _

from fields_history.base import BaseFieldsHistory

from .managers import FieldsHistoryManager


class FieldsHistoryQuerySet(models.QuerySet):
    def only_value_and_changed_at(self, field: str):
        return self.annotate(value=KeyTransform(field, "history")).values_list(
            "value", "changed_at"
        )


class FieldsHistory(BaseFieldsHistory):
    history = JSONField(verbose_name=_("history"))

    objects = FieldsHistoryManager.from_queryset(FieldsHistoryQuerySet)()

    class Meta:
        get_latest_by = "changed_at"

    def __str__(self):
        return f"{self.history.keys()} are changed for {self.content_object}"
