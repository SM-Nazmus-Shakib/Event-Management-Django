from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .forms import UserRegistrationForm, AssignRoleForm, GroupForm
from django.contrib.auth.tokens import default_token_generator
from .models import UserProfile
from events.models import Event  # Import Event model

def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')  # Redirect to events dashboard
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if not user.is_active:
                messages.error(request, 'Account not activated. Please check your email.')
                return redirect('sign-in')
            login(request, user)
            
            # Redirect based on group
            if user.groups.filter(name='Admin').exists():
                return redirect('admin:index')
            elif user.groups.filter(name='Organizer').exists():
                return redirect('event-create')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def sign_out(request):
    logout(request)
    return redirect('sign-in')

@login_required
def user_list(request):
    users = User.objects.all().prefetch_related('groups')
    return render(request, 'admin/user_list.html', {'users': users})

@login_required
def assign_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group']
            user.groups.clear()
            user.groups.add(group)
            messages.success(request, f'Role assigned successfully to {user.username}')
            return redirect('user-list')
    else:
        form = AssignRoleForm()
    return render(request, 'admin/assign_role.html', {'form': form, 'user': user})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group created successfully!')
            return redirect('group-list')
    else:
        form = GroupForm()
    return render(request, 'admin/create_group.html', {'form': form})

@login_required
def group_list(request):
    groups = Group.objects.all().prefetch_related('permissions')
    return render(request, 'admin/group_list.html', {'groups': groups})

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
