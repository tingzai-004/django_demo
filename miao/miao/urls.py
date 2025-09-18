"""
URL configuration for miao project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from miao1 import views
from miao1 import admin_list,dorm,code


urlpatterns = [
    #部门
    path('admin/', admin.site.urls),
    path("dep_add/",views.dep_add),
    path('dep_list/',views.dep_list),
    path("depart/<int:id>/delete",views.depart_delete),
    ##宿舍
    path('dorm_list/',dorm.dorm_list),
    path('dorm_add/',dorm.dorm_add),
    path('dorm/<int:id>/editor/',dorm.dorm_editor),
    path('dorm/<int:id>/delete/',dorm.dorm_delete),
   ##水电费
    path("balance/",dorm.balance),
    path("balance_add/",dorm.balance_add),

    #用户
    path('info_add/',views.info_add), 
    path('info/<int:id>/delete/', views.info_delete), 
    path('info/<int:id>/editor/',views.info_editor),
    path('info/',views.info_list,name="info"),

    #管理员
    path('admin_list/',admin_list.admin_dict,name="admin_list"),
    path("admin_list/<int:id>/reset",admin_list.admin_rest),
    path("admin_add/",admin_list.admin_add),
    path("admin_list/<int:id>/editor/",admin_list.admin_editor),
    path('admin_list/<int:id>/delete/',admin_list.admin_delete),
    #登录
     path('login/',admin_list.login_ing,name="login"),
    path('logout/',admin_list.logout),
    path('imag/code/',admin_list.image_code),
    
    
   
]
