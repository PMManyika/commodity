from django.contrib import admin
from .models import Commodity, Bid, BiddingSession, CommodityImage


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ("name", "broker", "current_price", "end_time")
    list_filter = ("end_time",)
    search_fields = ("name", "description")


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "commodity", "bid_amount", "bid_time")
    list_filter = ("bid_time",)
    search_fields = ("user__username", "commodity__name")


@admin.register(BiddingSession)
class BiddingSessionAdmin(admin.ModelAdmin):
    list_display = ("commodity", "start_time", "end_time")
    list_filter = ("end_time",)
    search_fields = ("commodity__name",)


@admin.register(CommodityImage)
class CommodityImageAdmin(admin.ModelAdmin):
    list_display = ("commodity", "image", "broker")
    list_filter = ("commodity__name",)
    search_fields = ("commodity__name",)
