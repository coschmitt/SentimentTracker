from django import forms


class SearchForm(forms.Form):
    REGIONS = (
        ("All regions", "All regions"),
        ('Southwest', 'Southwest'),
        ('Westcoast', 'Westcoast'),
        ('Eastcoast', 'Eastcoast'),
        ('Midwest', 'Midwest'),
        ('South', 'South'),
        ('Northeast', 'Northeast'),
        ('Pacific Northwest', 'Pacific Northwest'),
        ('Rocky Mountains', 'Rocky Mountains')
    )

    TWEET_TYPES = (
        ('Mixed', 'Mixed'),
        ('Most popular', 'Most popular'),
        ('Most recent', 'Most recent')
    )

    search = forms.CharField(required=True)
    region = forms.ChoiceField(choices=REGIONS, required=False)
    end_date = forms.DateField(
        input_formats=['%Y/%m/%d'], label="End date (default today): ", required=False
    )
    result_type = forms.ChoiceField(choices=TWEET_TYPES)

