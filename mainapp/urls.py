from django.urls import path

from . import views, images

urlpatterns = [
    path("", views.index, name="index"),
    path("authors", views.authors, name="authors"),
    path("author/<int:author_id>", views.author_info, name="author_info"),
    path("upload", views.upload, name="upload"),
    path("conferences", views.conferences, name="conferences"),
    path("affiliations", views.affiliations, name="affiliations"),
    path(
        "conferences/distribution.png",
        images.conferences_distribution,
        name="conferences_distribution.png",
    ),
    path(
        "papers/paper_rating_distribution.png",
        images.paper_rating_distribution,
        name="paper_rating_distribution.png",
    ),
]
