from django.contrib import admin
from django import forms
from .models import Category, Post, Tag
from django_ckeditor_5.widgets import CKEditor5Widget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'body': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='extends'
            )
        }

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'created_at', 'updated_at', 'author')
    search_fields = ('title', 'body')
    list_filter = ('post_date', 'category')
    readonly_fields = ('title_tag', 'created_at', 'updated_at')