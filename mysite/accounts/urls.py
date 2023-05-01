from django.urls import re_path as url
from . import views
# from django.contrib.auth.views import (password_reset, password_reset_done, password_reset_confirm)
from django.contrib.auth.views import PasswordResetView
# from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'
urlpatterns = [
    url(r'logout/$', LogoutView.as_view (template_name='accounts/logout.html'), name='logout'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^profile/$', views.view_profile, name= 'view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name= 'edit_profile'),
    url(r'^profile/cancelled/$', views.cancel_subscription, name= 'cancel_subscription'),
    url(r'^change-password/$', views.change_password, name= 'change_password'),
    url(r'^profile/password/$', views.change_password, name= 'change_password'),
    url(r'^reset-password/$', PasswordResetView.as_view(), name='reset_password'),
    # url(r'^reset-password/done/$', password_reset_done.as_view(), name='password_reset_done'),
    # url(r'^reset-password/confirm/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^profile/update_card/$', views.update_card, name='update_card'),
    # url(r'', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'', LoginView.as_view(template_name='accounts/login.html'), name='login'),

]
