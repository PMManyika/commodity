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

from .models import Commodity, PriceEntry, Market
from .forms import PriceEntryForm, MarketFilterForm


def list_commodities(request):
    # Initialize the form with data from the request
    form = MarketFilterForm(request.GET or None)
    market_name = request.GET.get(
        "market"
    )  # Get the market ID from the query parameters

    # If the form is valid and a market has been chosen, use that. Otherwise, default to 1.
    if form.is_valid():
        market_name = form.cleaned_data.get("market") or 1
    else:
        market_name = "Mbare Musika"

    # Get the market instance if it exists, otherwise default to the first market
    market = Market.objects.filter(name=market_name).first() or Market.objects.first()

    sort_by_type = request.GET.get("sort") == "type"
    commodities = (
        Commodity.objects.filter(priceentry__market=market).distinct()
        if market
        else Commodity.objects.all()
    )

    if market:
        commodities = Commodity.objects.filter(priceentry__market=market).distinct()
    else:
        commodities = Commodity.objects.all()

    commodities_data = []

    for commodity in commodities:
        # Get price entries for today and yesterday
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
                "name": commodity.name,
                "avg_previous_price": avg_previous_price,
                "avg_today_price": avg_today_price,
                "highest_today_price": highest_today_price,
                "lowest_today_price": lowest_today_price,
                "difference": difference,
                "percentage_change": percentage_change,
                "avg_price": avg_price,
                "trend_icon": trend_icon,
                "selected_market_id": market_name,
            }
        )

    # Sorting the list of dictionaries by 'commodity_type_name' or 'name'
    if sort_by_type:
        commodities_data.sort(key=lambda x: x["commodity_type_name"])
    else:
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
        "markets": markets,
    }

    return render(request, "commodity/index.html", context)


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
