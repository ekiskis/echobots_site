from django.contrib import admin
from django.utils.html import format_html
from .models import *
import os
from django.conf import settings


class PageBlockInline(admin.TabularInline):
    model = PageBlock
    extra = 1

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'format')
    search_fields = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(MenuList)
class MenuListAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent_list', 'linked_page', 'external_url', 'order')
    search_fields = ('title',)
    list_filter = ('parent_list',)
    ordering = ('order',)
    autocomplete_fields = ('linked_page',) 

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'uploaded_at', 'preview', 'html_code')
    
    def preview(self, obj):
        return format_html('<img src="{}" style="max-height: 50px;">', obj.image.url)
    
    def html_code(self, obj):
        return format_html('<code>{}</code>', obj.get_html_tag())
    
    html_code.short_description = "HTML-код"

    def delete_queryset(self, request, queryset):
        # Удаление файлов перед удалением записей
        for obj in queryset:
            if obj.image:
                if os.path.isfile(os.path.join(settings.MEDIA_ROOT, obj.image.name)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, obj.image.name))
        queryset.delete()

    def delete_model(self, request, obj):
        # Удаление файла при удалении одной записи
        if obj.image:
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT, obj.image.name)):
                os.remove(os.path.join(settings.MEDIA_ROOT, obj.image.name))
        obj.delete()
    
class MenuItemAdmin(admin.ModelAdmin):
    search_fields = ('title', 'linked_page__title')
    
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'linked_page', 'external_url', 'html_code')

    def html_code(self, obj):
        if obj.external_url:
            return format_html('<code>&lt;a href="{}" target="_blank"&gt;Текст&lt;/a&gt;</code>', obj.external_url)
        elif obj.linked_page:
            return format_html('<code>&lt;a href="{}"&gt;{}&lt;/a&gt;</code>', obj.linked_page.get_absolute_url(), obj.title)
        return "-"

    html_code.short_description = "HTML-код"

