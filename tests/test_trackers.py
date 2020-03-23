import pytest
from ddf import N

from fields_history.models import FieldsHistory

from .models import (
    CharFieldModel,
    DateFieldModel,
    DateTimeFieldModel,
    IntegerFieldModel,
    MultipleFieldModel,
)


@pytest.mark.parametrize(
    "model",
    [
        CharFieldModel,
        DateFieldModel,
        DateTimeFieldModel,
        IntegerFieldModel,
        MultipleFieldModel,
    ],
)
def test_no_changes_on_create(db, model):
    obj = N(model)
    obj.save()
    assert not FieldsHistory.objects.exists()
