from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'status', 'created', 'author')
    list_filter = ('title', 'status', 'author')
    search_fields = ('title', 'status', 'author')
    ordering = ('status', 'publish')


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post', 'created', 'author')
    list_filter = ('post', 'created', 'author')
    search_fields = ('post', 'created', 'author')
    ordering = ('post', 'created', 'author')
