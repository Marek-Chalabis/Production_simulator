import math

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, F, CharField, Value, DecimalField, ExpressionWrapper
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

from .filters import ToolsFilter, ProjectsFilter, EmployeesFilter, ProducersFilter
from .forms import CreateProject
from .models import Tools, Projects, Employees, Producers





class ToolsListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    queryset = Tools.objects.only('tool_id', 'geometry', 'material', 'diameter_mm', 'tool_radius_mm', 'tool_length_mm',
                                  'working_part_length_mm', 'compensation_mm', 'shank_diameter_mm', 'status',
                                  'project__project_name', 'producer__producer_name') \
        .select_related('producer', 'project')
    template_name = 'tools/tools.html'
    ordering = ['-diameter_mm', '-tool_radius_mm', '-tool_length_mm', '-working_part_length_mm']
    context_object_name = 'tools'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ToolsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ToolsDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = 'tools/tools_detail.html'

    def get_queryset(self):
        tool = get_object_or_404(Tools, pk=self.kwargs.get('pk'))
        queryset = Tools.objects.only('tool_id', 'geometry', 'material', 'diameter_mm', 'tool_radius_mm',
                                      'tool_length_mm', 'working_part_length_mm', 'compensation_mm',
                                      'shank_diameter_mm', 'status', 'price', 'date_of_purchase',
                                      'project__project_name', 'project__project_id',
                                      'producer__producer_name', 'producer__producer_id') \
            .select_related('producer', 'project').filter(pk=tool.tool_id)
        return queryset


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


class ToolsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tools
    template_name = 'tools/tools_update_form.html'
    fields = [
            'geometry', 'material', 'diameter_mm', 'shank_diameter_mm', 'tool_radius_mm',
            'tool_length_mm', 'working_part_length_mm', 'compensation_mm',  'producer',
            'status', 'price', 'project']
    success_message = "Tool was updated successfully"
    template_name_suffix = '_update_form'


class ToolsDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Tools
    template_name = 'tools/tools_confirm_delete.html'
    success_url = '/erp/tools/'
    success_message = 'Tool was deleted'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(ToolsDeleteView, self).delete(request, *args, **kwargs)


# -----------------------PROJECTS----------------------------

class ProjectsListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    queryset = Projects.objects.annotate(
        number_of_tools=Count('tools', distinct=True), number_of_projects=Count('employees', distinct=True))
    template_name = 'projects/projects.html'
    ordering = 'project_name'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProjectsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ProjectsDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Projects
    template_name = 'projects/projects_detail.html'

    def get_queryset(self):
        project = get_object_or_404(Projects, pk=self.kwargs.get('pk'))
        queryset = Projects.objects.filter(pk=project.project_id) \
            .annotate(number_of_tools=Count('tools', distinct=True),
                      number_of_projects=Count('employees', distinct=True))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tools = Tools.objects.filter(project_id=self.kwargs.get('pk')) \
            .annotate(full_description=Concat(Value('ID('), F('tool_id'), Value(')- '), F('material'), Value(' '),
                                              F('geometry'), Value(' Fi: '), F('diameter_mm'),
                                              output_field=CharField())).order_by('-diameter_mm')
        context['tools'] = tools

        employees = Employees.objects.select_related('position')\
            .filter(employeesinprojects__project_id=self.kwargs.get('pk')).annotate(
            full_name=Concat(F('first_name'), Value(' '), F('last_name'), Value(' ('),
                             F('position__position_name'), Value(')'), output_field=CharField()))\
            .order_by('-position')
        context['employees'] = employees
        return context


class ProjectsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    queryset = Projects.objects.select_related('position').prefetch_related('employees', 'employees__position')
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
    success_url = '/erp/projects/'
    success_message = 'Project was deleted'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(ProjectsDeleteView, self).delete(request, *args, **kwargs)


# ----------------------- Employees -------------------

class EmployeesListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    list_of_projects = Projects.objects.values_list('project_name', flat=True)
    # adds number of projects
    queryset = Employees.objects.select_related('position'). \
        filter(employeesinprojects__project__project_name__in=list_of_projects).annotate(
        number_of_projects=Count('projects'))
    template_name = 'employees/employees.html'
    ordering = ['last_name']
    context_object_name = 'employees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = EmployeesFilter(self.request.GET, queryset=self.get_queryset())
        return context


class EmployeesDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = 'employees/employees_detail.html'

    def get_queryset(self):
        employee = get_object_or_404(Employees, uuid_employee=self.kwargs.get('pk'))
        # ads salary
        queryset = Employees.objects.select_related('position').filter(uuid_employee=employee.uuid_employee)\
            .annotate(salary=ExpressionWrapper(F('position__hourly_rate') * 160, output_field=DecimalField()))
        return queryset

    def get_context_data(self, **kwargs):
        # calculate salary
        context = super(EmployeesDetailView, self).get_context_data(**kwargs)
        # projects where employee is in
        projects = Projects.objects.values('project_name', 'project_id')\
            .filter(employeesinprojects__employee__uuid_employee=self.kwargs.get('pk'))
        context['projects'] = projects
        return context


class EmployeesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Employees
    template_name = 'employees/employees_form.html'
    fields = ['first_name',
              'last_name',
              'email',
              'phone_number',
              'position'
              ]
    success_message = "Employee added"


class EmployeesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Employees
    template_name = 'employees/employees_update_form.html'
    fields = ['first_name',
              'last_name',
              'email',
              'phone_number',
              'position'
              ]
    success_message = "Employee was updated successfully"
    template_name_suffix = '_update_form'


class EmployeesDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Employees
    template_name = 'employees/employees_confirm_delete.html'
    success_url = '/erp/employees/'
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
    success_url = '/erp/producers/'
    success_message = 'Producer was deleted'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(ProducersDeleteView, self).delete(request, *args, **kwargs)
