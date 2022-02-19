from django.contrib import admin
from .models import Image

# Register your models here.

class ImageModelAdmin(admin.ModelAdmin):
    model = Image
    fields = ['title', 'image', 'caption']


admin.site.register(Image, ImageModelAdmin)