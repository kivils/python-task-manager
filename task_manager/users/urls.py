from django.urls import path
from task_manager.users.views import (
    UsersIndexView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)

urlpatterns = [
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('', UsersIndexView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='user_create'),
]
