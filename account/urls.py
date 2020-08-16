from django.urls import path, include
from account.views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('accounts/login/', CustomLoginView.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
]
