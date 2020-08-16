from django.contrib.auth.forms import AuthenticationForm
from blog.base_forms import BootstrapForm


class CustomAuthenticationForm(BootstrapForm, AuthenticationForm):
    pass


