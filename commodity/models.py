from datetime import timedelta
from django.db import models


class Market(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class MeasurementItem(models.Model):
    section = models.ForeignKey(
        Measurement, related_name="items", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class commodityType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Commodity(models.Model):
    name = models.CharField(max_length=255)
    commodityType = models.ForeignKey(commodityType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PriceEntry(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    market = models.ForeignKey(
        Market, on_delete=models.CASCADE, related_name="commodities", null=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )  # Records the date and time of creation.

    class Meta:
        ordering = ["-timestamp"]  # To ensure latest entries appear first by default.

    def __str__(self):
        return f"{self.commodity.name} - {self.price} - {self.timestamp}"
