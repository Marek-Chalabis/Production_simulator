from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import F, ExpressionWrapper
from .models import ShowInformations
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import F, Value, CharField
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
# ==========query========
query_information = ShowInformations.objects.select_related('author', 'author__profile').annotate(
        author_username=F('author__username'),
        author_fullname=Concat(F('author__first_name'), Value(' '), F('author__last_name'), output_field=CharField()))\
    .order_by('-date_posted')


class InformationsListView(ListView):
    queryset = query_information
    template_name = 'informations/informations.html'
    context_object_name = 'posts'
    paginate_by = 8


class UserInformationsListView(ListView):
    template_name = 'informations/user_informations.html'
    context_object_name = 'posts'
    paginate_by = 5
    test = 'fsfs'

    def get_queryset(self):
        # gets posts added by selected user
        # returns 404 if author doesn't exists
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = query_information.filter(author_id=author.id)
        return queryset


class InformationsDetailView(DetailView):

    def get_queryset(self):
        info = get_object_or_404(ShowInformations, pk=self.kwargs.get('pk'))
        queryset = query_information.filter(pk=info.id)
        return queryset


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
