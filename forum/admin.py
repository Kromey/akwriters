from django.contrib import admin


from .models import Board,BoardCategory

# Register your models here.

@admin.register(BoardCategory)
class BoardCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    ordering = ('category__title', 'slug')

