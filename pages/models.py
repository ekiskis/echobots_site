from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


from django.db import models
from django.utils.text import slugify

class Page(models.Model):
    """Модель для хранения контента страниц"""
    title = models.CharField(max_length=200, unique=True, verbose_name="Название страницы")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL-адрес")
    content = models.TextField(
        verbose_name="Содержимое", 
        help_text="Поддерживается HTML и Markdown", 
        default=""
    )
    format_choices = [
        ('html', 'HTML'),
        ('markdown', 'Markdown')
    ]
    format = models.CharField(max_length=10, choices=format_choices, default='html', verbose_name="Формат")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class PageBlock(models.Model):
    BLOCK_TYPES = [
        ('header', 'Заголовок'),
        ('text', 'Текст'),
        ('list', 'Список'),
        # ('image', 'Изображение'),
        ('link', 'Ссылка'),
    ]

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="blocks")
    block_type = models.CharField(max_length=10, choices=BLOCK_TYPES, verbose_name="Тип блока")
    content = models.TextField(verbose_name="Содержимое")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        return f"{self.get_block_type_display()} - {self.page.title}"

    class Meta:
        ordering = ['order']
        verbose_name = "Блок страницы"
        verbose_name_plural = "Блоки страниц"


class MenuList(models.Model):
    """Модель для списка элементов в боковом меню"""
    title = models.CharField(max_length=100, unique=True, verbose_name="Название списка")
    
    def __str__(self):
        return self.title

class MenuItem(models.Model):
    """Элемент меню (либо отдельный пункт, либо внутри списка)"""
    title = models.CharField(max_length=100, verbose_name="Название элемента")
    parent_list = models.ForeignKey(MenuList, on_delete=models.CASCADE, null=True, blank=True, related_name="items", verbose_name="Принадлежит списку")
    linked_page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Связанная страница")
    external_url = models.URLField(blank=True, null=True, verbose_name="Внешняя ссылка")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    def clean(self):
        """Гарантирует, что у элемента не может быть одновременно привязки к странице и внешней ссылке"""
        if self.linked_page and self.external_url:
            raise ValidationError("Элемент не может одновременно ссылаться на страницу и внешний ресурс.")

    def get_url(self):
        """Возвращает URL страницы или внешней ссылки"""
        if self.linked_page:
            return f"/page/{self.linked_page.slug}/"
        return self.external_url

    def __str__(self):
        return self.title

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/', verbose_name="Изображение")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name

    def get_html_tag(self):
        """Генерирует HTML-код для вставки изображения"""
        return f'<img src="{self.image.url}" alt="Текст">'
