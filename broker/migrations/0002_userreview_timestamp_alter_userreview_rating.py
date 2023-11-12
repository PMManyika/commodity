# Generated by Django 4.2.7 on 2023-11-03 21:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("broker", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userreview",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="userreview",
            name="rating",
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
    ]
