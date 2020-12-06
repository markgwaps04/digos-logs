from django.db import models
from datetime import date, datetime;
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.contenttypes.fields import GenericForeignKey;
from django.contrib.contenttypes.models import ContentType;
import random, string, pdb

# Create your models here.

class Document_type(models.Model):

    id = models.AutoField(primary_key=True);
    name = models.CharField(default="", max_length=200,null=False, blank=False);

    class Meta:
        verbose_name = 'Type of documents'
        verbose_name_plural = 'Type of documents'


    def __str__(self):
        return self.name;
        pass;

    pass;

class Department(models.Model):
    id = models.AutoField(primary_key=True);
    name = models.CharField(default="", max_length=100,null=False, blank=False);

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Deparment'


    def __str__(self):
        return self.name;
        pass;

    pass;


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True);
    user = models.OneToOneField(User,related_name="Profile", unique=True, on_delete=models.CASCADE,default=None,blank=False);
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True,null=True);

    pass;


class Person(models.Model):

    genderOf = [
        (0, 'Male'),
        (1, 'Female')
    ];
    id = models.AutoField(primary_key=True);
    first_name = models.CharField(default="", max_length=20, null=False, blank=False);
    last_name = models.CharField(default="", max_length=20,null=False, blank=False);
    middle_name = models.CharField(default="", max_length=20, null=True, blank=True);
    gender = models.IntegerField(default=0, choices=genderOf,blank=False,null=False);
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True,null=True);
    contact_number = models.BigIntegerField( null=True, blank=True);
    added_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=False,null=True);


    def visit_num(self, department_id):

        return Log.objects.filter(
            person_visitor_id=self.id,
            added_by__department__id=department_id
        ).count();

        pass;


    def last_visit(self, department_id):

        return Log.objects.filter(
            details__person_visitor__id=self.id,
            added_by__department__id=department_id
        ).order_by("-id").first();

        pass;


    pass;


class Log_details(models.Model):
    id = models.AutoField(primary_key=True);
    person_visitor = models.ForeignKey(Person,on_delete=models.CASCADE,blank=False,null=False);
    contact_number = models.TextField(null=True, blank=True);
    document_type =  models.ForeignKey(Document_type,on_delete=models.CASCADE,blank=True,null=True);
    document_from =  models.ForeignKey(Department, on_delete=models.CASCADE, blank=True,null=True);
    tracing_code = models.CharField(null=True, blank=True, max_length=100);
    added_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=False,null=True);

    def clean(self):

        if not self.tracing_code:
            self.tracing_code = Log_details.generate_unique_access_code();
            pass;

        pass;

    @staticmethod
    def generate_unique_access_code(length=5):

        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length));
        random_str = str(random_str).upper();

        is_exists = Log_details.check_access_code_is_exists(random_str);

        if is_exists:
            return Log_details.generate_unique_access_code(length+1);

        return random_str;

        pass;


    @staticmethod
    def check_access_code_is_exists(access_code : str):

        return Log_details\
            .objects\
            .filter(tracing_code=access_code)\
            .exists();

        pass;

    def refresh_map(self):
        has_exists = Log.objects.filter(details=self.id).exists();
        if not has_exists:
            self.delete();
            pass;
        pass;

    def log(self):

        return Log.objects.filter(details=self.id).first()

        pass;

    def last_log(self):

        return Log.objects\
            .filter(details=self.id)\
            .order_by("-id").first();

        pass;

    pass


class Log(models.Model):

    IN = 0;
    OUT = 1;
    IN_AND_OUT = 2;

    TypeOf = [
        (IN, 'In'),
        (OUT, 'Out'),
        (IN_AND_OUT, 'In and Out')
    ];

    id = models.AutoField(primary_key=True);
    type = models.IntegerField(default=0,choices=TypeOf,blank=False,null=False);
    date = models.DateField(null=False, default=date.today);
    time = models.TimeField(null=False, blank=False, default=datetime.now);
    purpose = models.TextField(null=True, blank=True);
    details = models.ForeignKey(Log_details,on_delete=models.CASCADE,blank=False,null=True);
    added_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=False,null=True);
    is_out = models.BooleanField(blank=False,null=False,default=False);
    date_now = models.DateTimeField(blank=False,null=False,default=datetime.now )


    def is_out_provided(self):
        return Out.objects.filter(log_id=self.id).exists();
        pass;

    def out(self):
        return Out.objects.filter(log=self.id).last();
        pass;

    def person_no_visit(self):

        return Log.objects.filter(
            details__person_visitor__id=self.details.person_visitor.id,
            added_by__department__id=self.added_by.department.id
        ).count();

        pass;

    def person_last_visit(self):

        return Log.objects.filter(
            details__person_visitor__id=self.id,
            added_by__department__id=self.added_by.department.id
        ).order_by("-id").first();

        pass;

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Log';


class Out(models.Model):
    id = models.AutoField(primary_key=True);
    log = models.ForeignKey(Log, on_delete=models.CASCADE,blank=False,null=False);
    receiver_name = models.CharField(default="", max_length=20,null=True, blank=True);
    date = models.DateField(null=False, default=date.today);
    time = models.TimeField(null=False, blank=False, default=datetime.now);
    description = models.TextField(null=True, blank=True);
    added_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=False,null=True);

    class Meta:
        verbose_name = 'Out'
        verbose_name_plural = 'Out'


class TempPerson(models.Model):
    first_name = models.CharField(default="", max_length=20, null=False, blank=False);
    last_name = models.CharField(default="", max_length=20,null=False, blank=False);
    middle_name = models.CharField(default="", max_length=20, null=True, blank=True);
    gender = models.IntegerField(default=0, choices=Person.genderOf,blank=False,null=False);
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True,null=True);
    contact_number = models.BigIntegerField(default=0, null=False, blank=False);
    fullname = models.TextField(default="", max_length=20, null=False, blank=False);
    added_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=False,null=True);

    class Meta:
        managed = False
        db_table = "vw_person";

    pass;


