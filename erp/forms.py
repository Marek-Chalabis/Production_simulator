from django import forms
from django.forms import ModelForm

from .models import Tools, Projects, Employees


class CreateProject(ModelForm):
    employees = forms.ModelMultipleChoiceField(
        queryset=Employees.objects.select_related('position').order_by('last_name'), required=False)

    class Meta:
        model = Projects
        fields = ['project_name', 'time_for_project_hours', 'profit', 'employees']

    add_tools_to_project = forms.ModelMultipleChoiceField(
        queryset=Tools.objects.filter(project_id=1).order_by('geometry', 'material', 'diameter_mm'), required=False)
