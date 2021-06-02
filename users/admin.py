from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from users.models import User

from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.
UserModel = get_user_model()

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'bio', 'location', 'birth_date', 'profile_pic']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'bio', 'location', 'birth_date', 'profile_pic')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'bio', 'location', 'birth_date', 'profile_pic',)}
        ),
    )

admin.site.register(User, UserAdmin)

admin.site.unregister(Group)