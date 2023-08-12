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
    data = {'cited_by_count': [], 'ratings': []}
    ratings = ["A++", "A+", "A", "A-", "B", "B-"]
    for rating in ratings:
        papers = Paper.objects.filter(conference__ggs_rating=rating)
        for p in papers:
            data["cited_by_count"].append(p.cited_by_count)
            data["ratings"].append(rating)

    df = pd.DataFrame(data)
    df['ratings'] = pd.Categorical(df["ratings"], ratings)
    
    f = figure.Figure()
    ax = f.add_subplot()

    means = df.groupby('ratings')['cited_by_count'].mean()
    ax.plot(range(1, 6+1), list(means), color='red')

    ax.violinplot(
        [df[df["ratings"] == r]['cited_by_count'] for r in ratings])

    ax.set_yscale('symlog')
    ax.legend(['Media delle citazioni', 'Numero di citazioni'])

    return create_image(f)


def h_index_vs_conference_rating(request):
    data = {'h_index': [], 'ratings': []}
    for pub in Publication.objects.all():
        if pub.author.h_index > 0:
            data["h_index"].append(pub.author.h_index)
            data["ratings"].append(pub.paper.conference.ggs_rating)
    
    df = pd.DataFrame(data)
    
    ratings = ["A++", "A+", "A", "A-", "B", "B-"]
    df['ratings'] = pd.Categorical(df["ratings"], ratings)
    f = figure.Figure()
    ax = f.add_subplot()
    ax.set_xticks(range(1, 6+1))
    ax.set_xticklabels(ratings)

    means = df.groupby('ratings')['h_index'].mean()
    ax.plot(range(1, 6+1), list(means), color='red')

    ax.violinplot(
        [df[df["ratings"] == r]['h_index'] for r in ratings])

    ax.legend(['Average $h$-index', '$h$-index'])

    return create_image(f)
