from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from app.models import Usercustome


class CustomUserAdmin(UserAdmin):
    model = Usercustome
    list_display = ('id','username', 'email', 'phone_number')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'user_role')}),
    )
    
admin.site.register(Usercustome, CustomUserAdmin)
    
    
    
    
    