from django.contrib import admin


from .models import Calendar,MonthCache


# Register your models here.
admin.site.register(Calendar)
admin.site.register(MonthCache)
