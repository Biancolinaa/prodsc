import pandas as pd
from io import BytesIO

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Author, Publication
from .forms import UploadForm


def index(request):
    return HttpResponse("Hello World")


def author_info(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "author_info.html", {"author": author})


def upload(request):
    if request.method == "GET":
        form = UploadForm()
    elif request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            authors_df = pd.read_csv(BytesIO(request.FILES["authors"].read()))
            papers_df = pd.read_csv(BytesIO(request.FILES["papers"].read()))
            affiliations_df = pd.read_csv(BytesIO(request.FILES["affiliations"].read()))
            conferences_df = pd.read_csv(BytesIO(request.FILES["conferences"].read()))

            print(authors_df)
            print(papers_df)
            print(affiliations_df)
            print(conferences_df)

    return render(request, "upload.html", {"form": form})
