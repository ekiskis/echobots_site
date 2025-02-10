from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название страницы")
    slug = models.SlugField(unique=True, verbose_name="URL (slug)")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

class PageBlock(models.Model):
    BLOCK_TYPES = [
        ('header', 'Заголовок'),
        ('text', 'Текст'),
        ('image', 'Изображение'),
        ('list', 'Список'),
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
