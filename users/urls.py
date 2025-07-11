from django.urls import path
from users.views import (
    user_list, assign_role, create_group, group_list,
    sign_up, sign_in, sign_out, activate_user
)

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),
    path('users/', user_list, name='user-list'),
    path('users/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('groups/', group_list, name='group-list'),
    path('groups/create/', create_group, name='create-group'),
]