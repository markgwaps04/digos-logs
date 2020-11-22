from django.urls import path;
from django.contrib import admin
from . import views

urlpatterns = [
    path("logout", views.request_logout, name="login"),
    path("user/account/details", views.template_profile_set, name="login"),
    path("user/account/details/request", views.request_database_add_personal_details, name="login"),
];
