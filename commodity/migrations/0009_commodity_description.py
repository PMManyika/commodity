# Generated by Django 4.2.7 on 2023-11-12 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commodity", "0008_measurement_measurementitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="commodity",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
