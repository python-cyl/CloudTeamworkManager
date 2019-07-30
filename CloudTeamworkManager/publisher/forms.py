from django import forms


class comment(forms.Form):
    content = forms.CharField(max_length = 200)
