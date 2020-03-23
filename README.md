# django-fields-history

A Django app that track history changes in model fields.

__Important note__: currently only one implementation of `FieldsHistory`
is supported and it's with `django.contrib.postgres.fields.JSONField`
which is [`JSONB`](https://www.postgresql.org/docs/9.4/datatype-json.html)
under the hood. So only _postgresql_ as database is supported

Similar projects:

 * [django-reversion](https://github.com/etianen/django-reversion)
 * [django-simple-history](https://github.com/treyhunner/django-simple-history)
 * [django-field-history](https://github.com/grantmcconnaughey/django-field-history)

Main difference that those libraries keep track of changes, and this library
tracks the history change.

Simple explanation:

```python
from field_history.trackers import FieldsHistoryTracker

class SimpleModel(models.Model):
    field = models.CharField(max_length=50)

    field_history = FieldsHistoryTracker(fields=['field'])

obj = SimpleModel.objects.create(field='value')
assert not obj.get_field_history()


obj.field = "new_value"
obj.save()
assert obj.get_field_history()
assert obj.get_field_history()[0].value == "value"
```


## QuickStart

Install `django-fields-history`:

```bash
pip install django-fields-history
```

Add `fields_history.postgres` to `INSTALLED_APPS` (currently only
postgres implementation is supported):

```python
INSTALLED_APPS = [
    # rest of apps
    "fields_history.postgres",
]
```

And add trackers to your models and specify fields to track:

```python
from field_history.trackers import FieldsHistoryTracker

class YourModel(models.Model):
    ...

    history_tracker = FieldsHistoryTracker(fields=["field1", "field2"])
```

And you are done.


## Implementation

Every change of your fields field changes be tracked in
`fields_history.models.FieldsHistory` in:

 * `fields_history.postgres` - `JSONB` postgres field

One object per save if tracked fields has been changed.


## Credits

Basically this project is implemented based on
[django-field-history](https://github.com/grantmcconnaughey/django-field-history)
which itself used [django-model-utils](https://github.com/jazzband/django-model-utils).
