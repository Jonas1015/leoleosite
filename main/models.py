from django.db import models
from PIL import Image

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'Categories_images')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, force_insert = False, force_update = False, using=None, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 400 or img.width > 300:
            output_size = (200,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Book(models.Model):
    name = models.CharField(max_length = 100)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True )
    isbn = models.CharField(max_length = 100, null=True, blank = True)
    author = models.CharField(max_length  =100, null = True, blank = True)
    publisher = models.CharField(max_length  =100, null = True, blank = True)
    year = models.PositiveIntegerField(null = True, blank = True)
    description = models.TextField(blank = True, null = True)
    is_popular = models.BooleanField(default=False)
    to_be_sold = models.BooleanField(default=True)
    image = models.ImageField(upload_to = 'books_images')
    file = models.FileField(upload_to = 'books')

    class Meta:
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.name

    # def save(self, force_insert = False, force_update = False, using=None, **kwargs):
    #     super().save()
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 400 or img.width > 300:
    #         output_size = (300,400)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
