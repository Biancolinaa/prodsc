from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Author, Publication


def index(request):
    return HttpResponse("Hello World")


def author_info(request, author_id):
    author = get_object_or_404(Author, pk=author_id)

    return render(request, "author_info.html", {"author": author})
