from django.urls import path

from . import views, images

urlpatterns = [
    path("", views.index, name="index"),
    path("authors", views.authors, name="authors"),
    path("author/<int:author_id>", views.author_info, name="author_info"),
    path("upload", views.upload, name="upload"),
    path("conferences", views.conferences, name="conferences"),
    path("conference/<int:conference_id>", views.conference_info, name="conference_info"),
    path("affiliations", views.affiliations, name="affiliations"),
    path(
        "conferences/distribution.png",
        images.conferences_distribution,
        name="conferences_distribution.png",
    ),
    path(
        "conferences/paper_rating_distribution.png",
        images.paper_rating_distribution,
        name="paper_rating_distribution.png",
    ),
    path(
        "conferences/paper_rating_distribution_impact.png",
        images.paper_rating_distribution_impact,
        name="paper_rating_distribution_impact.png",
    ),
    path(
        "conferences/h_index_vs_conference_rating.png",
        images.h_index_vs_conference_rating,
        name="h_index_vs_conference_rating"
    ),
    path(
        "affiliations/num_authors_per_country.png",
        images.num_authors_per_country,
        name="num_authors_per_country"
    ),
    path(
        "affiliations/num_documents_per_country.png",
        images.num_documents_per_country,
        name="num_documents_per_country"
    ),
    path(
        "affiliations/productivity_per_country.png",
        images.productivity_per_country,
        name="productivity_per_country"
    ),
    path(
        "authors/author_citations_vs_affiliation_size.png",
        images.author_citations_vs_affiliation_size,
        name="author_citations_vs_affiliation_size"
    ),
    path(
        "authors/author_h_index_vs_affiliation_size.png",
        images.author_h_index_vs_affiliation_size,
        name="author_h_index_vs_affiliation_size"
    )
]
