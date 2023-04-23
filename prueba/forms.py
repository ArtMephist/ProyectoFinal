from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from .models import Login_Account,Register_Account, Post, User, Message, Avatar
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

def search(request):
    search_query = request.GET.get('search_query')
    # Aquí implemente su lógica de búsqueda
    return render(request, 'search_results.html', {'search_query': search_query})


class SearchForm(forms.Form):
    name = forms.CharField()
    ingredients = forms.CharField()
    description = forms.CharField()



class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    

    class Meta:
        model = Register_Account
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class Login_account_Form(forms.ModelForm):
    class Meta:
        username = forms.CharField(max_length=50)
        password = forms.CharField(max_length=50)
        model = Login_Account
        fields = "__all__"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','subtitle','description','image']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Register_Account
        fields = ['username','email','password']
        exclude = ['last_login', 'last_name','first_name']

class AvatarChange(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image']

class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), empty_label='Choose a user')

    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }