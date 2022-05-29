from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets
from django.forms.widgets import PasswordInput, TextInput,DateInput,EmailInput
from .models import AlgoDetails

class AlgoDetailsForm(forms.ModelForm):
    class Meta:
        model = AlgoDetails
        fields = ('resourceType', 'resourceTitle', 'author','algorithmUsed', 'techniqueUsed', 'techniqueDescription', 'document',)