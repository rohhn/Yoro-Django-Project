from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField

class Album(models.Model):
    name = models.CharField(max_length=50)
    hashtags = models.CharField(max_length=200)
    publish = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add= True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Image(models.Model):
    title = models.CharField(max_length=100)
    color = ColorField(default="#000")
    position = models.CharField(
        max_length=6,
        choices= (
            ("center", "center"),
            ("left", "left"),
            ("right", "right")
        ),
        default="center"
    )
    image = models.ImageField(upload_to = "images/")
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    hashtags = models.CharField(max_length=300)
    publish = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add= True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
