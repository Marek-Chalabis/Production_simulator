from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import ShowInformations
from django.contrib.auth.models import User
# check if user is log in
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin


class InformationsListView(ListView):
    model = ShowInformations
    template_name = 'informations/informations.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 8


class UserInformationsListView(ListView):
    model = ShowInformations
    template_name = 'informations/user_informations.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return ShowInformations.objects.filter(author=user).order_by('date_posted')


class InformationsDetailView(DetailView):
    model = ShowInformations


class InformationsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ShowInformations
    fields = ['title', 'info']
    success_message = "Information added"

    def form_valid(self, form):
        # checks if the author of the post is user login
        form.instance.author = self.request.user
        return super().form_valid(form)


class InformationsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = ShowInformations
    fields = ['title', 'info']
    success_message = 'Information updated'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # check if the user who create post is log in
        information = self.get_object()
        if self.request.user == information.author:
            return True


class InformationsDeletelView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ShowInformations
    success_url = '/'
    success_message = 'Information deleted'

    def test_func(self):
        information = self.get_object()
        if self.request.user == information.author:
            return True
