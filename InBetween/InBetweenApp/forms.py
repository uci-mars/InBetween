from django import forms

class LocationAForm(forms.Form):
    loc_a = forms.CharField(label='')
    loc_a.widget.attrs.update({'id': 'search_termA','align': 'center', 'placeholder':'Enter your address'})

class LocationBForm(forms.Form):
    loc_b = forms.CharField(label='')
    loc_b.widget.attrs.update({'id': 'search_termB','align': 'center', 'placeholder':'Enter other address'})

class KeywordForm(forms.Form):
    keyword = forms.CharField(label='', required=False)
    keyword.widget.attrs.update({'align': 'center', 'placeholder':'FIND tacos, cafe, donut, sushi, etc.'})
