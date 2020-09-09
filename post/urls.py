from django.urls import path
from post.views.create_views import PostCreateView
from post.views.delete_views import PostDeleteView
from post.views.import_views import PostImportView
from post.views.update_views import PostUpdateView

urlpatterns = [
    path('post/new', PostCreateView.as_view(), name="new"),
    path('post/<slug:title>/new/', PostCreateView.as_view(), name="new-variant"),
    path('post/<slug:title>/edit', PostUpdateView.as_view(), name="edit"),
    path('post/<slug:title>/delete', PostDeleteView.as_view(), name="delete"),
    path('post/import', PostImportView.as_view(), name="import"),

]
