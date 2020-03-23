from django.urls import path
from . import views

urlpatterns = [
    path('', views.InformationsListView.as_view(), name='informations-home'),
    path('user/<str:username>', views.UserInformationsListView.as_view(), name='user-informations'),
    path('information/<int:pk>/', views.InformationsDetailView.as_view(), name='informations-detail'),
    path('information/new/', views.InformationsCreateView.as_view(), name='informations-create'),
    path('information/<int:pk>/update/', views.InformationsUpdateView.as_view(), name='informations-update'),
    path('information/<int:pk>/delete/', views.InformationsDeletelView.as_view(), name='informations-delete'),
]
