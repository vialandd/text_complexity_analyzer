from django.contrib import admin
from .models import Category, Tag, TextDocument

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(TextDocument)
class TextDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'short_content')
    list_filter = ('category', 'created_at', 'tags')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    
    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    short_content.short_description = "Content Preview"
