from django.shortcuts import render_to_response
from models import *

def view_blogpost(request, id):
    blogpost = Blogpost.objects.get(id=int(id))
    return render_to_response("blogpost.html", { 'blogpost' : blogpost })
