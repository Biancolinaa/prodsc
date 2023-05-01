from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("author/<int:author_id>", views.author_info, name="author_info"),
    path("upload", views.upload, name="upload"),
]
