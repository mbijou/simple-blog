from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from account.forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy("frontpage:frontpage")
