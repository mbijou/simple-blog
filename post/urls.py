from django.urls import path
from post.views.create_views import PostCreateView
from post.views.delete_views import PostDeleteView
from post.views.update_views import PostUpdateView

urlpatterns = [
    path('post/new', PostCreateView.as_view(), name="new"),
    path('post/<int:pk>/edit', PostUpdateView.as_view(), name="edit"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="delete"),
]
