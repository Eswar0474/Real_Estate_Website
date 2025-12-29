"""
URL configuration for Real project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # The root URL of your app will show the registration page.
    # name='register' is a unique identifier for this URL pattern.
    path('register/', views.register_view, name='register'),

    # The URL for the login page.
    path('login/', views.login_view, name='login'),

    # The URL to handle user logout.
    path('logout/', views.logout_view, name='logout'),

    # The destination page for sellers after they log in.
    path('seller/', views.seller_page_view, name='seller_page'),

    # The destination page for buyers after they log in.
    path('buyer/', views.buyer_page_view, name='buyer_page'),
    path('settings/', views.settings_view, name='settings'),
    path('password-reset/', views.password_reset_verify_view, name='password-reset-verify'),
    path('password-reset/confirm/', views.password_reset_confirm_view, name='password-reset-confirm'),
    path('password-reset/<int:id>', views.password_reset, name='password-reset'),

]