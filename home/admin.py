from django.contrib import admin
from .models import cryptUser, quesAns
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from import_export.admin import ExportActionMixin


class UserAdminConfig(ExportActionMixin, UserAdmin):
    search_fields = ('email', 'user_name', 'first_name', 'college_name', 'discord_id')
    list_filter = ('college_name', 'is_verified', 'is_staff')
    ordering = ('-current_level',)
    list_display = ('email','user_name', 'first_name', 'discord_id','is_verified', 'is_staff', 'current_level')

    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', 'discord_id', 'college_name', 'college_roll_number' ,'password')}),
        ('Permissions', {'fields':('is_staff', 'is_verified', 'is_active')}),
        ('Progress', {'fields':('current_level','score', 'rank' , 'start_date', 'date_time' ,'answers')})
        
    )

    add_fieldsets = (
        (None,{
        'classes':('wide',),
        'fields': ('email', 'user_name', 'first_name', 'last_name','discord_id', 'college_name', 'college_roll_number', 'password1', 'password2', 'is_verified', 'is_staff')
    }),
    )


admin.site.register(cryptUser, UserAdminConfig)
admin.site.register(quesAns)