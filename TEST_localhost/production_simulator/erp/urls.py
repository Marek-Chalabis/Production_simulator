from django.urls import path
from .views import (
    ToolsListView, ToolsDetailView, ToolsCreateView, ToolsUpdateView, ToolsDeleteView,
    ProjectsDeleteView, ProjectsListView, ProjectsDetailView, ProjectsCreateView,  ProjectsUpdateView,
    EmployeesListView, EmployeesDetailView, EmployeesCreateView, EmployeesUpdateView, EmployeesDeleteView,
    ProducerListView, ProducersDetailView, ProducersCreateView, ProducersUpdateView, ProducersDeleteView,)

urlpatterns = [
    path('tools/', ToolsListView.as_view(), name='tools-home'),
    path('tool/<int:pk>', ToolsDetailView.as_view(), name='tool-detail'),
    path('tool/new', ToolsCreateView.as_view(), name='tool-create'),
    path('tool/<int:pk>/update/', ToolsUpdateView.as_view(), name='tool-update'),
    path('tool/<int:pk>/delete/', ToolsDeleteView.as_view(), name='tool-delete'),

    path('projects/', ProjectsListView.as_view(), name='projects-home'),
    path('project/<int:pk>', ProjectsDetailView.as_view(), name='project-detail'),
    path('project/new', ProjectsCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update/', ProjectsUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', ProjectsDeleteView.as_view(), name='project-delete'),

    path('employees/', EmployeesListView.as_view(), name='employees-home'),
    path('employee/<uuid:pk>', EmployeesDetailView.as_view(), name='employee-detail'),
    path('employee/new', EmployeesCreateView.as_view(), name='employee-create'),
    path('employee/<uuid:pk>/update/', EmployeesUpdateView.as_view(), name='employee-update'),
    path('employee/<uuid:pk>/delete/', EmployeesDeleteView.as_view(), name='employee-delete'),

    path('producers/', ProducerListView.as_view(), name='producers-home'),
    path('producer/<int:pk>', ProducersDetailView.as_view(), name='producer-detail'),
    path('producer/new', ProducersCreateView.as_view(), name='producer-create'),
    path('producer/<int:pk>/update/', ProducersUpdateView.as_view(), name='producer-update'),
    path('producer/<int:pk>/delete/', ProducersDeleteView.as_view(), name='producer-delete'),
]

