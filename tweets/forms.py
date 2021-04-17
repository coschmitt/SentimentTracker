from django import forms


class SearchForm(forms.Form):
    REGIONS = (
        ("All regions", "All regions"),
        ('Southwest', '34.694910,-105.981320,450'),
        ('Westcoast', '37.696473,-117.139650,450'),
        ('Northeast', '41.474976,-76.508037,450'),
        ('Midwest', "41.782133,-87.999337,450"),
        ('South', '34.560107,-85.692607,450'),
        ('Pacific Northwest', '45.582650,-119.882060,450'),
        ('Rocky Mountains', '41.672229,-108.280497,450')
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


