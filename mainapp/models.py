from django.db import models


# Create your models here.
class Author(models.Model):
    surname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    citation_count = models.IntegerField()
    cited_by_count = models.IntegerField()
    h_index = models.IntegerField()


class Conference(models.Model):
    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=200)
    ggs_rating = models.CharField(max_length=5)
    num_papers = models.IntegerField()
    citation_count = models.IntegerField()


class Paper(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    source_title = models.CharField(max_length=200)
    cited_by_count = models.IntegerField()
    doi = models.CharField(max_length=200)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)


class Affiliation(models.Model):
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    author_count = models.IntegerField()
    document_count = models.IntegerField()


class Publication(models.Model):
    affiliation = models.ForeignKey(Affiliation, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["affiliation", "paper", "author"], name="publication_unique"
            )
        ]
