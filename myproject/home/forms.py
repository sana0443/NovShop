from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import profile
from django.forms import TextInput

class SignUpForm(UserCreationForm):
    name=forms.CharField(label=("Full Name"))
    username=forms.EmailField(label=("Email"))
    class Meta:
        model=User
        fields=('name','username','password1','password2')


    
class UserUpdate(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username']
        widgets={
            'first_name':TextInput(attrs={
            'class':'form-control',
            'style': 'max-width: 100%'
            }),
            'email':TextInput(attrs={
            'class':'form-control',
            'style': 'max-width: 100%'
            }),
            'username':TextInput(attrs={
            'class':'form-control',
            'style': 'max-width: 100%'
            })
        }

class profileUpdate(forms.ModelForm):
    class Meta:
        model=profile
        fields=['name','phone','address','postcode','state','email','country','phone2','image','primary_address','city']
        
        widgets={
            'phone':TextInput(attrs={
            'class':'form-control',
            'style': 'max-width: 100%'
            }),
            'address':TextInput(attrs={
            'class':'form-control',
            'style': 'max-width: 100%'
            }),
            'postcode':TextInput(attrs={
            'class':'form-control',
            'style': 'max-width: 100%'
            }),
            'state':TextInput(attrs={
            'class':'form-control',
            'style': 'max-width: 100%'
            }),
            'country':TextInput(attrs={
            'class':'form-control',
            'style': 'max-width: 100%'
            }),
            'city':TextInput(attrs={
            'class':'form-control',
            'style': 'max-width: 100%'
            }),
             'name':TextInput(attrs={
            'class':'form-control',
            'style': 'max-width: 100%'
            }),
            
        }


