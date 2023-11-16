from django.db import models
from django.core.validators import RegexValidator


class NewsletterSubscription(models.Model):
    # Regex validator for mobile number (modify regex as per your requirements)
    mobile_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    mobile_number = models.CharField(
        validators=[mobile_regex], max_length=17, unique=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mobile_number
