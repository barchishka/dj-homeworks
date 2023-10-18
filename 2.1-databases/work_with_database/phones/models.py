from django.db import models


class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60, null=False)
    price = models.IntegerField(default=None)
    image = models.URLField(default=None)
    release_date = models.DateTimeField(default=None)
    lte_exists = models.BooleanField(default=None)
    slug = models.SlugField(default=None)

    def __str__(self):
        return f'{self.id}: {self.name}'
