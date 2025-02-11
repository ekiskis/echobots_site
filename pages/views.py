from django.shortcuts import render, get_object_or_404
from .models import Page, MenuList
import markdown

def home(request):
    menu_lists = MenuList.objects.prefetch_related("items").all()
    return render(request, "pages/home.html", {"menu_lists": menu_lists})

def events(request):
    menu_lists = MenuList.objects.prefetch_related("items").all()
    return render(request, "pages/events.html", {"menu_lists": menu_lists})

def about(request):
    menu_lists = MenuList.objects.prefetch_related("items").all()
    return render(request, "pages/about.html", {"menu_lists": menu_lists})

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    menu_lists = MenuList.objects.prefetch_related("items").all()

    # Если формат markdown, конвертируем в HTML
    if page.format == "markdown":
        page.content = markdown.markdown(page.content)

    return render(request, "pages/page_detail.html", {"page": page, "menu_lists": menu_lists})