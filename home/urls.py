from django.urls import path;
from django.contrib import admin
from . import views

urlpatterns = [
    path("home", views.home, name="login"),
    path("log", views.log, name="add_log.html"),
    path("log/add", views.add_log, name="add_log.html"),
    path("log/add/request", views.request_temp_old_visitor, name="add_log.html"),

    # form request add data to the database

    path("log/new/request", views.database_add_new_log, name="successfully_added_new_log.html"),

    path("log/search", views.request_log_search, name="add_log.html"),
    path("visitor/add", views.request_temp_visitor_add, name="add_log.html"),
    path("visitor/add/request", views.database_add_new_visitor, name="add_log.html"),

    # ajax request populate list log
    path("log/populate", views.populate_list_log, name="log_list.html"),


    # ajax request return template
    path("log/details", views.request_temp_log_more_details, name="log_details.html"),


    # ajax request save database as out and return template
    path("log/out/save", views.database_save_as_out, name="log_details.html"),

    # ajax request return template
    path("log/tracing_code", views.get_tracing_code_info, name="log_details.html"),


    # ajax request return template
    path("log/remove", views.log_remove, name="remove log"),


];
