from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil



class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nome_completo = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=30, required=True)


    class Meta:
        model = User
        fields = ("nome_completo", "username", "email", "telefone", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            perfil = Perfil.objects.create(
                user=user,
                nome_completo=self.cleaned_data['nome_completo'],
                telefone=self.cleaned_data['telefone']
            )

        return user