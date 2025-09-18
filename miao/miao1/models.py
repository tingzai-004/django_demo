from django.db import models

# Create your models here.
class depart(models.Model):
    depart_title=models.CharField(max_length=50,verbose_name="部门名称")
    depart_number=models.CharField(max_length=50,verbose_name="部门人数",default=6)
    def __str__(self):
        return self.depart_title
    
class user (models.Model):
    name=models.CharField(max_length=50,verbose_name="员工姓名")
   
    password = models.CharField(verbose_name="密码", max_length=64)
    age=models.IntegerField(verbose_name="年龄")
    data=models.DateField(verbose_name="入职时间")
    depart=models.ForeignKey(to='depart',to_field='id',on_delete=models.CASCADE)
    dorm_number=models.ForeignKey(to='dorm',to_field='dorm_number',on_delete=models.CASCADE,null=True,blank=True)
    gender_choices=((1,"男"),(2,"女"),(0,"未知"),)
    gender=models.SmallIntegerField(verbose_name="性别",choices=gender_choices,default=0)
''' # row_obj=models.userinfo.objects.filter(id=nid).first()   
# form=usermodelform(data=request.post,instance=row_obj)
#告诉Django表单，这不是在创建一个全新的数据，而是在「编辑一个已经存在的对象」。

# 拆解说明：
# row_obj 是你从数据库里查出来的那个老对象（比如ID为nid的用户信息）。

# request.POST 是用户新提交上来的表单数据。

# 如果你只传 data=request.POST，Django表单会认为：「好的，我们要用这些数据创建一个全新的用户。」

# 但如果你同时传了 instance=row_obj，Django表单就明白了：「噢，原来我们是拿着新提交的数据，来更新这个已经存在的老对象 (row_obj) 啊！」
# 把 instance 想象成一个 「身份牌」：

# 不给身份牌 (instance=None) -> 表单行为：「好的，我来造一个新员工。」

# 给一个老员工的身份牌 (instance=old_obj) -> 表单行为：「明白，我来给这个老员工更新一下信息。」

# 所以，只要你是在「编辑」或者「更新」，你就必须把这个「身份牌」（instance）带上。      
##用户编辑'''

##管理员列表

class admin_list(models.Model):
    name=models.CharField(max_length=50,verbose_name="姓名")
    password=models.CharField(max_length=50,verbose_name="密码")
    phone=models.CharField(max_length=120,verbose_name="手机号码")
    user_type = models.IntegerField(default=1)

class dorm(models.Model):
    dorm_number=models.AutoField(max_length=50,verbose_name="宿舍号",primary_key=True)
    depart=models.ForeignKey(to="depart",to_field="id",on_delete=models.CASCADE)
    user_name=models.CharField(max_length=50,verbose_name="宿舍负责人",default="张三")
    # user_id=models.ForeignKey(to="user",to_field="id",on_delete=models.CASCADE)
    building_choices=(("D5","D5栋"),("D8","D8栋"))
    building=models.CharField(max_length=8,choices=building_choices,default="D5",verbose_name="栋别")
    user_type = models.IntegerField(default=0)
    # def __str__(self):
    #     return self.bulding
    def __str__(self):
        return str(self.dorm_number)

class balance(models.Model):
    dorm_number=models.OneToOneField(to="dorm",to_field="dorm_number",on_delete=models.CASCADE)
    people_number=models.IntegerField(verbose_name="人数")
    balance_one=models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name="水电余额")
    status_choices=((1,"正常"),(2,"欠费"))
    status=models.SmallIntegerField(choices=status_choices,default=1,verbose_name="状态")


    
