from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ShowInformationsViewSets, ToolsViewSets, ProjectsViewSets, EmployeesViewSets, \
    ProducersViewSets

router = DefaultRouter()
router.register('users', UserViewSet, basename='users_api')
router.register('informations', ShowInformationsViewSets, basename='informations_api')
router.register('tools', ToolsViewSets, basename='tools_api')
router.register('projects', ProjectsViewSets, basename='projects_api')
router.register('employees', EmployeesViewSets, basename='employees_api')
router.register('producers', ProducersViewSets, basename='producers_api')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('get-token', views.obtain_auth_token)
]