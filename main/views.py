import sys;
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import logout
from modules import helpers
from django.shortcuts import redirect
from main.models import  Department, UserProfile;
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required, user_passes_test;     
from main.v_employee import \
    has_user_profile, \
    is_not_personal_set , \
    is_personal_set, \
    has_no_user_profile;
from django.contrib.auth import logout

# Create your views here.



def index(request):

    if not request.user.is_authenticated :
        return redirect("/");

    group = request.user.groups.last();
    name = str(group.name).lower();

    return redirect("/" + name + "/home");

@login_required(login_url="/")
def request_logout(request):
    logout(request);
    return redirect("/");
    pass;


@login_required(login_url="/")
@user_passes_test(test_func=has_no_user_profile, login_url="/")
def request_database_add_personal_details(request):
    constraint = helpers.constraint(request, "POST");
    data = constraint.safe({
        "first_name": True,
        "last_name": True,
        "department": False
    });

    request.user.first_name = data['first_name'];
    request.user.last_name = data['last_name'];
    request.user.full_clean();
    request.user.clean();
    request.user.save();

    try:
        of_department = Department.objects.get(id=data['department']);

        of_user_profile = UserProfile(
            user=request.user,
            department= of_department
        );

        of_user_profile.full_clean();
        of_user_profile.clean();
        of_user_profile.save();

        return redirect("/");

    except Department.DoesNotExist:
        raise Department.DoesNotExist("Index id of department object does not exists");

    pass;

@login_required(login_url="/")
@user_passes_test(test_func=has_no_user_profile, login_url="/")
def template_profile_set(request):

    of_department = Department.objects.all().order_by("name");

    return render(request, "profile_set.html", {
        'title': "INFO",
        'department' : of_department,
        "user": request.user,
        "init": ""
    });

    pass;
