from datetime import datetime
from typing import Any, NamedTuple

from django.conf import settings


class FieldHistoryValue(NamedTuple):
    name: str
    value: Any
    changed_at: datetime


if "fields_history.postgres" in settings.INSTALLED_APPS:
    from fields_history.postgres.models import FieldsHistory
else:
    raise ImproperlyConfigured("Only postgres database is supported")
