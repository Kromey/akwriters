from django.contrib import admin


from .models import Character,CharacterNotes,CharacterNotesAnswer


# Register your models here.
class CharacterNotesAnswerInline(admin.TabularInline):
    model = CharacterNotesAnswer
    fields = ('question','answer',)
    readonly_fields = ('question','answer',)


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

    inlines = (CharacterNotesAnswerInline,)


@admin.register(CharacterNotes)
class CharacterNotesAdmin(admin.ModelAdmin):
    list_display = ('question','is_active',)


