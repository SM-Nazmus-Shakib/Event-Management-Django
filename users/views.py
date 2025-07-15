from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseForbidden
from .forms import CustomRegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm

User = get_user_model()

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('events:dashboard')
        
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, 'Registration successful! Please check your email to activate your account.')
            return redirect('users:sign-in')
    else:
        form = CustomRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('events:dashboard')
        
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('events:dashboard')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def sign_out(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:sign-in')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully! You can now log in.')
            return redirect('users:sign-in')
        messages.error(request, 'Invalid activation link.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    return redirect('home')


@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    users = User.objects.prefetch_related('groups').all().order_by('-date_joined')
    for user in users:
        user.group_name = user.groups.first().name if user.groups.exists() else 'No group'
    return render(request, 'admin/dashboard.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def assign_role(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f'Role {role.name} assigned to {user.username}')
            return redirect('users:admin-dashboard')
    else:
        form = AssignRoleForm()
    return render(request, 'admin/assign_role.html', {'form': form, 'user': user})

@user_passes_test(lambda u: u.is_superuser)
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f'Group {group.name} created successfully!')
            return redirect('users:group-list')
    else:
        form = CreateGroupForm()
    return render(request, 'admin/create_group.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def group_list(request):
    from django.contrib.auth.models import Group
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})

def no_permission(request):
    return HttpResponseForbidden("You don't have permission to access this page.")