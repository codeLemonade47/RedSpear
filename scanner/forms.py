from django import forms

class ScanForm(forms.Form):
    website_url = forms.URLField(label='Website URL')