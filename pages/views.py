from django.shortcuts import render, get_object_or_404
from .models import Page

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def events(request):
    return render(request, 'pages/events.html')

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, "pages/page_detail.html", {"page": page})