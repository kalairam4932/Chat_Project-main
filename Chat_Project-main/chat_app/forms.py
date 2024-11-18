from django import forms
from .models import UserAccount

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta: 
        model = UserAccount
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
    
    class Meta:
        model = UserAccount
        exclude = ['is_active']

class RoomForm(forms.Form):
    """
    Normal form, not connected to models.
    """
    room_name = forms.CharField()