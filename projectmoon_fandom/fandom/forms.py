from django import forms
from .models import Anomalies

class AnomaliesForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Название")
    code = forms.CharField(max_length=20, label="Код")
    risk_level = forms.ChoiceField(choices=Anomalies.Risk_levels, label="Уровень риска")
    description = forms.CharField(widget=forms.Textarea, label="Описание")

    ego_name = forms.CharField(max_length=100, required=False, label="Название EGO")
    ego_slot = forms.CharField(max_length=50, required=False, label="Слот")
    ego_effect = forms.CharField(widget=forms.Textarea, required=False, label="Эффект")

    image_title = forms.CharField(max_length=200, required=False, label="Название изображения")
    image_file = forms.FileField(required=False, label="Файл изображения")

    class Meta:
        model = Anomalies
        fields = ['name', 'code', 'risk_level', 'description']


    def clean_code(self):
        code = self.cleaned_data.get('code')
        if Anomalies.objects.filter(code__iexact=code).exists():
            raise forms.ValidationError("Аномалия с таким кодом уже существует в базе данных!")
        return code