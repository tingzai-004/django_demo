from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def user_list(request):
    # 获取所有数据
    user_list = User.objects.all()
    
    # 创建Paginator对象，每页显示10条
    paginator = Paginator(user_list, 10)
    
    # 获取当前页码
    page_number = request.GET.get('page')
    
    try:
        # 获取当前页的数据
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # 如果page参数不是整数，显示第一页
        page_obj = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，显示最后一页
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, 'dorm_list.html', {
        'page_obj': page_obj,
        'dorms': page_obj.object_list  # 当前页的数据
    })
"""page_obj.object_list - 当前页的对象列表

page_obj.number - 当前页码

page_obj.has_previous() - 是否有上一页

page_obj.has_next() - 是否有下一页

page_obj.previous_page_number() - 上一页页码

page_obj.next_page_number() - 下一页页码"""