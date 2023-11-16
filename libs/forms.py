from django import forms


class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
                "required": True,
            }
        ),
    )
