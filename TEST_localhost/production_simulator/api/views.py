from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from erp.models import Tools, Projects, Employees, Producers
from informations.models import ShowInformations
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from . import page_pagination
from .permissions import AuthorOrAdminPermission
from .serializers import UserSerializer, \
    ShowInformationsSerializer, AdminStaffShowInformationsSerializer, \
    ShowInformationsFilter, \
    ToolsSerializer, ToolsFilter, ToolDetailSerializer, \
    ProjectsSerializer, ProjectsFilter, ProjectsDetailSerializer, \
    EmployeesSerializer, EmployeesFilter, EmployeesDetailSerializer, \
    ProducersSerializer, ProducersDetailSerializer


# ========USERS========


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin, ):

    queryset = User.objects.select_related('profile').filter(is_staff=False).order_by('id')
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    pagination_class = page_pagination.MediumPagination
    serializer_class = UserSerializer
    search_fields = ['username', 'last_name', 'email', 'profile__branch']

# =========INFORMATION========


@method_decorator(cache_page(60 * 60 * 6), name='dispatch')
class ShowInformationsViewSets(viewsets.ModelViewSet):

    queryset = ShowInformations.objects.order_by('-date_posted')
    permission_classes = [IsAuthenticatedOrReadOnly, AuthorOrAdminPermission]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    pagination_class = page_pagination.MediumPagination
    ordering_fields = ['author', 'id', 'date_posted']
    search_fields = ['title', 'info']
    filterset_class = ShowInformationsFilter

    def get_serializer_class(self):
        """only STAFF can modify all fields"""
        if self.request.user.is_staff:
            return AdminStaffShowInformationsSerializer
        return ShowInformationsSerializer

    def create(self, request, *args, **kwargs):
        """automatically adds author and current date unless staff makes/modify posts"""
        if self.request.user.is_staff:
            serializer = AdminStaffShowInformationsSerializer(data=request.data)
        else:
            serializer = ShowInformationsSerializer(data=request.data)
        if serializer.is_valid():
            if self.request.user.is_staff:
                serializer.save()
            else:
                serializer.save(author=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========TOOLS========


class ToolsViewSets(viewsets.ModelViewSet):

    queryset = Tools.objects.order_by('-diameter_mm', '-tool_radius_mm', '-tool_length_mm', '-working_part_length_mm')
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    pagination_class = page_pagination.BigPagination
    ordering_fields = [
            'tool_id', 'diameter_mm', 'shank_diameter_mm', 'tool_radius_mm',
            'tool_length_mm', 'working_part_length_mm', 'compensation_mm', 'price', 'date_of_purchase']
    filterset_class = ToolsFilter
    serializer_class = ToolsSerializer

    @action(detail=True, url_path='detail', methods=['GET'], permission_classes=[IsAuthenticated])
    def detail_object(self, request, *args, **kwargs):
        """ returns more detail information about project and producer"""
        object = Tools.objects.select_related('producer', 'project').get(pk=kwargs['pk'])
        serializer = ToolDetailSerializer(object)
        return Response(serializer.data)

# =========PROJECTS========


class ProjectsViewSets(viewsets.ModelViewSet):

    queryset = Projects.objects.prefetch_related('employees', 'tools_set').order_by('project_name')
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    pagination_class = page_pagination.SmallPagination
    filterset_class = ProjectsFilter
    ordering_fields = ['project_id', 'time_for_project_hours', 'profit']
    serializer_class = ProjectsSerializer

    @action(detail=True, url_path='detail', methods=['GET'], permission_classes=[IsAuthenticated])
    def detail_object(self, request, *args, **kwargs):
        """ returns more detail information about employees and tools"""
        object = Projects.objects.prefetch_related('employees', 'tools_set').get(pk=kwargs['pk'])
        serializer = ProjectsDetailSerializer(object)
        return Response(serializer.data)

# =========EMPLOYEES========


class EmployeesViewSets(viewsets.ModelViewSet):

    queryset = Employees.objects.select_related('position').order_by('last_name')
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    pagination_class = page_pagination.MediumPagination
    filterset_class = EmployeesFilter
    ordering_fields = ['date_of_employment', 'position']
    serializer_class = EmployeesSerializer

    @action(detail=True, url_path='detail', methods=['GET'], permission_classes=[IsAuthenticated])
    def detail_object(self, request, *args, **kwargs):
        """ returns all information about employee and list of projects that he/she is in """
        object = Employees.objects.select_related('position').get(pk=kwargs['pk'])
        serializer = EmployeesDetailSerializer(object)
        return Response(serializer.data)

# =========PRODUCERS========


class ProducersViewSets(viewsets.ModelViewSet):

    queryset = Producers.objects.order_by('producer_name')
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    pagination_class = page_pagination.SmallPagination
    search_fields = ['producer_name', 'contact_person', 'email', 'phone_number']
    ordering_fields = ['producer_id', 'rabat']
    serializer_class = ProducersSerializer

    @action(detail=True, url_path='detail', methods=['GET'], permission_classes=[IsAuthenticated])
    def detail_object(self, request, *args, **kwargs):
        """ returns detailed information about producer and list of tools provided by him/her """
        object = Producers.objects.get(pk=kwargs['pk'])
        serializer = ProducersDetailSerializer(object)
        return Response(serializer.data)
