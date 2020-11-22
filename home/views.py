import sys;
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import logout
from modules import helpers
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test;
from main.models import Log, \
    Out, \
    Person, \
    Department, \
    TempPerson, \
    UserProfile, Document_type, Log_details;
from datetime import datetime;
from django.db.models import Q, Value, Count;
from django.core.paginator import Paginator;
from main.v_employee import \
    has_user_profile, \
    is_not_personal_set, \
    is_personal_set, \
    has_no_user_profile;
import pdb;
from home.models import Article, Comment, Post


# Create your views here.

@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def home(request):

    of_department = Department.objects.all().order_by("name");
    of_document_type = Document_type.objects.all().order_by("name");

    return render(request, "home.html", {
        'title': "HOME",
        "user": request.user,
        "init": "",
        "departments" : of_department,
        "documents" : of_document_type
    });


pass;


@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def log(request):
    return render(request, "add_log.html", {
        'title': "HOME",
        "user": request.user,
        "department": Person.departmentOf,
        "init": ""
    });

    pass;


@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def add_log(request):
    return render(request, "add_log.html", {
        'title': "HOME",
        "user": request.user,
        "department": Person.departmentOf,
        "init": ""
    });

    pass;


@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def request_log_search(request):
    try:
        constraint = helpers.constraint(request, "POST");
        data = constraint.safe({
            "firstname": True,
            "lastname": True,
            "middlename": False,
            "pageIndex": True,
            "pageSize": True
        });

        of_person = TempPerson.objects.filter(
            Q(fullname__icontains=data['firstname']),
            Q(fullname__icontains=data['lastname']),
            Q(first_name__icontains=data['firstname']) |
            Q(last_name__icontains=data['lastname']) |
            Q(middle_name__icontains=data['middlename'])
        ).order_by("-id");

        if not of_person: return HttpResponse();

        split = Paginator(of_person, int(data["pageSize"]));
        split_by = split.page(int(data['pageIndex']));
        data_splitted = split_by.object_list;

        of_user = UserProfile.objects.get(user=request.user.id);

        for per in data_splitted:
            of_in_last = Log.objects.filter(
                details__person_visitor_id=per.id,
                added_by__department_id=of_user.department_id
            ).order_by("-id").first();

            per.last_in = of_in_last;

            pass;

        return render(request, "ajax_temp/person_list.html", {
            'data': data_splitted,
            "params": data,
            "itemCount": len(of_person)
        });

    except helpers.InvalidRequest:
        return HttpResponse();
    pass;

    pass;


@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def request_temp_visitor_add(request):
    try:
        constraint = helpers.constraint(request, "POST");
        data = constraint.safe({
            "firstname": True,
            "lastname": True,
            "middlename": False
        });

        of_department = Department.objects.all().order_by("name");
        of_user_profile = UserProfile.objects.get(id=request.user.id);

        return render(request, "ajax_temp/action_type_new_visitor.html", {
            'data': data,
            "of_date": datetime.now(),
            "department": of_department,
            "user_profile" : of_user_profile,
            "document_type": Document_type.objects.all().order_by("name"),
            "log_type": Log.TypeOf
        });


    except helpers.InvalidRequest:
        return HttpResponse('Gago');
    pass;

    pass;


@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def request_temp_old_visitor(request):
    constraint = helpers.constraint(request, "POST");
    data = constraint.safe({
        "visitor_id": True
    });

    of_department = Department.objects.all().order_by("name");

    of_user = UserProfile.objects.get(user_id=request.user.id);

    of_person = Person.objects.get(id=data['visitor_id']);

    of_log = Log.objects.filter(
        details__person_visitor_id=of_person,
        added_by__department_id=of_user.department_id
    ).order_by("-id").first();

    return render(request, "ajax_temp/action_type_old_visitor.html", {
        'data': data,
        "person": of_person,
        "of_date": datetime.now(),
        "last_log": of_log,
        "department": of_department,
        "obj_log" :Log,
        "document_type" : Document_type.objects.all().order_by("name"),
    });


# Ajax add new data
@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def database_add_new_visitor(request):

    constraint = helpers.constraint(request, "POST");
    data = constraint.safe({
        "contact_number": False,
        "department": False,
        "first_name": True,
        "last_name": True,
        "middle_name": False,
        "gender": True,
        "purpose": False,
        "type": True,
        "contact_number2": False,
        "document_type": False,
        "document_from": False
    });

    of_user = UserProfile.objects.get(user=request.user.id);

    person_params = {
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "middle_name": data['middle_name'],
        "gender": data['gender'],
        "added_by": of_user
    };

    if data['contact_number']:
        person_params['contact_number'] = data['contact_number'];
        pass;

    if data['department']:
        person_params['department'] = Department.objects.get(id=data['department']);

    of_person = Person(**person_params);

    of_person.full_clean();
    of_person.clean();
    of_person.save();

    log_details_params = {
        "person_visitor": of_person,
        "contact_number":data['contact_number2'],
        "added_by" : of_user
    };

    if data['document_type']:
        log_details_params['document_type'] = Document_type.objects.get(id=data['document_type']);

    if data['document_from']:
        log_details_params['document_from'] = Department.objects.get(id=data['document_from']);

    of_log_details = Log_details(**log_details_params);

    of_log_details.full_clean();
    of_log_details.clean();
    of_log_details.save();

    of_log = Log(
        type=data['type'],
        purpose=data['purpose'],
        details=of_log_details,
        added_by=of_user
    );

    try:
        of_log.full_clean();
        of_log.clean();
        of_log.save();
    except e :
        of_log_details.delete();
        raise Exception(e);
        pass;

    return render(request, "ajax_temp/after_added_new_log.html", {
        'log': of_log,
        "obj_log" : Log,
        "log_details_person" : of_log.details.person_visitor
    });


@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def database_add_new_log(request):
    constraint = helpers.constraint(request, "POST");
    data = constraint.safe({
        "contact_number2": False,
        "purpose": False,
        "type": True,
        "visitor_id": True,
        "document_from": False,
        "document_type" : False
    });

    try:
        of_user = UserProfile.objects.get(user=request.user.id);
        of_person = Person.objects.get(id=data['visitor_id']);

        log_details_params = {
            "person_visitor": of_person,
            "contact_number":data['contact_number2'],
            "added_by" : of_user
        };

        if data['document_type']:
            log_details_params['document_type'] = Document_type.objects.get(id=data['document_type']);

        if data['document_from']:
            log_details_params['document_from'] = Department.objects.get(id=data['document_from']);

        of_log_details = Log_details(**log_details_params);

        of_log_details.full_clean();
        of_log_details.clean();
        of_log_details.save();

        of_log = Log(
            type=data['type'],
            purpose=data['purpose'],
            details=of_log_details,
            added_by=of_user
        );

        try:
            of_log.full_clean();
            of_log.clean();
            of_log.save();
        except e :
            of_log_details.delete();
            raise Exception(e);
            pass;

        return render(request, "ajax_temp/after_added_new_log.html", {
            'log': of_log,
            "obj_log" : Log,
            "log_details_person" : of_log.details.person_visitor
        });

    except Person.DoesNotExist:
        raise UserProfile.DoesNotExist("Index id of Person object does not exists");

    except UserProfile.DoesNotExist:
        raise UserProfile.DoesNotExist("Index id of UserProfile object does not exists");

    except helpers.InvalidRequest:
        return HttpResponse('Invalid Request');

    pass;


@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def populate_list_log(request):
    constraint = helpers.constraint(request, "POST");
    data = constraint.safe({
        "pageIndex": True,
        "pageSize": True,
        "firstname" : False,
        "lastname" : False,
        "middlename" : False,
        "department" : False,
        "document_type" : False,
        "state_in_out" : False,
        "tracing_code" : False,
        "start_date" : False,
        "end_date" : False
    }, True);

    of_user = UserProfile.objects.get(user_id=request.user.id);

    of_log = Log.objects.filter(
        added_by__department_id=of_user.department_id
    );

    if data['firstname']  :
        of_log = of_log.filter(
            Q(details__person_visitor__first_name__icontains=data['firstname'])
        )
        pass;

    if data['lastname']  :
        of_log = of_log.filter(
            Q(details__person_visitor__last_name__icontains=data['lastname'])
        )
        pass;

    if data['tracing_code']  :
        of_log = of_log.filter(
            Q(details__tracing_code__icontains=data['tracing_code'])
        )
        pass;


    if data['department']  :
        of_log = of_log.filter(
            Q(details__document_from=data['department']) |
            Q(details__person_visitor__department=data['department'])
        )
        pass;


    if data['document_type']  :
        of_log = of_log.filter(
            Q(details__document_type_id=data['document_type'])
        )
        pass;


    if data['state_in_out']  :
        of_log = of_log.filter(
            Q(type=Log.IN_AND_OUT),
            Q(is_out=int(data['state_in_out']) > 0)
        )
        pass;

    if data['start_date'] and data['end_date']:

        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d");
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d");
        of_log = of_log.filter(Q(date__range=(start_date, end_date)));

        pass;

    of_log = of_log.order_by("-date","-time")

    if len(of_log):

        split = Paginator(of_log, int(data["pageSize"]));
        split_by = split.page(int(data['pageIndex']));
        data_splitted = split_by.object_list;

        for per in data_splitted:
            of_out = Out.objects.filter(log_id=per.id).last();
            per.out = of_out;
    else:
        data_splitted = [];
        pass;


    return render(request, "ajax_temp/log_list.html", {
        'data': data_splitted,
        'itemCount': len(of_log),
        "params" : data,
        "LOG" : Log
    });


@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def request_temp_log_more_details(request):
    try:
        constraint = helpers.constraint(request, "POST");
        data = constraint.safe({
            "log_id": True,
        });

        of_user = UserProfile.objects.get(user_id=request.user.id);

        of_log = Log.objects.get(
            id=data['log_id'],
            added_by__department_id=of_user.department_id
        );


        return render(request, "ajax_temp/log_details.html", {
            'data': of_log,
            'out': of_log.out(),
            "is_out": of_log.is_out_provided(),
            "LOG" : Log
        });


    except Log.DoesNotExist:
        raise Log.DoesNotExist("Index id of Log object does not exists");

    except UserProfile.DoesNotExist:
        raise UserProfile.DoesNotExist("Index id of UserProfile object does not exists");

    except helpers.InvalidRequest:
        raise helpers.InvalidRequest("Parameters does not supply required fields")
    pass;

    pass;


@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def database_save_as_out(request):
    try:
        constraint = helpers.constraint(request, "POST");
        data = constraint.safe({
            "log_id": True,
            "receiver_name": False,
            "description": False
        });

        of_user = UserProfile.objects.get(user_id=request.user.id);

        of_log = Log.objects.get(
            id=data['log_id'],
            added_by__department_id=of_user.department_id,
        );

        of_out = Out(
            receiver_name=data['receiver_name'],
            log=of_log,
            description=data['description'],
            added_by=of_user
        );

        of_out.full_clean();
        of_out.clean();
        of_out.save();

        of_log.is_out = True;
        of_log.save();


        return render(request, "ajax_temp/log_details.html", {
            'data': of_log,
            'out': of_log.out(),
            "is_out": of_log.is_out_provided(),
            "LOG" : Log
        });


    except Log.DoesNotExist:
        raise Log.DoesNotExist("Index id of Log object does not exists");

    except UserProfile.DoesNotExist:
        raise UserProfile.DoesNotExist("Index id of UserProfile object does not exists");

    except helpers.InvalidRequest:
        raise helpers.InvalidRequest("Parameters does not supply required fields")
    pass;



@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def get_tracing_code_info(request):

    try:
        constraint = helpers.constraint(request, "POST");
        data = constraint.safe({
            "tracing_code": True
        });

        of_user_profile = UserProfile.objects.get(id=request.user.id);

        of_log_details = Log_details.objects.get(
            tracing_code=data['tracing_code']
        );

        is_department_log = of_log_details\
                                .added_by\
                                .department_id == of_user_profile.department_id;

        return render(request, "ajax_temp/action_tracking_code_info.html", {
            'log_details': of_log_details,
            'is_department_log' : is_department_log,
            "obj_log" : Log,
            "log_details_person" : of_log_details.person_visitor
        });

    except Log_details.DoesNotExist:
        raise Log.DoesNotExist("Log details id does not exists");

    except UserProfile.DoesNotExist:
        raise UserProfile.DoesNotExist("Index id of UserProfile object does not exists");

    except helpers.InvalidRequest:
        raise helpers.InvalidRequest("Parameters does not supply required fields")
    pass;

    pass;


@login_required(login_url="/")
@user_passes_test(test_func=is_personal_set, login_url="/user/account/details")
def log_remove(request):

    constraint = helpers.constraint(request, "POST");
    data = constraint.safe({
        "log_id": True
    });

    of_log = Log.objects.get(id=data['log_id']);
    of_log.delete();

    return render(request, "ajax_temp/successfully_remove_new_log.html", {
        "data" : of_log
    });

