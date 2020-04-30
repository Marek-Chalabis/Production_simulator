import django_filters
from .models import Tools, Projects, Employees, Producers


class ToolsFilter(django_filters.FilterSet):

    # list of projects
    # project_list = Projects.objects.values_list('project_name', flat=True)
    # print(list(zip(project_list, project_list)))
    # print(type(project_list))
    tool_radius_mm = django_filters.RangeFilter(label='Range of radius')
    diameter_mm = django_filters.RangeFilter(label='Range of diameter')
    # todo check for perf --API
    #project = django_filters.ChoiceFilter(label='Project', method='get_tools_for_project', choices=project_list)
    project = django_filters.ModelChoiceFilter(queryset=Projects.objects.all())

    class Meta:
        model = Tools
        fields = ['project', 'geometry', 'material', 'diameter_mm', 'tool_radius_mm']

    # def get_tools_for_project(self, queryset, name, value):
    #     """
    #     Returns tools in specific project
    #     """
    #     print('*'*45)
    #     print(value)
    #     print(name)
        # if value == 'Yes':
        #     return queryset.exclude(id__in=not_able_donation_id)
        # elif value == 'No':
        #     return queryset.filter(id__in=not_able_donation_id)


class ProjectsFilter(django_filters.FilterSet):

    project_name = django_filters.CharFilter(lookup_expr='icontains')
    time_for_project_hours = django_filters.RangeFilter(label="Range of time for project")
    profit = django_filters.RangeFilter(label="Range of profit")

    class Meta:
        model = Projects
        fields = ['project_name', 'time_for_project_hours', 'profit']


class EmployeesFilter(django_filters.FilterSet):

    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    date_of_employment = django_filters.DateFromToRangeFilter(label='Date range(yyyy-mm-dd)')

    class Meta:
        model = Employees
        fields = ['first_name', 'last_name', 'position', 'date_of_employment']


class ProducersFilter(django_filters.FilterSet):

    producer_name = django_filters.CharFilter(lookup_expr='icontains')
    contact_person = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Producers
        fields = ['producer_name', 'contact_person']
