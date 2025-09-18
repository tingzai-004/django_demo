from django.contrib import admin
from miao1.models import user

# Register your models here.
admin.site.register(user)
    # name=models.CharField(max_length=50,verbose_name="员工姓名")

    # class Meta:
    #     db_table="user"
    #     verbose_name="用户表"
    #     verbose_name_plural=verbose_name