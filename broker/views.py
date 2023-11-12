from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .models import CommodityBroker, UserReview, Broker
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, CommodityBrokerForm, BrokerForm


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def list_brokers(request):
    brokers_list = Broker.objects.all()
    # Set the number of brokers per page
    paginator = Paginator(brokers_list, 10)  # Show 10 brokers per page

    # Get the page number from the query parameters
    # If page parameter is not available, default to 1
    page = request.GET.get("page", 1)

    try:
        brokers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        brokers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        brokers = paginator.page(paginator.num_pages)

    return render(request, "broker/list_brokers.html", {"brokers": brokers})


def broker_detail(request, id):
    broker = get_object_or_404(Broker, id=id)
    reviews = UserReview.objects.filter(broker=broker)
    return render(
        request, "broker/broker_detail.html", {"broker": broker, "reviews": reviews}
    )


@login_required
def add_review(request, broker_id):
    broker = get_object_or_404(Broker, id=broker_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.broker = broker
            review.user = request.user
            review.save()
            return redirect("broker_detail", broker_id=broker_id)
    else:
        form = ReviewForm()
    return render(request, "broker/add_review.html", {"form": form, "broker": broker})


def add_broker(request, broker_id=None):
    # If broker_id is None, we're creating a new broker, otherwise we're updating
    if broker_id:
        broker = get_object_or_404(Broker, pk=broker_id)
        if request.method == "POST":
            form = BrokerForm(request.POST, instance=broker)
            if form.is_valid():
                form.save()
                return redirect(
                    "/"
                )  # Replace with the name of your view or URL where you list brokers
        else:
            form = BrokerForm(instance=broker)
    else:
        if request.method == "POST":
            form = BrokerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(
                    "/"
                )  # Replace with the name of your view or URL where you list brokers
        else:
            form = BrokerForm()

    return render(request, "broker/add_commodity_broker.html", {"form": form})
