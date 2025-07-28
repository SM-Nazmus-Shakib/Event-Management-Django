from django.urls import path
from users.views import (
    SignUpView, SignInView, SignOutView, ActivateAccountView,
    ProfileView, ProfileUpdateView,
    CustomPasswordChangeView, CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    AdminDashboardView, GroupListView, CreateGroupView, AssignRoleView  # Add these
)
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
    path('activate/<int:user_id>/<str:token>/',  ActivateAccountView.as_view(), name='activate-user'),
    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
    
    # Password
    path('password-change/', CustomPasswordChangeView.as_view(), name='password-change'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    
    # Admin URLs
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/groups/', GroupListView.as_view(), name='group-list'),
    path('admin/groups/create/', CreateGroupView.as_view(), name='create-group'),
    path('admin/assign-role/<int:user_id>/', AssignRoleView.as_view(), name='assign-role'),
]