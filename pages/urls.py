from django.urls import path
from .views import home, events, about, page_detail

urlpatterns = [
    path("", home, name="home"),
    path("events/", events, name="events"),
    path("about/", about, name="about"),
    path("page/<slug:slug>/", page_detail, name="page_detail"),
]
