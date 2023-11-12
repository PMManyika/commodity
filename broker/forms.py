from django import forms
from .models import UserReview, CommodityBroker, Broker


class CommodityBrokerForm(forms.ModelForm):
    class Meta:
        model = CommodityBroker
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ["review_text", "rating"]


class BrokerForm(forms.ModelForm):
    class Meta:
        model = Broker
        fields = "__all__"  # Use all the fields from the model
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "website": forms.TextInput(
                attrs={"class": "form-control"}
            ),  # If website field is supposed to be URL, use URLInput instead.
            "rating": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),  # step corresponds to decimal places
            "verified": forms.Select(
                choices=[("Yes", "Yes"), ("No", "No")], attrs={"class": "form-control"}
            ),
        }

    def clean_website(self):
        website = self.cleaned_data.get("website")
        # Add your validation for website
        return website

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        # Add your validation for rating if needed
        return rating
