from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import NewsletterSubscription
from django.shortcuts import render
from django.utils import timezone
from commodity.models import Commodity
from bids.models import Bid


def subscribe_to_newsletter(request):
    if request.method == "POST":
        mobile_number = request.POST.get("mobile_number")
        if mobile_number:
            # Check if the mobile number already exists in the database
            if NewsletterSubscription.objects.filter(
                mobile_number=mobile_number
            ).exists():
                messages.error(request, "This mobile number is already subscribed.")
            else:
                # Create a new NewsletterSubscription object
                subscription = NewsletterSubscription(mobile_number=mobile_number)
                subscription.save()
                # Add a success message
                messages.success(
                    request,
                    "Thank you for subscribing to our newsletter with your mobile number!",
                )

    return render(request, "libs/subscribe.html")


def profile_dashboard(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        # Redirect to login page or show an error message
        pass

    # Get all winning bids of the current user where the auction has ended
    winning_bids = Bid.objects.filter(
        user=request.user, commodity__end_time__lt=timezone.now()
    ).order_by("-commodity__end_time")

    won_commodities = [
        bid.commodity
        for bid in winning_bids
        if bid.commodity.current_price == bid.bid_amount
    ]
    # Implement pagination
    paginator = Paginator(won_commodities, 10)  # Adjust the number per page as needed
    page_number = request.GET.get("page")
    won_commodities = paginator.get_page(page_number)

    context = {"won_commodities": won_commodities}

    return render(request, "profile_dashboard.html", context)
