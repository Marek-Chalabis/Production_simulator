from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('informations.urls'), name='informations'),
    path('ERP/', include('erp.urls'), name='erp'),

    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('profile/', user_views.profile, name='profile'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView
         .as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete', auth_views.PasswordResetCompleteView
         .as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
