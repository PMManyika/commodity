# Generated by Django 4.2.7 on 2023-11-11 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("commodity", "0005_remove_commodity_market_priceentry_market"),
    ]

    operations = [
        migrations.AddField(
            model_name="commodity",
            name="unit_of_measurement",
            field=models.CharField(
                choices=[
                    ("kg", "Kilogram"),
                    ("g", "Gram"),
                    ("lb", "Pound"),
                    ("bag", "Bag"),
                    ("bushel", "Bushel"),
                    ("crate", "Crate"),
                ],
                default="kg",
                help_text="Unit of measurement for this commodity",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="priceentry",
            name="quantity",
            field=models.DecimalField(
                decimal_places=2,
                default=1,
                help_text="Quantity of commodity in the specified unit of measurement",
                max_digits=10,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="priceentry",
            name="market",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="price_entries",
                to="commodity.market",
            ),
            preserve_default=False,
        ),
    ]