from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fields_history", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fieldshistory",
            name="history",
            field=models.JSONField(),
        ),
    ]
