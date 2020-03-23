from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, reverse
from .models import Tools, Projects, Employees, Producers
from django.contrib.auth.decorators import login_required
from .filters import ToolsFilter, ProjectsFilter, EmployeesFilter, ProducersFilter
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
import math

from .forms import CreateProject


class ToolsListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Tools
    template_name = 'tools/tools.html'
    ordering = ['-diameter_mm', '-tool_radius_mm', '-tool_length_mm', '-working_part_length_mm']
    context_object_name = 'tools'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ToolsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ToolsDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Tools
    template_name = 'tools/tools_detail.html'


class ToolsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tools
    template_name = 'tools/tools_form.html'
    fields = ['geometry',
              'material',
              'producer',
              'diameter_mm',
              'tool_radius_mm',
              'tool_length_mm',
              'working_part_length_mm',
              'price',
              'project']
    success_message = "Tool was created successfully"

    def form_valid(self, form):
        # allows to overwride the form
        form.instance.shank_diameter_mm = math.ceil(form.instance.diameter_mm)
        form.instance.compensation_mm = 0
        form.instance.status = 'Can be use'
        if form.instance.geometry == 'Square':
            form.instance.tool_radius_mm = 0
        elif form.instance.geometry == 'Ball':
            form.instance.tool_radius_mm = form.instance.diameter_mm / 2
        return super().form_valid(form)


class ToolsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tools
    template_name = 'tools/tools_update_form.html'
    fields = '__all__'
    success_message = "Tool was updated successfully"
    template_name_suffix = '_update_form'


class ToolsDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Tools
    template_name = 'tools/tools_confirm_delete.html'
    success_url = '/ERP/tools/'
    success_message = 'Tool was deleted'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(ToolsDeleteView, self).delete(request, *args, **kwargs)


# -----------------------PROJECTS----------------------------


class ProjectsListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Projects
    template_name = 'projects/projects.html'
    ordering = ['project_name']
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProjectsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ProjectsDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Projects
    template_name = 'projects/projects_detail.html'


class ProjectsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Projects
    template_name = 'projects/projects_form.html'
    form_class = CreateProject
    success_message = "Project was created successfully"

    def form_valid(self, form):
        # adds tools to project (outside model)
        tools_for_project = form.cleaned_data.get('add_tools_to_project')
        self.object = form.save()
        for tool in tools_for_project:
            tool_update = Tools.objects.get(tool_id=tool.tool_id)
            tool_update.project = self.object
            tool_update.save()
        return super().form_valid(form)


class ProjectsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Projects
    template_name = 'projects/projects_update_form.html'
    form_class = CreateProject
    success_message = "Project was updated successfully"
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        # adds tools to project (outside model)
        tools_for_project = form.cleaned_data.get('add_tools_to_project')
        self.object = form.save()
        for tool in tools_for_project:
            tool_update = Tools.objects.get(tool_id=tool.tool_id)
            tool_update.project = self.object
            tool_update.save()
        return super().form_valid(form)

class ProjectsDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    # delete function
    model = Projects
    template_name = 'projects/projects_confirm_delete.html'
    success_url = '/ERP/projects/'
    success_message = 'Project was deleted'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(ProjectsDeleteView, self).delete(request, *args, **kwargs)

# ----------------------- Employees -------------------


class EmployeesListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Employees
    template_name = 'employees/employees.html'
    ordering = ['last_name']
    context_object_name = 'employees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = EmployeesFilter(self.request.GET, queryset=self.get_queryset())
        return context


class EmployeesDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Employees
    template_name = 'employees/employees_detail.html'

    def get_context_data(self, **kwargs):
        # calculate salary
        context = super(EmployeesDetailView, self).get_context_data(**kwargs)
        salary_hour = Employees.objects.get(uuid_employee=self.object.uuid_employee).position.hourly_rate
        salary = int(salary_hour) * 160
        context['salary'] = salary
        return context


class EmployeesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Employees
    template_name = 'employees/employees_form.html'
    fields = ['first_name',
              'last_name',
              'email',
              'give_phone_number',
              'position',
              'date_of_employment']
    success_message = "Employee added"


class EmployeesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Employees
    template_name = 'employees/employees_update_form.html'
    fields = '__all__'
    success_message = "Employee was updated successfully"
    template_name_suffix = '_update_form'


class EmployeesDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Employees
    template_name = 'employees/employees_confirm_delete.html'
    success_url = '/ERP/employees/'
    success_message = 'Employee was deleted'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(EmployeesDeleteView, self).delete(request, *args, **kwargs)


# ----------------------------Producer--------------------------------

class ProducerListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Producers
    template_name = 'producers/producers.html'
    ordering = ['producer_name']
    context_object_name = 'employees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProducersFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ProducersDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Producers
    template_name = 'producers/producers_detail.html'


class ProducersCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Producers
    template_name = 'producers/producers_form.html'
    fields = '__all__'
    success_message = "Producer added"


class ProducersUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Producers
    template_name = 'producers/producers_update_form.html'
    fields = '__all__'
    success_message = "Producer was updated successfully"
    template_name_suffix = '_update_form'


class ProducersDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Producers
    template_name = 'producers/producers_confirm_delete.html'
    success_url = '/ERP/producers/'
    success_message = 'Producer was deleted'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(ProducersDeleteView, self).delete(request, *args, **kwargs)