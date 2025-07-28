from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.admin.models import LogEntry


# Add at the bottom of admin.py
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
    list_filter = ['action_time', 'user', 'content_type']
    search_fields = ['object_repr', 'change_message']
    date_hierarchy = 'action_time'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_per_page = 25
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'bio')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 
                'phone_number', 'password1', 'password2', 
                'is_active', 'is_staff'
            ),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ('groups', 'user_permissions')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

