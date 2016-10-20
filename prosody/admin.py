from django.contrib import admin


from .models import Prosody,ProsodyRoster


# Register your models here.
@admin.register(Prosody)
class ProsodyAdmin(admin.ModelAdmin):
    list_display = ('user','store','key','value')

@admin.register(ProsodyRoster)
class ProsodyRosterAdmin(admin.ModelAdmin):
    list_display = ('user','key','value')

