from django import forms
from ..models import Fabricante


class FabricanteForm(forms.ModelForm):
    class Meta:
        model = Fabricante
        fields = ['fabricante']
        widgets = {
            'fabricante': forms.TextInput(attrs={'class': 'form-control'}),
        }
