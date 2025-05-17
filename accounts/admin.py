from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import CustomUserModel
from accounts.forms import  CustomUserCreateForm, CustomUserChangeForm 


@admin.register(CustomUserModel)
class CustomUserAdmin(UserAdmin):
    model = CustomUserModel
    form = CustomUserChangeForm
    add_form = CustomUserCreateForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )   
    
    list_display = [
        "email",
        "username",
        "is_staff",
        "is_active",
    ]

