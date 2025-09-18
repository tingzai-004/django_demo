from django import forms
from miao1.models import admin_list
from miao1 import models
from django.shortcuts import render ,redirect,HttpResponse
from miao1.code import check_code
from io import BytesIO
import hashlib
from django.core.paginator import Paginator
from miao1.bootstrap import BootStrapModelForm,BootStrapForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

#md5加密
def md5(data_string):
    if data_string is None:
        # 可以选择返回一个默认值，或者抛出更明确的异常
        raise ValueError("Cannot encode None value")
    obj = hashlib.md5()
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()

##新建管理员表单
class adminmodelform( BootStrapModelForm):
    s_password=forms.CharField(max_length=20,label="确认密码",widget=forms.PasswordInput(render_value=True))
    password=forms.CharField(max_length=20,label="密码",widget=forms.PasswordInput(render_value=True))
    phone=forms.CharField(label="手机号",validators=[RegexValidator(r'^1[3-9]\d{3}$', '手机格式错误')])

    class Meta:
        model=admin_list
        fields=[
            'name','password','s_password','phone'
        ]
    """ # def clean_password(self):
    #     pwd=self.cleaned_data.get('password')
    #     if pwd and pwd.isdigit():
    #         return pwd
    #     raise ValidationError('密码不能是纯数字')##错误信息不显示的问题"""
    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        pwd=md5(pwd)
        return pwd

    def clean(self):
        pwd=self.cleaned_data.get('password')
        s_pwd=md5(self.cleaned_data.get('s_password'))
        if pwd!=s_pwd:
            raise ValidationError('两次密码不一致')  
        return self.cleaned_data
            
class admineditormodelform(BootStrapModelForm):
    phone=forms.CharField(label="手机号",validators=[RegexValidator(r'^1[3-9]\d{3}$', '手机格式错误')])
    class Meta:
        model=admin_list
        fields =[
            'name','phone'
        ]
    

        
 
class adminresetform(BootStrapModelForm):
    s_password=forms.CharField(max_length=20,label="确认密码",widget=forms.PasswordInput(render_value=True),error_messages={
            'required': '密码不能为空',
            'min_length': '密码长度不能少于6位'
        })
    password=forms.CharField(max_length=20,label="密码",widget=forms.PasswordInput(render_value=True))
    class Meta:
        model=admin_list
        fields=[
            'password','s_password'
        ]
        widgets={
            "password":forms.PasswordInput(render_value=True),   
        }
    def clean_password(self):
        pwd=self.cleaned_data.get('password')
        md_pwd=md5(pwd)   
        abc= models.admin_list.objects.filter(id=self.instance.pk,password=md_pwd).exists()#因为密码可能相同，id不可能相同
        if abc:
            raise forms.ValidationError('新密码不能与旧密码相同')
        return md_pwd

    def clean(self):
        pwd=self.cleaned_data.get("password")
        s_pwd=md5(self.cleaned_data.get('s_password'))
        if pwd!=s_pwd:
            raise forms.ValidationError('密码不一致')
        return self.cleaned_data


##登录表单
class longinform(BootStrapForm):
    name=forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class":"form-control"})
    )
    password=forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class":"form-control"},render_value=True)
    )
    code=forms.CharField(
        label="验证码",
        widget=forms.TextInput
    )
    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        return md5(pwd)
    


#管理员列表
def  admin_dict(request):
    """检查用户是否已经登录，检查用户是否有cookies，拿随机字符串去看session中有没有，有就登录，没有就跳转到登录页面"""
    # info=request.session['info']
    # print(info)
    # if not info:
    #     return redirect('/login/')
    # print(request.session.get("info")) 
    disct={}
    value=request.GET.get('f',"")
    # print("查询的是",value)
    if value:
        disct['name__contains']=value
    form=models.admin_list.objects.filter(**disct)
   
    return render(request,'admin_list.html',{"form":form})


##新建管理员
def admin_add(request):
    if request.method == "GET":
        form = adminmodelform()
        return render(request, 'admin_add.html', {"form": form, "title": "新建管理员"})
    form = adminmodelform(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin_list/')
    # 如果验证失败，返回带有错误信息的表单
    # error=form.errors.get("__all__")
    return render(request, "info_add.html", {"form": form, "title": "新建管理员"})

#管理员编辑
def admin_editor(request,id):
    row_obj=models.admin_list.objects.filter(id=id).first()
    if row_obj ==None:
        return HttpResponse("用户不存在")
    if request.method=="GET":
        form=admineditormodelform(instance=row_obj)
        return render(request,'admin_editor.html',{"form":form})
    form=admineditormodelform(data=request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('admin_list')
    return render(request,'admin_editor.html',{'form':form})

#管理删除
def admin_delete(request,id):
    models.admin_list.objects.filter(id=id).first().delete()
    return redirect('admin_list')


    




#重置密码
def admin_rest(request,id):
    row_objects=models.admin_list.objects.filter(id=id).first()
    if row_objects==None:
            return HttpResponse('用户不存在')
    if request.method=="GET":
        title="重置密码-{}".format(row_objects.name)
        form=adminresetform()
        return render(request,"admin_rest.html",{"title":title,"form":form})
    form=adminresetform(data=request.POST,instance=row_objects)
    if form.is_valid():
        form.save()
        return redirect('/admin_list/')
    return render (request,"admin_rest.html",{"form":form})

#登录
def login_ing(request):
    if request.method=="GET":
        form=longinform()
        return render(request,"login.html",{"form":form})
    form=longinform(data=request.POST)
    if form.is_valid():
        code_input=form.cleaned_data.pop('code')
        code=request.session.get('image_code',"")
        if code.upper()!=code_input.upper():
            form.add_error('code','验证码错误')
            return render(request,'login.html',{'form':form})

        longin_data=models.admin_list.objects.filter(**form.cleaned_data).first()
        if longin_data:
            request.session["info"]=longin_data.name
            request.session['user_type'] = longin_data.user_type  # 记录用户类型
            request.session.set_expiry(7200)#设置时间过期为两个小时
            # request.session.modified = True
            return redirect('/admin_list/')
   
        form.add_error('password','用户名或密码错误')
    return render(request,"login.html",{"form":form})



# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         # 验证用户是否存在
#         try:
#             user_obj = user.objects.get(username=username, password=password)
#             # 登录成功：把用户信息存入session（Django的会话机制）
#             request.session['user_id'] = user_obj.id
#             request.session['user_type'] = user_obj.user_type  # 记录用户类型
#             return redirect('dorm_list')  # 跳转到宿舍列表页
#         except user.DoesNotExist:
#             messages.error(request, '用户名或密码错误')
    
#     return render(request, 'login.html')



##注销
def logout(request):
    request.session.clear()
    return redirect('/login/') 
    

##图片验证码
def  image_code(request):
    """调用pillow"""
    img,code=check_code()

    #写入到自己的session中（后面校验要用，后面还会删除）
    request.session['image_code']=code#image_code是什么自己设置的那个不是叫info
    """设置60s超时"""
    request.session.set_expiry(60)

    stream=BytesIO()##写在文件上还得打开文件，所以选择写在内存中，为什么要给用户的调用者返还图片中的对象？
    #创建内存字节流对象
    img.save(stream,'png')#以png形式保存在内存中
    return HttpResponse(stream.getvalue())#getvalue的作用是提取内存流中的二进制数据，
    #httpresponse是给调用者返回一个响应对象，响应对象中包含了图片的二进制数据

#导入分页
# def my_view(request):
#     item_list = admin_list.objects.all()
#      # 每页10条数据
    
#     return render(request, 'template.html', {'page_obj': page_obj})
