from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Тег")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name

class TextDocument(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='documents', verbose_name="Категория")
    tags = models.ManyToManyField(Tag, related_name='documents', blank=True, verbose_name="Теги")

    class Meta:
        verbose_name = "Текстовый документ"
        verbose_name_plural = "Текстовые документы"

    def __str__(self):
        return self.title
