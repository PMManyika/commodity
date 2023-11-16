from django.contrib import messages
from django.shortcuts import render, redirect
from .models import NewsletterSubscription


def subscribe_to_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            # Check if the email already exists in the database
            if NewsletterSubscription.objects.filter(email=email).exists():
                messages.error(request, "This email address is already subscribed.")
            else:
                # Create a new NewsletterSubscription object
                subscription = NewsletterSubscription(email=email)
                subscription.save()
                # Add a success message
                messages.success(
                    request, "Thank you for subscribing to our newsletter!"
                )

    return render(request, "libs/subscribe.html")
