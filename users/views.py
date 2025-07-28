from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, FormView, DetailView, UpdateView, TemplateView, ListView
)
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordChangeView, PasswordResetView, 
    PasswordResetConfirmView
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from .models import User
from .forms import (
    CustomRegistrationForm, LoginForm, 
    ProfileUpdateForm, CustomPasswordChangeForm,
    CustomPasswordResetForm, CustomSetPasswordForm,
    GroupForm, AssignRoleForm
)

def admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='users:sign-in'  # Changed from non-existent URL
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/dashboard.html'
    
    @method_decorator(admin_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.select_related().order_by('-date_joined')
        context['total_users'] = User.objects.count()
        context['active_users'] = User.objects.filter(is_active=True).count()
        context['staff_users'] = User.objects.filter(is_staff=True).count()
        return context

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'
    paginate_by = 20
    
    @method_decorator(admin_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CreateGroupView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('users:group-list')
    
    @method_decorator(admin_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Group created successfully!')
        return super().form_valid(form)

class AssignRoleView(LoginRequiredMixin, FormView):
    form_class = AssignRoleForm
    template_name = 'admin/assign_role.html'
    success_url = reverse_lazy('users:admin-dashboard')
    
    @method_decorator(admin_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, pk=self.kwargs['user_id'])
        return context
    
    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        group = form.cleaned_data['group']
        user.groups.clear()
        user.groups.add(group)
        messages.success(self.request, f'Role assigned successfully to {user.username}!')
        return super().form_valid(form)

class SignUpView(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Set to False if using email activation
        user.save()
        
        # Send activation email (handled by signals.py)
        messages.info(self.request, 'Please check your email to activate your account.')
        return super().form_valid(form)

class SignInView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('users:profile')  # Changed default redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, 'Your account is not activated. Please check your email.')
            return self.form_invalid(form)
        
        login(self.request, user)
        messages.success(self.request, f'Welcome back, {user.username}!')
        return super().form_valid(form)

class ActivateAccountView(TemplateView):
    template_name = 'users/activation_result.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        token = kwargs['token']
        
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                context = {'success': True, 'already_active': True}
            elif default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                login(request, user)  # Auto-login after activation
                context = {'success': True, 'already_active': False}
                return redirect('users:profile')
            else:
                context = {'success': False}
        except Exception as e:
            context = {'success': False}
        
        return self.render_to_response(context)

class SignOutView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('users:sign-in')

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed successfully!')
        return super().form_valid(form)

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been reset successfully!')
        return super().form_valid(form)