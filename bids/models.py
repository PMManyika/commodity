from django.db import models
from django.contrib.auth.models import User
from broker.models import Broker


class Commodity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    end_time = models.DateTimeField()
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class CommodityImage(models.Model):
    commodity = models.ForeignKey(
        Commodity, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="commodity_images/")
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.commodity.name}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.commodity.name} - ${self.bid_amount}"


class BiddingSession(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Bidding Session for {self.commodity.name}"
