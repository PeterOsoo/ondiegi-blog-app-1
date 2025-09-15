from django.contrib import admin
from .models import BlogPost, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}  # auto-fill slug from name


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "created_at")
    search_fields = ("title", "author__username", "content")
    ordering = ("-created_at",)
    list_filter = ("category", "created_at")
    prepopulated_fields = {"slug": ("title",)}
