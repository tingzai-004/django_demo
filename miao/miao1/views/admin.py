##管理员列表
from django.shortcuts import render ,redirect,HttpResponse
from django import forms
from miao1.models import admin_list
from miao1 import models
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe

def  admin_dict(request):
    # disct=[]
    form=models.admin_list.objects.all()
    return render(request,'admin_list.html',{"form":form})