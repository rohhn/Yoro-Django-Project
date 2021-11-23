from django.contrib import admin
from .models import Album, Image

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass