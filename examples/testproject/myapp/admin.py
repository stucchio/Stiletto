from django.contrib import admin
from models import *

class BlogpostAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Blogpost, BlogpostAdmin)
