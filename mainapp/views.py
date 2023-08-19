import pandas as pd
import math
from io import BytesIO

from django.db.models import Q, Count, Avg, StdDev, F
from django.shortcuts import render, get_object_or_404

from .models import Author, Conference, Publication, Affiliation, Paper
from .forms import UploadForm


def index(request):
    return render(request, "index.html")


def conferences(request):
    conferences = Conference.objects.all()
    return render(
        request,
        "conferences.html",
        {
            "conferences": conferences,
        },
    )


def affiliations(request):
    affiliations = Affiliation.objects.all()
    h_indexes_avgs = []
    for a in affiliations:
        h_index = a.publication_set.aggregate(Avg("author__h_index"))[
            "author__h_index__avg"
        ]
        h_indexes_avgs.append("{:.2f}".format(h_index) if h_index is not None else "-")
    return render(
        request,
        "affiliations.html",
        {"affiliations": zip(affiliations, h_indexes_avgs)},
    )


def authors(request):
    authors = Author.objects.all()
    return render(request, "authors.html", {"authors": authors})


def author_info(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    num_confs = {}

    for pub in author.publication_set.all():
        rating = pub.paper.conference.ggs_rating
        if rating in num_confs:
            num_confs[rating] += 1
        else:
            num_confs[rating] = 1

    return render(
        request, "author_info.html", {"author": author, "num_confs": num_confs}
    )


def conference_info(request, conference_id):
    conference = get_object_or_404(Conference, pk=conference_id)
    return render(
        request, "conference_info.html", {"conference": conference}
    )


def upload(request):
    if request.method == "GET":
        form = UploadForm()
        return render(request, "upload.html", {"form": form})

    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        auth_aff = {}
        authors_df = pd.read_csv(BytesIO(request.FILES["authors"].read()))
        papers_df = pd.read_csv(BytesIO(request.FILES["papers"].read()))
        affiliations_df = pd.read_csv(BytesIO(request.FILES["affiliations"].read()))
        conferences_df = pd.read_csv(BytesIO(request.FILES["conferences"].read()))

        for _, data in conferences_df.iterrows():
            conf = Conference(
                id=data["id"],
                name=data["title"],
                acronym=data["acronym"],
                ggs_rating=data["rating"],
                num_papers=data["num-papers"],
                citation_count=data["num-citations"],
            )
            conf.save()

        for _, data in affiliations_df.iterrows():
            aff = Affiliation(
                id=data["id"],
                name=data["affiliation_name"],
                state=data["state"],
                country=data["country"],
                author_count=data["author_count"],
                document_count=data["document_count"],
            )
            aff.save()

        for _, data in authors_df.iterrows():
            auth = Author(
                id=data["id"],
                surname=data["surname"],
                name=data["name"],
                citation_count=data["citation_count"]
                if not math.isnan(data["citation_count"])
                else 0,
                cited_by_count=data["cited_by_count"]
                if not math.isnan(data["cited_by_count"])
                else 0,
                h_index=data["h_index"] if not math.isnan(data["h_index"]) else 0,
            )
            auth.save()
            auth_aff[data["id"]] = data["affiliation_id"]

        for _, data in papers_df.iterrows():
            if data["confid"] == "-":
                continue

            conf_id = int(data["confid"])
            if not Conference.objects.filter(pk=conf_id).exists():
                continue

            paper = Paper(
                pk=data["ID"],
                title=data["Title"],
                year=data["Year"],
                source_title=data["Source title"],
                cited_by_count=data["Cited by"]
                if not math.isnan(data["Cited by"])
                else 0,
                doi=data["DOI"],
                conference=Conference.objects.get(pk=conf_id),
            )
            paper.save()

            if data["Author(s) ID"] == "[No author name available]":
                continue

            for auth_id in data["Author(s) ID"].split(";"):
                auth_id = int(auth_id)
                if not Author.objects.filter(pk=auth_id).exists():
                    continue

                aff_id = auth_aff[auth_id]
                if (
                    math.isnan(aff_id)
                    or not Affiliation.objects.filter(pk=int(aff_id)).exists()
                ):
                    continue

                affiliation = Affiliation.objects.get(pk=int(aff_id))
                author = Author.objects.get(pk=auth_id)

                pub = Publication(
                    paper=paper,
                    author=author,
                    affiliation=affiliation,
                )
                pub.save()

    return render(request, "upload.html", {"form": form})
