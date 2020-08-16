from django.contrib.auth.views import LoginView
from django.shortcuts import render

# Create your views here.
from account.forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
