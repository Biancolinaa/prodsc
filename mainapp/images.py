import pandas as pd
import math
import matplotlib.figure as figure
import numpy as np

from django.db.models import Q, Count, Avg, StdDev
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Author, Conference, Publication, Affiliation, Paper
from .forms import UploadForm


def create_image(fig):
    resp = HttpResponse(content_type="image/png")
    fig.savefig(resp)
    return resp


def conferences_distribution(request):
    ratings = list(reversed(["A++", "A+", "A", "A-", "B", "B-"]))  # I want A++ on top
    counts = [len(Conference.objects.filter(ggs_rating=rating)) for rating in ratings]

    f = figure.Figure()
    ax = f.add_subplot()

    ax.barh(ratings, counts)

    return create_image(f)


def paper_rating_distribution(request):
    xs = []
    ys = []
    avgs = []
    ratings = ["A++", "A+", "A", "A-", "B", "B-"]
    for rating in ratings:
        papers = Paper.objects.filter(conference__ggs_rating=rating)
        avgs.append(np.mean([p.cited_by_count for p in papers]))
        for p in papers:
            xs.append(rating)
            ys.append(p.cited_by_count)

    f = figure.Figure()
    ax = f.add_subplot()
    ax.set_yscale("log")

    ax.scatter(xs, ys)
    ax.plot(ratings, avgs)

    return create_image(f)


def h_index_vs_conference_rating(request):
    data = {'h_index': [], 'ratings': []}
    for pub in Publication.objects.all():
        if pub.author.h_index > 0:
            data["h_index"].append(pub.author.h_index)
            data["ratings"].append(pub.paper.conference.ggs_rating)
    
    df = pd.DataFrame(data)
    
    ratings = ["A++", "A+", "A", "A-", "B", "B-"]
    df['ratings'] = pd.Categorical(df["ratings"], reversed(ratings))
    df.sort_values(by=['ratings'], inplace=True)
    f = figure.Figure()
    ax = f.add_subplot()
    ax.scatter(df['h_index'], df["ratings"])

    return create_image(f)
