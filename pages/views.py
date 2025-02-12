from django.shortcuts import render, get_object_or_404
from .models import Page, MenuList, MenuItem
import markdown

def home(request):
    menu_lists = MenuList.objects.prefetch_related("items").all()
    menu_items = MenuItem.objects.all().order_by('order')
    return render(request, "pages/home.html", {"menu_lists": menu_lists, "menu_items": menu_items})

def events(request):
    menu_lists = MenuList.objects.prefetch_related("items").all()
    menu_items = MenuItem.objects.all().order_by('order')
    return render(request, "pages/events.html", {"menu_lists": menu_lists, "menu_items": menu_items})

def about(request):
    menu_lists = MenuList.objects.prefetch_related("items").all()
    menu_items = MenuItem.objects.all().order_by('order')
    return render(request, "pages/about.html", {"menu_lists": menu_lists, "menu_items": menu_items})

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    menu_lists = MenuList.objects.prefetch_related("items").all()
    menu_items = MenuItem.objects.all().order_by('order')

    if page.format == "markdown":
        page.content = markdown.markdown(page.content)

    return render(request, "pages/page_detail.html", {
        "page": page, 
        "menu_lists": menu_lists,
        "menu_items": menu_items
    })