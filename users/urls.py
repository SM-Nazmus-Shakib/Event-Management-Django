from django.urls import path
from users.views import (
    SignUpView, CustomLoginView, SignOutView, activate_user,
    AdminDashboardView, AssignRoleView, CreateGroupView, GroupListView,
    ProfileView, ChangePassword, CustomPasswordResetView, CustomPasswordResetConfirmView, EditProfileView
)
from django.contrib.auth.views import PasswordChangeDoneView

app_name = 'users'

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),
    
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/users/<int:user_id>/assign-role/', AssignRoleView.as_view(), name='assign-role'),
    path('admin/groups/create/', CreateGroupView.as_view(), name='create-group'),
    path('admin/groups/', GroupListView.as_view(), name='group-list'),
    
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/', ChangePassword.as_view(), name='password-change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'), name='password-change-done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile')
]