from django.contrib.auth import get_user_model, update_session_auth_hash
from django.forms import Form
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.users.forms import UserCreateForm
from task_manager.users.mixins import UserCreatorOnlyMixin
from task_manager.view_mixins import (
    CreateViewMixin,
    UpdateViewMixin,
    DeleteViewMixin,
    IndexViewMixin
)


class UsersAbstractMixin:
    model = get_user_model()
    success_url = reverse_lazy('users')
    form_class = UserCreateForm


class UsersIndexView(UsersAbstractMixin, IndexViewMixin):
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(UsersAbstractMixin, CreateViewMixin):
    success_url = reverse_lazy('login')
    template_name = 'users/create.html'
    success_message = _('User has been registered successfully.')


class UserUpdateView(UserCreatorOnlyMixin, UsersAbstractMixin,
                     UpdateViewMixin):
    template_name = 'users/update.html'
    success_message = _('User has been updated successfully.')

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.instance)
        return response


class UserDeleteView(UserCreatorOnlyMixin, UsersAbstractMixin,
                     DeleteViewMixin):
    template_name = 'users/delete.html'
    success_message = _('User has been deleted successfully.')
    failure_message = _('Cannot delete user because it is in use.')
    form_class = Form

    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=request.user.id)
        if user.tasks_author.first() or user.tasks_executor.first():
            self.have_dependencies = True
        return super().post(request, *args, **kwargs)
