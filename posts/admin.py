from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'status', 'created', 'author')
    list_filter = ('title', 'status', 'author')
    search_fields = ('title', 'status', 'author')
    ordering = ('status', 'publish')
# admin.site.register(Post)
