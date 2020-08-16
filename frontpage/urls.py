from django.urls import path
from django.views.generic import TemplateView

from frontpage.views import CustomLoginView

urlpatterns = [
    path('', TemplateView.as_view(template_name="frontpage/index.html"), name="frontpage"),
    path('login', CustomLoginView.as_view(template_name="frontpage/login.html"), name="login"),
]
