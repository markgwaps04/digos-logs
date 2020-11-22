import sys;
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import logout
from modules import helpers
from django.shortcuts import redirect
import django;

# Create your views here.

def login(request):

    if request.user.is_authenticated :

        if request.user.is_superuser: return redirect("/admin");
        else: return redirect("/home");

    return render(request, "auth/login.html", {
        'title': "HOME",
        "init": ""
    });


def request(request):

    if len(request.POST) > 0:

        # print(request.__class__.__name__);

        constraint = helpers.constraint(request);
        data = constraint.strict(["account", "password"], True);

        user = auth.authenticate(
            username=data['account'],
            password=data['password']
        );

        if user and not user.is_superuser:
            auth.login(request, user);
            return redirect("/home");

        str_message = """
        Please enter the correct username and password for a employee
        account. Note that both fields may be case-sensitive.
        """;

        messages.error(request, str_message);

    return redirect("/");
