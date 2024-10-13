from django.contrib import admin
from blogs.models import Blog


@admin.register(Blog)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'image', 'date_of_creation', 'views_count', 'user',)
    list_filter = ('title', 'date_of_creation', 'views_count', 'user',)
    readonly_fields = ('user', 'views_count', 'date_of_creation',)