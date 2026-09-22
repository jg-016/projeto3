from django import forms
from django.contrib.auth.models import User
from ..models import Usuario


class UserUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['usuario', 'perfil', 'aniversario']
        widgets = {
            'usuario': forms.HiddenInput(),
            'perfil': forms.Select(attrs={'class': 'form-select'}),
            'aniversario': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        if current_user is not None and not (current_user.is_staff or current_user.is_superuser):
            self.fields.pop('perfil', None)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
