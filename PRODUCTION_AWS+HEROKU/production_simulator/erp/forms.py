from django import forms
from django.db import models
from django.forms import ModelForm
from .models import Tools, Projects


class CreateProject(ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'

    add_tools_to_project = forms.ModelMultipleChoiceField(
        # widget=forms.CheckboxSelectMultiple,
        queryset=Tools.objects.filter(project_id=1).order_by('geometry', 'material', 'diameter_mm'))


