from django.contrib import admin
from .models import Post

admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['category', ...]
