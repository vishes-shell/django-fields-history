from importlib import import_module

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _

OBJECT_ID_TYPE_SETTING = "FIELDS_HISTORY_OBJECT_ID_TYPE_SETTING"


def init_object_id_field(object_id_class_or_tuple) -> models.fields.Field:
    if isinstance(object_id_class_or_tuple, (list, tuple)):
        object_id_class, object_id_kwargs = object_id_class_or_tuple
    else:
        object_id_class = object_id_class_or_tuple
        object_id_kwargs = {}

    if isinstance(object_id_class, str):
        try:
            module_path, class_name = object_id_class.rsplit(".", 1)
        except ValueError as err:
            raise ImportError(
                f"{object_id_class} doesn't look like a module path"
            ) from err

        module = import_module(module_path)

        object_id_class = getattr(module, class_name)

    if not issubclass(object_id_class, models.fields.Field):
        raise TypeError()
    elif not isinstance(object_id_kwargs, dict):
        raise TypeError()

    return object_id_class(db_index=True, **object_id_kwargs)


class BaseFieldsHistory(models.Model):
    object_id = init_object_id_field(
        getattr(settings, OBJECT_ID_TYPE_SETTING, models.TextField)
    )
    content_type = models.ForeignKey(
        "contenttypes.ContentType", db_index=True, on_delete=models.CASCADE
    )
    content_object = GenericForeignKey()

    changed_at = models.DateTimeField(
        verbose_name=_("changed at"), auto_now_add=True, db_index=False
    )

    class Meta:
        abstract = True
