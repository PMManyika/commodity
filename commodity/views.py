from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, timedelta
from django.db.models import Avg, Max, Min
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from broker.models import Broker

from .models import Commodity, PriceEntry, Market
from .forms import PriceEntryForm, MarketFilterForm


def list_commodities(request):
    # Initialize the form with data from the request
    form = MarketFilterForm(request.GET or None)
    sort = request.GET.get("sort")
    market_filter = request.GET.get("market")

    # If the form is valid and a market has been chosen, use that.
    if form.is_valid() and market_filter:
        market = Market.objects.filter(id=market_filter).first()
    else:
        market = Market.objects.first()
        market_filter = market.id  # Default to the first market's ID

    # Apply the market filter and sorting
    commodities = Commodity.objects.filter(priceentry__market=market).distinct()
    if sort == "name":
        commodities = commodities.order_by("name")
    elif sort == "type":
        commodities = commodities.order_by("commodityType__name")

    commodities_data = []
    for commodity in commodities:
        today_entries = PriceEntry.objects.filter(
            commodity=commodity, market=market, timestamp__date=date.today()
        )
        yesterday_entries = PriceEntry.objects.filter(
            commodity=commodity,
            market=market,
            timestamp__date=date.today() - timedelta(days=1),
        )

        # Fetching highest and lowest prices for today
        highest_today_price = today_entries.aggregate(Max("price"))["price__max"] or 0
        lowest_today_price = today_entries.aggregate(Min("price"))["price__min"] or 0

        # Use the latest entry for today's price
        today_price = today_entries.last().price if today_entries.exists() else 0
        yesterday_price = (
            yesterday_entries.last().price if yesterday_entries.exists() else 0
        )

        # Compute average price for today from multiple entries
        avg_today_price = today_entries.aggregate(Avg("price"))["price__avg"] or 0
        avg_previous_price = (
            yesterday_entries.aggregate(Avg("price"))["price__avg"] or 0
        )
        difference = avg_today_price - avg_previous_price
        percentage_change = (
            ((avg_today_price - avg_previous_price) / avg_previous_price) * 100
            if avg_previous_price
            else 0
        )
        avg_price = (
            PriceEntry.objects.filter(
                commodity=commodity,
                market=market,
                timestamp__date__gte=date.today() - timedelta(days=7),
            ).aggregate(Avg("price"))["price__avg"]
            or 0
        )

        trend_icon = (
            "🔼" if percentage_change > 0 else "🔽" if percentage_change < 0 else "➡️"
        )

        # Append the commodity data to the list
        commodities_data.append(
            {
                "commodity_type_name": commodity.commodityType.name,
                "commodity_id": commodity.pk,
                "name": commodity.name,
                "description": commodity.description,
                "avg_previous_price": avg_previous_price,
                "avg_today_price": avg_today_price,
                "highest_today_price": highest_today_price,
                "lowest_today_price": lowest_today_price,
                "difference": difference,
                "percentage_change": percentage_change,
                "avg_price": avg_price,
                "trend_icon": trend_icon,
            }
        )

    # Sorting the list if not already sorted by query
    if not sort:
        commodities_data.sort(key=lambda x: x["name"])

    # Pagination
    paginator = Paginator(commodities_data, 8)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    # Getting the market list for the context
    markets = Market.objects.all()

    # Define the context for rendering
    context = {
        "form": form,
        "commodities_data": page_obj,
        "markets": Market.objects.all(),
        "current_market": market_filter,  # Pass the current market ID to the template
    }

    return render(request, "commodity/index.html", context)


def commodity_details(request, commodity_id):
    # Get commodity by ID and any other related data
    commodity = get_object_or_404(Commodity, pk=commodity_id)
    # ... Fetch related data ...
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

    # Render template fragment to string
    html = render_to_string(
        "commodity/commodity_details.html", {"commodity": commodity, "brokers": brokers}
    )

    return HttpResponse(html)


def add_price_entry(request):
    if request.method == "POST":
        form = PriceEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")  # Redirect to the commodity list view
    else:
        form = PriceEntryForm()

    return render(request, "commodity/add_price_entry.html", {"form": form})


class MarketCommodityListView(ListView):
    template_name = "commodity/market_commodity_list.html"
    context_object_name = "commodities"

    def get_queryset(self):
        self.market = get_object_or_404(Market, name=self.kwargs["market_name"])
        return Commodity.objects.filter(market=self.market)

    def get_context_data(self, **kwargs):
        context = super(MarketCommodityListView, self).get_context_data(**kwargs)
        context["market"] = self.market
        return context


def commodity_price_entry(request):
    PriceEntryFormSet = modelformset_factory(
        PriceEntry, form=PriceEntryForm, extra=1
    )  # 'extra' is the number of empty forms to display
    if request.method == "POST":
        formset = PriceEntryFormSet(request.POST, queryset=PriceEntry.objects.none())
        if formset.is_valid():
            formset.save()
            return redirect("/")  # Redirect to a success page
    else:
        formset = PriceEntryFormSet(queryset=PriceEntry.objects.none())

    return render(
        request, "commodity/multiple_price_entries.html", {"formset": formset}
    )
