from django.db import models
from datetime import date, datetime;
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.contenttypes.fields import GenericForeignKey;
from django.contrib.contenttypes.models import ContentType;



class Article(models.Model):
    content = models.CharField(default="", max_length=100,null=False, blank=False);
    pass;

class Post(models.Model):
    content = models.CharField(default="", max_length=100,null=False, blank=False);
    pass;

class Comment(models.Model):
    comm = models.CharField(default="", max_length=100,null=False, blank=False);
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=False,null=False);
    object_id = models.PositiveIntegerField();
    content_object = GenericForeignKey("content_type","object_id");
    pass;



