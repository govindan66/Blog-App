from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.BlogPost)
class BlogPostModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','image','featured']
