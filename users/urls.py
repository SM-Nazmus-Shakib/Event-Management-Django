from django.urls import path
from .views import (
    sign_up, sign_in, sign_out, activate_user,
    admin_dashboard, assign_role, create_group, 
    group_list, no_permission
)

app_name = 'users'

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),
    
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/users/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/groups/create/', create_group, name='create-group'),
    path('admin/groups/', group_list, name='group-list'),
    
    path('no-permission/', no_permission, name='no-permission'),
]