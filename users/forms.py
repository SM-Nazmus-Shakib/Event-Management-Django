from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    AuthenticationForm
)
from .models import User
from django.contrib.auth.models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {
            'permissions': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class AssignRoleForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Select Role"
    )

class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            base_classes = "block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            
            if isinstance(field.widget, (forms.TextInput, forms.PasswordInput, forms.EmailInput, forms.NumberInput)):
                field.widget.attrs.update({
                    'class': f"{base_classes} py-2 px-3 border",
                    'placeholder': field.label
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{base_classes} py-2 px-3 border",
                    'rows': 3,
                    'placeholder': field.label
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': f"{base_classes} py-2 px-3 border"
                })
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': "block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                })

class CustomRegistrationForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter username or email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter password'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'bio']

class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass

class CustomSetPasswordForm(StyledFormMixin, SetPasswordForm):
    pass

# Admin forms
class CustomUserCreationForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'bio', 'is_active', 'is_staff')

class CustomUserChangeForm(StyledFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'bio', 'is_active', 'is_staff', 'groups', 'user_permissions')