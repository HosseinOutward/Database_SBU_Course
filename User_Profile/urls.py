from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(template_name='base_panel/home.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='page-login.html'), name='login'),

    path('', home_page, name='base-home'),

    path('employee/', WorkerCreateView.as_view(), name='employee-create'),
    path('registration/', ClientCreateView.as_view(), name='client-create'),
    path('profileUpdate/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('profile/delete/', UserDeleteView.as_view(), name='user-delete'),
]
