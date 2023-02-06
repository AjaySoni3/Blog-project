from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='blogs')

    def __str__(self):
        return self.title


class AddImage(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)


