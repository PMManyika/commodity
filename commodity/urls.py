from django.urls import path
from .views import (
    Logout,
    add_price_entry,
    MarketCommodityListView,
    list_commodities,
    commodity_details,
    commodity_price_entry,
    packages,
)

urlpatterns = [
    path("", list_commodities, name="list_commodities"),
    path(
        "commodity-details/<int:commodity_id>/",
        commodity_details,
        name="commodity_details",
    ),
    path("add-price-entry/", add_price_entry, name="add_price_entry"),
    path(
        "market/<str:market_name>/",
        MarketCommodityListView.as_view(),
        name="market_commodity_list",
    ),
    path("commodity/price-entry/", commodity_price_entry, name="commodity-price-entry"),
    path("packages/", packages, name="packages"),
    path("logout/", Logout, name="logout"),
]
