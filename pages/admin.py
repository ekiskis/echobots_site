from django.contrib import admin
from .models import Page, PageBlock

class PageBlockInline(admin.TabularInline):
    model = PageBlock
    extra = 1

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PageBlockInline]
