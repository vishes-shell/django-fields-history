from uuid import uuid4

from django.db import models
from fields_history.trackers import FieldsHistoryTracker


class CharFieldModel(models.Model):
    field = models.CharField(max_length=50)

    history_tracker = FieldsHistoryTracker(fields=["field"])

    class Meta:
        app_label = "tests"


class IntegerFieldModel(models.Model):
    field = models.IntegerField()

    history_tracker = FieldsHistoryTracker(fields=["field"])

    class Meta:
        app_label = "tests"


class DateFieldModel(models.Model):
    field = models.DateField()

    history_tracker = FieldsHistoryTracker(fields=["field"])

    class Meta:
        app_label = "tests"


class DateTimeFieldModel(models.Model):
    field = models.DateTimeField()

    history_tracker = FieldsHistoryTracker(fields=["field"])

    class Meta:
        app_label = "tests"


class MultipleFieldModel(models.Model):
    first_field = models.CharField(max_length=50)
    second_field = models.CharField(max_length=50)

    history_tracker = FieldsHistoryTracker(fields=["first_field", "second_field"])

    class Meta:
        app_label = "tests"


class OneOfManyTrackedFieldModel(models.Model):
    tracked = models.CharField(max_length=50)
    not_tracked = models.CharField(max_length=50)

    history_tracker = FieldsHistoryTracker(fields=["tracked"])

    class Meta:
        app_label = "tests"
