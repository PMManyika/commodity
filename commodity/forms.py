from django import forms
from .models import Commodity, PriceEntry, Market


class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ["name", "commodityType", "description"]


class PriceEntryForm(forms.ModelForm):
    class Meta:
        model = PriceEntry
        fields = ["commodity", "price", "market"]

    # Optionally, you might want to initialize the commodity field with only active commodities or some other subset
    def __init__(self, *args, **kwargs):
        super(PriceEntryForm, self).__init__(*args, **kwargs)
        self.fields["commodity"].queryset = Commodity.objects.all().order_by("name")


class MarketFilterForm(forms.Form):
    market = forms.ModelChoiceField(
        queryset=Market.objects.all(),
        required=False,
        label="Select a market to filter by:",
        empty_label="All Markets",
    )

    def __init__(self, *args, **kwargs):
        initial_market = kwargs.pop("initial_market", None)
        super(MarketFilterForm, self).__init__(*args, **kwargs)
        if initial_market:
            self.fields["market"].initial = initial_market
