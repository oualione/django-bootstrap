from django.db import models
from django.db.models.fields import CharField, DateTimeField, IntegerField, TextField
from users.models import Profile


# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=20)


    def __str__(self):
        return f"{self.label}"

class Category(models.Model):
    label = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.label}"


  


class Course (models.Model):

    tags = models.ManyToManyField("Tag")
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField()
    price = models.FloatField()
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.description}"

    
    def post_is_published(self):
        if self.is_published:
            return print("The Post is Published")
        return print("This Post isn't published yet !")
    
   
    




