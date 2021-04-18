from django import forms
from tweets.graphAnalysis.woied_helpers import get_filter_choices

class SearchForm(forms.Form):
    REGIONS = (
        ("All regions", "All regions"),
        ('34.694910,-105.981320,450','Southwest'),
        ('37.696473,-117.139650,450','Westcoast'),
        ('41.474976,-76.508037,450','Northeast'),
        ("41.782133,-87.999337,450",'Midwest'),
        ('34.560107,-85.692607,450','South'),
        ('45.582650,-119.882060,450','Pacific Northwest'),
        ('41.672229,-108.280497,450','Rocky Mountains')
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



