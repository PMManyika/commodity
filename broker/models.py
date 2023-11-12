from django.db import models
from django.contrib.auth.models import User


class CommodityBroker(models.Model):
    # Basic Information
    name = models.CharField(max_length=255)
    license_details = models.TextField(null=True, blank=True)
    regulation_details = models.TextField(null=True, blank=True)
    platforms = models.CharField(
        max_length=255, null=True, blank=True
    )  # If there are multiple platforms, consider using a ManyToMany field

    # Fees and Commissions
    fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commissions = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Available Commodities
    AVAILABLE_COMMODITIES_CHOICES = (
        ("metals", "Metals"),
        ("agriculture", "Agriculture"),
        ("energy", "Energy"),
        # Add more as needed
    )
    commodities = models.ManyToManyField("CommodityType", blank=True)

    # Ratings & Reviews (assuming a scale of 1-5, adjust as needed)
    customer_service_rating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, blank=True
    )
    overall_rating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Broker(models.Model):
    # Basic Information
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    website = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    verified = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CommodityType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)  # Added timestamp field

    def __str__(self):
        return f"Review by {self.user} for {self.broker}"
