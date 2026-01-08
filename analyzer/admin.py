"""
Admin configuration for the analyzer app.
"""
from django.contrib import admin
from .models import Category, Tag, TextDocument


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin view for Category model."""
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin view for Tag model."""
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TextDocument)
class TextDocumentAdmin(admin.ModelAdmin):
    """Admin view for TextDocument model."""
    list_display = ("title", "category", "created_at", "short_content")
    list_filter = ("category", "created_at", "tags")
    search_fields = ("title", "content")
    date_hierarchy = "created_at"

    def short_content(self, obj):
        """Returns a truncated version of the content."""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    short_content.short_description = "Content Preview"

