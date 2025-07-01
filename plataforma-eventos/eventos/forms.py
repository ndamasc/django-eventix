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

    def __init__(self, *args, **kwargs):
        self.usuario_atual = kwargs.pop('instance', None)
        super().__init__(*args, instance=self.usuario_atual, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.pk if self.instance else None

        if User.objects.exclude(pk=user_id).filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_id = self.instance.pk if self.instance else None
        
        if User.objects.exclude(pk=user_id).filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

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
    

class EditarPerfilForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']



class EditarDadosComplementaresForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome_completo', 'telefone']