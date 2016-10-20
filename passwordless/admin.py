from django.contrib import admin


from .models import User,AuthToken,AppPassword


# Register your models here.
def app_password_count(obj):
    return obj.apppassword_set.count()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','is_active','last_login',app_password_count)
    fields = ('username','jid','email','is_active','is_superuser',('date_joined','last_login'),)
    readonly_fields = ('jid','date_joined','last_login',)


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user','date_sent','is_valid')
    fields = ('user','date_sent','date_expires','is_valid')
    readonly_fields = ('user','date_sent','date_expires','is_valid')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        else:
            return not obj.is_valid


@admin.register(AppPassword)
class AppPasswordAdmin(admin.ModelAdmin):
    list_display = ('user','name','created_on','last_used')
    fields = ('user','name','created_on','last_used')
    readonly_fields = ('user','name','created_on','last_used')

    def has_add_permission(self, request, obj=None):
        return False

