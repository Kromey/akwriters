from django.contrib import admin


from .models import Character,CharacterNotes,CharacterNotesAnswer


# Register your models here.
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name','owner',)
    readonly_fields = ('owner',)


@admin.register(CharacterNotes)
class CharacterNotesAdmin(admin.ModelAdmin):
    list_display = ('question','is_active',)


@admin.register(CharacterNotesAnswer)
class CharacterNotesAnswerAdmin(admin.ModelAdmin):
    list_display = ('character','question','answer',)
    readonly_fields = ('character','question','answer',)

