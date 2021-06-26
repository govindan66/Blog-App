from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from . import models


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(label='Password',
                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username']
        widgets = {
        'first_name': forms.TextInput(attrs={'class':'form-control'}),
        'last_name': forms.TextInput(attrs={'class':'form-control'}),
        'email': forms.EmailInput(attrs={'class':'form-control'}),
        'username': forms.TextInput(attrs={'class':'form-control'})
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False,
                widget=forms.PasswordInput(attrs={'autocomplete':'current_password', 'class':'form-control'}))

class BlogsForm(forms.ModelForm):
    class Meta:
        model=models.BlogPost
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Blogs Title',
            'description': 'Blog Description',
            'image' : 'Upload a Picture',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Blog title here'}),
            'description': forms.Textarea(attrs={'placeholder':'Enter Blog description'}),
        }
