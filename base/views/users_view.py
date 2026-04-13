from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from base.models import User
from base.forms import UserCreateForm

class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'