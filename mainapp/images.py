import pandas as pd
import matplotlib.figure as figure
import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.db.models import Sum, F, ExpressionWrapper, FloatField

from .models import Author, Conference, Publication, Affiliation, Paper


def create_image(fig):
    resp = HttpResponse(content_type="image/png")
    fig.savefig(resp)
    return resp

# ------------ Conference metrics


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

# ------------ Affiliation metrics


def num_authors_per_country(request):
    f = figure.Figure()
    ax = f.add_subplot()

    qs = Affiliation.objects.values("country").annotate(num_authors=Sum("author_count")).order_by("-num_authors")
    xs = []
    ys = []
    for aff in qs[:10]:
        xs.append(aff['country'])
        ys.append(aff['num_authors'])

    bars = ax.bar(xs, ys)
    ax.bar_label(bars, labels=[f'{x / 1e6:.2f}e6' for x in ys])
    ax.set_xticks(xs, labels=xs, rotation=45, ha='right')
    f.tight_layout()

    return create_image(f)


def num_documents_per_country(request):
    f = figure.Figure()
    ax = f.add_subplot()

    qs = Affiliation.objects.values("country").annotate(num_docs=Sum("document_count")).order_by("-num_docs")
    xs = []
    ys = []
    for aff in qs[:10]:
        xs.append(aff['country'])
        ys.append(aff['num_docs'])

    bars = ax.bar(xs, ys)
    ax.bar_label(bars, labels=[f'{x / 1e6:.2f}e6' for x in ys])
    ax.set_xticks(xs, labels=xs, rotation=45, ha='right')
    f.tight_layout()

    return create_image(f)


def productivity_per_country(request):
    f = figure.Figure()
    ax = f.add_subplot()

    qs = Affiliation.objects.values("country") \
        .annotate(
            num_docs=Sum("document_count"),
            num_authors=Sum("author_count"),
            # The * 1.0 is to convert to float
            productivity=ExpressionWrapper(F('num_authors') * 1.0 / F('num_docs'), output_field=FloatField())) \
        .order_by("-productivity")

    countries = [aff['country'] for aff in Affiliation.objects.values("country")
                 .annotate(num_docs=Sum("document_count"))
                 .order_by("-num_docs")[:10]]
    countries += [aff['country'] for aff in Affiliation.objects.values("country")
                  .annotate(num_authors=Sum("author_count"))
                  .order_by("-num_authors")[:10]]
    xs = []
    ys = []
    for aff in qs:
        if aff['country'] in countries:
            xs.append(aff['country'])
            ys.append(aff['productivity'])
            print(aff)

    bars = ax.bar(xs, ys)
    ax.bar_label(bars, labels=[f'{y:.2f}' for y in ys])
    ax.set_xticks(xs, labels=xs, rotation=45, ha='right')
    f.tight_layout()

    return create_image(f)
