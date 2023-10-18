from django.db import models


class Article(models.Model):
    objects = None
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение', )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Object(models.Model):
    name = models.CharField(max_length=50, verbose_name='Раздел')
    article = models.ManyToManyField(Article, through='Relationship', related_name='tags', verbose_name='Статьи')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.name


class Relationship(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes', verbose_name='Разделы')
    tag = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='scopes', verbose_name='Разделы')
    is_main = models.BooleanField(verbose_name='Основной')
