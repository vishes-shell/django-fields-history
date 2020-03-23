from copy import deepcopy
from functools import partialmethod
from typing import Any, Callable, Dict, Iterable, List, Optional, Type

from django.contrib.postgres.fields.jsonb import KeyTransform
from django.db import models

from .models import FieldHistoryValue, FieldsHistory


def _get_field_history(
    obj: models.Model, field: str, **filter_kwargs
) -> List[FieldHistoryValue]:
    to_python: Callable[[str], Any] = obj._meta.get_field(obj).to_python

    qs = (
        FieldsHistory.objects.get_for_model_and_field(obj, field)
        .filter(**filter_kwargs)
        .annotate(value=KeyTransform(field, "history"))
        .values_list("value", "changed_at")
    )

    return [
        FieldHistoryValue(name=field, value=to_python(value), changed_at=changed_at)
        for value, changed_at in qs
    ]


class FieldInstanceTracker:
    def __init__(self, obj: models.Model, fields: Iterable[str]) -> None:
        self.obj = obj
        self.fields = fields

    def get_field_value(self, field: str) -> Any:
        return getattr(self.obj, field)

    def set_saved_fields(self, fields: Optional[Iterable[str]] = None) -> None:
        if self.obj._state.adding:
            self._saved_data: Dict[str, Any] = {}
        elif not fields:
            self._saved_data = self.current()

        # preventing mutable fields side effects
        for field, field_value in self._saved_data.items():
            self._saved_data[field] = deepcopy(field_value)

    def current(self, fields: Optional[Iterable[str]] = None) -> Dict[str, Any]:
        """Returns dict of current values for all tracked fields
        """
        if fields is None:
            fields = self.fields

        return {f: self.get_field_value(f) for f in fields}

    def has_changed(self, field: str) -> bool:
        """Returns ``True`` if field has changed from currently saved value"""
        return self.previous(field) != self.get_field_value(field)

    def previous(self, field: str) -> Optional[Any]:
        """Returns currently saved value of given field
        """
        return self._saved_data.get(field)


class FieldsHistoryTracker:
    tracker_class = FieldInstanceTracker

    def __init__(self, fields: Iterable[str]):
        self.fields = set(fields)

    def contribute_to_class(self, cls: Type[models.Model], name: str) -> None:
        setattr(cls, "_get_field_history", _get_field_history)
        for field in self.fields:
            setattr(
                cls,
                f"get_{field}_history",
                partialmethod(_get_field_history, field=field),
            )
        self.name = name
        self.attname = f"_{self.name}"
        models.signals.class_prepared.connect(self.finalize_class, sender=cls)

    def finalize_class(self, sender: Type[models.Model], **kwargs) -> None:
        models.signals.post_init.connect(self.init_tracker)
        self.model_class = sender
        setattr(sender, self.name, self)

    def _init_tracker(self, instance):
        tracker = self.tracker_class(instance, self.fields)
        setattr(instance, self.attname, tracker)
        tracker.set_saved_fields()

    def init_tracker(self, sender, instance, **kwargs):
        if not isinstance(instance, self.model_class):
            return  # Only init instances of given model (including children)
        self._init_tracker(instance)
        self._patch_save(instance)

    def _patch_save(self, obj):
        original_save = obj.save

        def save(**kwargs):
            ret = original_save(**kwargs)
            tracker = getattr(obj, self.attname)

            changes = {}
            for field in self.fields:
                if obj._state.adding or not tracker.has_changed(field):
                    continue

                value_to_string: Callable[[Any], str] = obj._meta.get_field(
                    field
                ).value_to_string

                changes[field] = value_to_string(getattr(obj, field))

            if changes:
                FieldsHistory.objects.create(content_object=obj, changes=changes)

            self._init_tracker(obj)

            return ret

        obj.save = save
