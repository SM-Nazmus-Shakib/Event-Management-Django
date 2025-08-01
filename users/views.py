from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout,authenticate
from users.forms import CustomRegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm, EditProfileForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, FormView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

User = get_user_model()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

class SignUpView(CreateView):
    model = User
    form_class = CustomRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:sign-in') 
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        messages.success(self.request, 'A confirmation email has been sent. Please check your email.')
        return super().form_valid(form)

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        if self.request.user.groups.filter(name='Admin').exists():
            return reverse_lazy('users:admin-dashboard')
        return reverse_lazy('users:profile')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, 'Your account is not activated. Please check your email for activation link.')
            return self.form_invalid(form)
        
        messages.success(self.request, f'Welcome back, {user.username}!')
        return super().form_valid(form)

class SignOutView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/logout.html'
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:sign-in')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully! You can now log in.')
            return redirect('users:sign-in')  # Use namespace
        else:
            messages.error(request, 'Invalid activation token')
            return redirect('users:sign-in')
    except User.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('users:sign-in')

class AdminDashboardView(UserPassesTestMixin, ListView):
    template_name = 'admin/dashboard.html'
    context_object_name = 'users'
    
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_queryset(self):
        return User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
        ).all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for user in context['users']:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'No Group Assigned'
        return context

class AssignRoleView(UserPassesTestMixin, FormView):
    template_name = 'admin/assign_role.html'
    form_class = AssignRoleForm
    
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_user(self):
        return User.objects.get(id=self.kwargs['user_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_user()
        return context
    
    def form_valid(self, form):
        user = self.get_user()
        role = form.cleaned_data.get('role')
        user.groups.clear()
        user.groups.add(role)
        messages.success(self.request, f"User {user.username} has been assigned to the {role.name} role")
        return redirect('users:dashboard')

class CreateGroupView(UserPassesTestMixin, CreateView):
    model = Group
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('create-group')
    
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def form_valid(self, form):
        group = form.save()
        messages.success(self.request, f"Group {group.name} has been created successfully")
        return super().form_valid(form)

class GroupListView(UserPassesTestMixin, ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'
    
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile/detail.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'profile/update.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    template_name = 'profile/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('profile')

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('sign-in')
    email_template_name = 'registration/password_reset_email.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'A password reset email has been sent. Please check your inbox.')
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password_confirm.html'
    success_url = reverse_lazy('sign-in')
    
    def form_valid(self, form):
        messages.success(self.request, 'Your password has been reset successfully!')
        return super().form_valid(form)