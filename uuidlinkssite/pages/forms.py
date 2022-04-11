from django import forms
from .models import Page


class PageForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())


class CreatePage(forms.Form):
    title = forms.CharField(required=False, max_length=100)
    template = forms.CharField(
        required=True,
        max_length=1000,
        widget=forms.Textarea(attrs={"rows": 20, "cols": 40}),
    )
    password = forms.CharField(required=True, widget=forms.PasswordInput())
