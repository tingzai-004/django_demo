from django.shortcuts import render ,redirect,HttpResponse
from django import forms
from miao1.models import depart,user,admin_list
from miao1 import models
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from miao1.bootstrap import BootStrapModelForm,BootStrapForm






# Create your views here.
#部门表单
class myform(BootStrapForm):#8/19
    depart_title=forms.CharField(max_length=30,error_messages={"require":"字段不可为空"},label="部门")
    depart_number = forms.CharField(max_length=30, label="部门人数")
#部门添加
def dep_add(request):
    if request.method=="GET":
        form=myform()
        return render(request,"depart.html",{'form':form})
    form=myform(request.POST)
    if form.is_valid():
        data=form.cleaned_data
        models.depart.objects.create(**data)
        return redirect('/dep_list/')
    return render(request,"depart.html",{'form':form})

##在seting文件里面的language code改成“zh-hans"
#用modelform，出现错误后原来输入的值还在输入框，不会消失
    
    clean_error=form.error.get("__all__")
    return render (request,"info.html",{'form':form,'clean_error':clean_error})

#部门列表
def  dep_list(request):
    dict={}
    search_data=request.POST.get("f","")
    if search_data:
        dict["depart_title__contains"]=search_data
    depart_list=models.depart.objects.filter(**dict)
    return render(request,"depart_list.html",{"depart_list":depart_list})

#部门删除
def depart_delete(request,id):
    row_obj=models.depart.objects.filter(id=id).first()
    if row_obj:
        row_obj.delete()
        return redirect('/dep_list/')
    return HttpResponse("找不到")
      
class usermodelform(BootStrapModelForm):
    name=forms.CharField(max_length=3,label="姓名")#label是框里的默认字，输入后消失
    # mobile=forms.CharField(label='手机号', validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机格式错误')],)#正则表达式规定手机号格式
   
    
    
    class Meta:
        model=user
        
        fields=['name','age','password',"data",'gender', 'depart']
    '''    # widgets={
        #      "name":forms.TextInput(attrs={"class:form-control"}),
        #      "password":forms.PasswordInput(attrs={"class":"form-control"}),#8/20 widgets是form插件 在html中自动生成输入框，自己定义样式
        # }
        # def __init__(self,*args,**kwargs):
        #      super().__init__(*args,**kwargs)
        #     # 循环找到所有的widget插件，添加form-control样式
        #      for name,field in self.fields.items():
        #           print(name,field)#field遍历的就是对象
        #           if name=="password":
        #                break#password这个字段不用这个样式
        #           field.widget.attrs={"class":"form-control"}'''
 ##用户列表                 
#用户列表+用户搜索+分页
##用户搜索放到用户列表里面
# 当用户没有搜索时：data_dict 保持 {} → 显示所有数据
# 当用户有搜索时：data_dict 变成 {"mobile__contains": value} → 只显示匹配数据
def info_list(request):
    data_list = {}
    search_data = request.GET.get('q', "")
    
    if search_data:
        data_list["name__contains"] = search_data
        '''创建一个搜索条件,让filter搜索'''
        
    """page = int(request.GET.get('page', 1))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size
    querset=models.user.objects.filter(**data_list).order_by("-age")[start:end]#**data_list把字典变成关键字参数
    
    total_count = models.user.objects.filter(**data_list).order_by("-age").count()  # 改为-age
    
    total_page_count, div = divmod(total_count, page_size)
    
    if div:
        total_page_count += 1

    plus = 5
    if total_page_count <= 2 * plus + 1:
        start_page = 1
        end_page = total_page_count + 1
    else:
        if page <= plus:##当前页码小于5
            start_page = 1
            end_page = 2 * plus + 1
        else:
            if page >= total_page_count - plus:#当前页码>zon数-5
                start_page = total_page_count - 2 * plus
                end_page = total_page_count + 1
            else:
                start_page = page - plus
                end_page = page + plus + 1

    page_str_list = []

    if page <= 1:
        prev = ' <li class="page-item"><a class="page-link" href="?page={}">上一页</a></li>'.format(1)
    else:
        prev = ' <li class="page-item"><a class="page-link" href="?page={}">上一页</a></li>'.format(page - 1)
    page_str_list.append(prev)

    for i in range(start_page, end_page):
        if i > total_page_count:
            break
        ele = ' <li class="page-item"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i) 
        page_str_list.append(ele)
    
    page_string = mark_safe("".join(page_str_list))

    if page >= total_page_count:
        next_page = ' <li class="page-item"><a class="page-link" href="?page={}">下一页</a></li>'.format(total_page_count)
    else:
        next_page = ' <li class="page-item"><a class="page-link" href="?page={}">下一页</a></li>'.format(page + 1)
    page_str_list.append(next_page)
    
    page_string = mark_safe("".join(page_str_list))"""
    

    query = models.user.objects.filter(**data_list).order_by("-age")[start:end]  # 这里已经改为-age
    
    return render(request, "info.html", {
        "query": query, 
        "search_data": search_data, 
        "page_string": page_string
        # "data_list":data_list
    })
               
##用户添加
def info_add(request):
        if request.method=="GET":
            form=usermodelform()
            
            return render(request,"info_add.html",{'form':form,"title":"新建用户"})#8/19
        form=usermodelform(data=request.POST)#这个form跟原来的空的表单不一样，会出现上一位输入的内容
        if form.is_valid():
             #默认保存的是用户输入的所有数据，如果想保存用户输入以外的值
            #  form.instance.字段名=值

             form.save()     #这里的form是一个被绑定用户提交数据且通过验证的实例
             return redirect('/info/')
        
        return render(request,"info_add.html",{"form":form,"title":"新建用户"})#如果数据错误，有数据的form对象会重新传回模版，所以用modelform，出现错误后原来输入的值还在输入框，不会消失


#用户更新
def info_editor(request,id):
    row=models.user.objects.filter(id=id).first()
    if row==None:
        return HttpResponse("用户不存在")
    elif request.method=="GET":
        form1=usermodelform(instance=row)
        return render (request,'info_editor.html',{"form1":form1})
    
    form1=usermodelform(data=request.POST,instance=row)
    if form1.is_valid():
        form1.save()
        return redirect('/info/')#URL不是html
    return render (request,'info_editor.html',{"form1":form1})

        

##用户删除
def info_delete(request,id):
    models.user.objects.filter(id=id).first().delete()
    return redirect('/info/')

from django.shortcuts import redirect
from django.utils.decorators import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            # 根据用户名查询用户
            user = User.objects.get(name=username)
        except User.DoesNotExist:
            # 如果查询不到用户（比如用户被删除等情况），重定向到登录页
            return redirect('login')
        # 校验是否为管理员（假设 user_type=1 是管理员）
        if user.user_type != 1:
            # 普通用户，重定向到仅查询的页面
            return redirect('dorm_list')
        return view_func(request, *args, **kwargs)
    return wrapper










    





   
    




    
    
    