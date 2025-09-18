from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render ,redirect

class M1(MiddlewareMixin):
    def process_request(self,request):
        ##排除那些不想要登录就能访问的页面
        if request.path_info  in [  "/login/","/imag/code/"]:
            # print("登录页面")
            return 
        ##读取当前访问的用户的session信息，如果能读到，说明已登录过，就可以在继续向后走。
        info_dict=request.session.get('info')
        if  info_dict:
            return
        ##如果没有登录过，就跳转到登录页面
        return redirect('/login/')
        
       