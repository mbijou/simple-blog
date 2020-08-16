from django.urls import path
from content.views.create_views import ContentCreateView
from content.views.update_views import ContentUpdateView
from content.views.delete_views import ContentDeleteView


urlpatterns = [
    path('post/<int:pk>/content/<int:content_pk>/edit', ContentUpdateView.as_view(), name="edit"),
    path('post/<int:pk>/content/new', ContentCreateView.as_view(), name="new"),
    path('post/<int:pk>/delete/<int:content_pk>/delete', ContentDeleteView.as_view(), name="delete"),
]
