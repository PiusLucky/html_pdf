#forms.py
import re

from django import forms
from main.models import URL

class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = (
            "url",
        )