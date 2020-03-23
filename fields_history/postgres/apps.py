from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PostgresFieldsHistoryConfig(AppConfig):
    name = "fields_history.postgres"
    label = "fields_history"
    verbose_name = _("Fields History")
