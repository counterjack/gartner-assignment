from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from rest_framework import routers
from users.views import (
    ManagerDashboardAPI, AssociateDashboardAPI, DashboardRedirectAPI, LoginView, LogoutView, 
    ClientAttributeTransactionView)


urlpatterns = [
    path(r'', LoginView.as_view(), name="user-login"),
    path('logout/', LogoutView.as_view(), name="user-logout"),
    url(r'^dashboard', DashboardRedirectAPI.as_view(), name="dashboard"),
    url(r'^manager-dashboard', ManagerDashboardAPI.as_view(), name="manager-dashboard"),
    url(r'^associate-dashboard', AssociateDashboardAPI.as_view(), name="associate-dashboard"),
    url(r'action-on-attribute', ClientAttributeTransactionView.as_view(), name="action-on-attribute")
    # url(r'^forgot-password/$', ForgotPasswordFormView.as_view()),
]