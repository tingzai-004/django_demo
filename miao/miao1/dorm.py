from miao1 import models
from django.shortcuts import render ,redirect,HttpResponse,get_object_or_404
from miao1.models import dorm,balance
from django import forms
from miao1.bootstrap import BootStrapModelForm,BootStrapForm

class dorm_addmodelform(BootStrapModelForm):
    class Meta:
        model=dorm
        fields=["depart","building","user_name","dorm_number"]
class balance_addmodelform(BootStrapModelForm):
    class Meta:
        model=balance
        fields=["dorm_number","people_number","balance_one","status"]

##宿舍列表
def dorm_list(request):
    
    dict={}
    search_data=request.GET.get("q","")
    if search_data:
        dict['dorm_number__contains']=search_data
    form=models.dorm.objects.filter(**dict)

    return render (request,"dorm_list.html",{"form":form})
#宿舍添加：

def dorm_add(request):
    if request.method=="GET":
        form=dorm_addmodelform()
        return render(request,'dorm_add.html',{"form":form,"title":"新建宿舍"})
    form=dorm_addmodelform(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/dorm_list/')
    return render(request,'dorm_add.html',{"form":form,"title":"新建宿舍"})

#宿舍编辑
def dorm_editor(request,id):
    row_object=get_object_or_404(dorm,dorm_number=id)
    if request.method=="GET":
        form=dorm_addmodelform(instance=row_object)
        title="修改-{}的信息".format(row_object.dorm_number)
        return render(request,"dorm_add.html",{"form":form,"title":title})
    form=dorm_addmodelform(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/dorm_list/')
    return render(request,"dorm_add.html",{"form":form})

def dorm_delete(request,id):
    models.dorm.objects.filter(dorm_number=id).delete()
    return redirect('/dorm_list/')

##水电
def balance(request):
    dict={}
    search_data=request.GET.get("q","")
    if search_data:
        dict[dorm_title__contains]=search_data
    form=models.balance.objects.filter(**dict)
    return render(request,"balance.html",{"form":form})

def balance_add(request):
    if request.method=="GET":
        form=balance_addmodelform()
        return render(request,'dorm_add.html',{"form":form})
    form=balance_addmodelform(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/balance/")
    return render(request,"dorm_add.html",{"form":form})
    
def balance_editor(request,id):
    row_object=get_object_or_404(model=balance,id=id)
    if request.method=="GET":
        form=balance_addmodelform(instance=row)
        return render(request,'dorm_add.html',{"form":form})

# def data(request):
    for i in range(50):
        form=models.dorm.objects.create(dorm_number=431,building="D8",depart_id=3,user_name="李思")
#         form.save()
#     return HttpResponse("添加成功")



        