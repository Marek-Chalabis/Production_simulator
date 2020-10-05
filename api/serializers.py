import django_filters
from django.contrib.auth.models import User
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from erp.models import Tools, Projects, Producers, Employees
from informations.models import ShowInformations


class UserSerializer(FlexFieldsModelSerializer):
    image = serializers.ImageField(source='profile.image', use_url=True)
    branch = serializers.CharField(source='profile.branch')

    class Meta:
        model = User
        fields = ["id", 'username', 'first_name', 'last_name', 'email', 'branch', 'image']


class ShowInformationsSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ShowInformations
        fields = ['id', 'author', 'title', 'info', 'date_posted']
        read_only_fields = ['date_posted', 'author']


class AdminStaffShowInformationsSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ShowInformations
        fields = '__all__'


class ShowInformationsFilter(django_filters.FilterSet):
    my = django_filters.BooleanFilter(method='user_objects')

    class Meta:
        model = ShowInformations
        fields = {
            "id": ['exact', 'in'],
            "author": ['exact', 'in'],
            "title": ['exact', 'icontains'],
            "info": ['exact', 'icontains'],
            "date_posted": ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'year', 'month', 'day', 'range']}

    def user_objects(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(author=self.request.user)
        return queryset


class EmployeesSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Employees
        fields = ['uuid_employee', 'first_name', 'last_name', 'email',
                  'phone_number', 'date_of_employment', 'position']
        depth = 1


class EmployeesDetailSerializer(FlexFieldsModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Employees
        fields = ['uuid_employee', 'first_name', 'last_name', 'email',
                  'phone_number', 'date_of_employment', 'position', 'projects']
        depth = 1

    def get_projects(self, object):
        return Projects.objects.values_list('project_id', flat=True).filter(employees=object)


class EmployeesFilter(django_filters.FilterSet):
    employees = django_filters.UUIDFilter(method='uuid_search')

    class Meta:
        model = Employees
        fields = {
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'phone_number': ['exact', 'icontains'],
            'date_of_employment': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'year', 'month', 'day', 'range'],
            'position': ['exact', 'in']}

    def uuid_search(self, queryset, name, value):
        return queryset.filter(uuid_employee=value)


class ProducersSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Producers
        fields = ["producer_id", "producer_name", "contact_person",
                  "phone_number", "email", "rabat", "delivery_time_days"]


class ProducersDetailSerializer(FlexFieldsModelSerializer):
    tools = serializers.SerializerMethodField()

    class Meta:
        model = Producers
        fields = ["producer_id", "producer_name", "contact_person",
                  "phone_number", "email", "rabat", "delivery_time_days", 'tools']

    def get_tools(self, object):
        return Tools.objects.values_list('tool_id', flat=True).filter(producer=object)


class ProjectsSerializer(FlexFieldsModelSerializer):
    employees = serializers.PrimaryKeyRelatedField(queryset=Employees.objects.select_related('position'),
                                                   many=True, pk_field=serializers.UUIDField(format='hex_verbose'),
                                                   required=False)
    tools_in_project = serializers.PrimaryKeyRelatedField(source='tools_set', many=True, read_only=True)
    tools_id = serializers.PrimaryKeyRelatedField(queryset=Tools.objects.filter(project_id=1).all(),
                                                  many=True, write_only=True, required=False)

    class Meta:
        model = Projects
        fields = ['project_id', 'project_name', 'time_for_project_hours', 'profit', 'employees', 'tools_in_project',
                  'tools_id']

    def create(self, validated_data):
        """updates tools and employees objects"""
        if 'tools_id' in validated_data:
            tools_to_update = validated_data.pop('tools_id')
        if 'employees' in validated_data:
            employees_to_project = validated_data.pop('employees')

        # creates new project
        new_project = Projects.objects.create(**validated_data)

        # check if there is data do update tools/employees
        if 'employees_to_project' in locals():
            new_project.employees.set(employees_to_project)
            new_project.save()
        if 'tools_to_update' in locals():
            for tool in tools_to_update:
                tool.project = new_project
            Tools.objects.bulk_update(tools_to_update, ['project'])

        return new_project


class ProjectsDetailSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Projects
        fields = ['project_id', 'project_name', 'time_for_project_hours', 'profit', 'employees', 'tools_set']
        depth = 1


class ProjectsFilter(django_filters.FilterSet):
    employees = django_filters.UUIDFilter(method='uuid_search')

    class Meta:
        model = Projects
        fields = {
            'project_id': ['exact', 'in'],
            'project_name': ['exact', 'icontains'],
            'time_for_project_hours': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'range'],
            'profit': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'range'], }

    def uuid_search(self, queryset, name, value):
        return queryset.filter(employees__uuid_employee=value)


class ToolsSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Tools
        fields = [
            'tool_id', 'geometry', 'material', 'diameter_mm', 'shank_diameter_mm', 'tool_radius_mm',
            'tool_length_mm', 'working_part_length_mm', 'compensation_mm', 'producer',
            'status', 'price', 'date_of_purchase', 'project']
        read_only_fields = ['date_of_purchase']


class ToolDetailSerializer(FlexFieldsModelSerializer):
    producer = ProducersSerializer(read_only=True)
    project = ProjectsSerializer(read_only=True)

    class Meta:
        model = Tools
        fields = [
            'tool_id', 'geometry', 'material', 'diameter_mm', 'shank_diameter_mm', 'tool_radius_mm',
            'tool_length_mm', 'working_part_length_mm', 'compensation_mm', 'producer',
            'status', 'price', 'date_of_purchase', 'project']


class ToolsFilter(django_filters.FilterSet):
    class Meta:
        model = Tools
        fields = {
            'tool_id': ['exact', 'in'],
            'geometry': ['exact', 'icontains'],
            'material': ['exact', 'icontains'],
            'diameter_mm': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'range'],
            'shank_diameter_mm': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'range'],
            'tool_radius_mm': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'range'],
            'tool_length_mm': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'range'],
            'working_part_length_mm': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'range'],
            'compensation_mm': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'range'],
            'producer': ['exact', 'in'],
            'status': ['exact', 'icontains'],
            'price': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'range'],
            'date_of_purchase': ['exact', 'icontains', 'gt', 'gte', 'lt', 'lte', 'year', 'month', 'day', 'range'],
            'project': ['exact', 'in']}
