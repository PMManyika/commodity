from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Commodity, Bid, BiddingSession, CommodityImage
from django.utils import timezone
from libs.forms import NewsletterSubscriptionForm
from libs.models import NewsletterSubscription


def commodity_list(request):
    commodities_list = Commodity.objects.filter(end_time__gte=timezone.now()).order_by(
        "-id"
    )

    items_per_page = 10
    paginator = Paginator(commodities_list, items_per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
    }

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

    return render(request, "bids/commodity_list.html", context)


def commodity_detail(request, commodity_id):
    commodity = get_object_or_404(Commodity, pk=commodity_id)

    # Fetch all products from the same broker except the current one
    related_products = Commodity.objects.filter(broker=commodity.broker).exclude(
        pk=commodity_id
    )

    bids = Bid.objects.filter(commodity=commodity).order_by("-bid_time")[:12]
    bid_count = Bid.objects.filter(commodity=commodity).count()

    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            if NewsletterSubscription.objects.filter(email=email).exists():
                messages.error(request, "This email address is already subscribed.")
            else:
                subscription = NewsletterSubscription(email=email)
                subscription.save()
                messages.success(
                    request, "Thank you for subscribing to our newsletter!"
                )

    # Fetch all images associated with the commodity
    commodity_images = CommodityImage.objects.filter(commodity=commodity)

    # Initialize winning_bid as None
    winning_bid = None

    # Fetch the highest bid for this commodity
    # winning_bid = (
    #     Bid.objects.filter(commodity=commodity).order_by("-bid_amount").first()
    # )

    # Initialize variables
    user_is_winner = False
    if (
        winning_bid
        and winning_bid.user == request.user
        and commodity.end_time < timezone.now()
    ):
        user_is_winner = True

    # Determine if the auction has ended
    if commodity.end_time < timezone.now():
        # Fetch the highest bid for this commodity
        highest_bid = (
            Bid.objects.filter(commodity=commodity).order_by("-bid_amount").first()
        )

        # Check if the current user is the seller
        if request.user == commodity.broker.user:
            winning_bid = highest_bid

    # Initialize context
    context = {
        "commodity": commodity,
        "related_products": related_products,
        "bidding_session": commodity.end_time,
        "bids": bids,
        "bid_count": bid_count,
        "commodity_images": commodity_images,
        "user_is_winner": user_is_winner,
        "winning_bid": winning_bid,
    }

    return render(request, "bids/commodity_detail.html", context)


@login_required
def place_bid(request, commodity_id):
    commodity = get_object_or_404(Commodity, pk=commodity_id)

    if request.method == "POST":
        bid_amount = request.POST["bid_amount"]
        if float(bid_amount) > commodity.current_price:
            bid = Bid(user=request.user, commodity=commodity, bid_amount=bid_amount)
            bid.save()
            commodity.current_price = bid_amount
            commodity.save()

    # Redirect back to the previous page (current page)
    return redirect(request.META.get("HTTP_REFERER", ""))


def bidding_sessions(request):
    sessions = BiddingSession.objects.filter(end_time__gte=timezone.now())
    return render(request, "bids/bidding_sessions.html", {"sessions": sessions})
