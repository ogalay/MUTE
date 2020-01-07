from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'rating', 'hated_mus_genre', 'is_staff', 'is_active',)
    list_filter = ('username', 'rating', 'hated_mus_genre', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'first_name', 'last_name', 'rating', 'hated_mus_genre')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'rating',
                       'hated_mus_genre', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)