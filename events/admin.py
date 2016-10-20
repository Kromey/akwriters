from django.contrib import admin


from .models import Calendar,MonthCache


# Register your models here.
@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ('name','remote_id','css_class')

@admin.register(MonthCache)
class MonthCacheAdmin(admin.ModelAdmin):
    list_display = ('calendar','month','data_cached_on','is_cache_stale')
    readonly_fields = [field.name for field in MonthCache._meta.get_fields()]

    def has_add_permission(self, request, obj=None):
        return False

