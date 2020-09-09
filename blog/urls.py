from django.urls import path

from blog.views.export_views import PostExportView
from blog.views.list_views import PostListView
from blog.views.detail_views import PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name="blog"),
    path('<slug:title>/', PostDetailView.as_view(), name="post-detail"),
    path('<slug:title>/export/json', PostExportView.as_view(), name="post-export")
]
