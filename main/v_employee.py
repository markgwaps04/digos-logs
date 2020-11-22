import sys;
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import logout
from modules import helpers
from django.shortcuts import redirect
import django;
from django.contrib.auth.models import Group
from main.models import UserProfile;

# Create your views here.


def is_personal_set(user):
    try:
        user_profile = UserProfile.objects.get(user=user.id);
        if not user.first_name: return False;
        if not user.last_name: return False;
        return True;
    except UserProfile.DoesNotExist:
        return False;
    pass;


def is_not_personal_set(user):
    return not is_personal_set(user);
    pass;

def has_user_profile(user : User):
    return UserProfile.objects.filter(user=user).exists();
    pass;

def has_no_user_profile(user : User):
    return not UserProfile.objects.filter(user=user).exists();
    pass;


