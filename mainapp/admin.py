from django.contrib import admin

from .models import Author, Affiliation, Paper, Publication, Conference

# Register your models here.

admin.site.register(Author)
admin.site.register(Affiliation)
admin.site.register(Publication)
admin.site.register(Paper)
admin.site.register(Conference)
