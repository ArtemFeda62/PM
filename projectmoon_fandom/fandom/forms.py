from django import forms
from .models import Anomalies, EGO, MediaFiles

class AnomaliesForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    code = forms.CharField(max_length=20)
    risk_level = forms.ChoiceField(choices=Anomalies.Risk_levels)
    description = forms.CharField(
        widget=forms.Textarea
    )

    ego_name = forms.CharField(max_length=100)
    ego_slot = forms.CharField(max_length=50)
    ego_effect = forms.CharField(
        widget=forms.Textarea
    )

    image_tittle = forms.CharField(max_length=200)
    image_file = forms.FileField()