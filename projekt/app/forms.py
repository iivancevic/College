from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from app import forms
from .models import *

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Korisnik
        fields = ("username", "email", "status", "uloga", "password1", "password2")

class SubjectForm(ModelForm):
    class Meta:
        model = Predmet
        fields = {"ime", "kod", "program", "ects", "sem_red", "sem_izv", "izborni", "nositelj"}
    
    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields.get('nositelj').queryset = Korisnik.objects.filter(uloga=3)
        
    
class UserForm(ModelForm):
    class Meta:
        model = Korisnik
        fields = ("username", "email", "status", "uloga")
