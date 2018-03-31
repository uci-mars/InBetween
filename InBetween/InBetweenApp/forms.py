from django import forms

class LocationAForm(forms.Form):
    loc_a = forms.CharField(label='Point A')
    loc_a.widget.attrs.update({'align': 'center'})

class LocationBForm(forms.Form):
    loc_b = forms.CharField(label='Point B')
    loc_b.widget.attrs.update({'align': 'center'})

class KeywordForm(forms.Form):
    keyword = forms.CharField(label='Keyword', required=False)
    keyword.widget.attrs.update({'align': 'center'})

