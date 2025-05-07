from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EventModel

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email",required=True)
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2',]
        

class EventForm(forms.ModelForm):
    class Meta:
        model = EventModel
        fields =['title', 'description', 'event_day',]