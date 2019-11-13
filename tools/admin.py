from django.contrib import admin


from .models import Character,CharacterNotes,CharacterNotesAnswer


# Register your models here.
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name','story',)
    fields = (
        'story',
        ('name', 'age',),
        'appearance',
    )
    readonly_fields = ('story',)
    select_related = ('story', 'story__owner')


@admin.register(CharacterNotes)
class CharacterNotesAdmin(admin.ModelAdmin):
    list_display = ('question','is_active',)


@admin.register(CharacterNotesAnswer)
class CharacterNotesAnswerAdmin(admin.ModelAdmin):
    list_display = ('character','question','answer',)
    readonly_fields = ('character','question','answer',)

