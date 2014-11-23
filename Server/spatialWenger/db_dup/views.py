from django.shortcuts import render

# Create your views here.

def home_view(req):
    return render(req, 'index.html', {'page_title': 'Dog',})


