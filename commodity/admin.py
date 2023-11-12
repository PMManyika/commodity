from django.contrib import admin
from .models import (
    commodityType,
    Commodity,
    PriceEntry,
    Market,
    Measurement,
    MeasurementItem,
)


@admin.register(commodityType)
class CommodityTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ("name", "commodityType")
    list_filter = ("commodityType",)
    search_fields = ("name",)


@admin.register(PriceEntry)
class PriceEntryAdmin(admin.ModelAdmin):
    list_display = ("commodity", "price", "timestamp")
    list_filter = ("commodity", "timestamp")
    search_fields = ("commodity__name",)


admin.site.register(Market)
admin.site.register(Measurement)


@admin.register(MeasurementItem)
class MeasurementItemAdmin(admin.ModelAdmin):
    list_display = ("title", "section")
