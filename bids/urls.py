from django.urls import path
from . import views

urlpatterns = [
    path("", views.commodity_list, name="commodity_list"),
    path(
        "commodity/<int:commodity_id>/", views.commodity_detail, name="commodity_detail"
    ),
    path("commodity/<int:commodity_id>/place_bid/", views.place_bid, name="place_bid"),
    path("bidding_sessions/", views.bidding_sessions, name="bidding_sessions"),
]
