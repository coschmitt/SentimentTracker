from django import forms
from tweets.graphAnalysis.woied_helpers import get_filter_choices

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

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['search'].widget.attrs['class'] = 'form-control'
        self.fields['region'].widget.attrs['class'] = 'form-control'
        self.fields['result_type'].widget.attrs['class'] = 'form-control'



class TrendsFilterForm(forms.Form):
    FILTER_CHOICES = get_filter_choices()
    location = forms.ChoiceField(required=True, choices=FILTER_CHOICES)

    def __init__(self, *args, **kwargs):
        super(TrendsFilterForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs['class'] = 'form-control'


