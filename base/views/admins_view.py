from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from base.models import Admin
from base.forms import AdminForm


class AdminListView(ListView):
    model = Admin
    template_name = 'admins/admin_list.html'
    context_object_name = 'admins'


class AdminCreateView(CreateView):
    model = Admin
    form_class = AdminForm
    template_name = 'admins/admin_form.html'
    success_url = reverse_lazy('admin_list')
