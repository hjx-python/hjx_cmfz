import uuid

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from datetime import datetime
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from bannerapp.models import Banner


def banner_list(request):
    '''
    展示表格数据
    :param request:
    :return:
    '''
    '''
    获取rows(每页有多少条数据)和page(第几页);
    构造分页器对象,获取到该页的数据
    构造data
    返回
    '''
    def mydefault(b):
        if isinstance(b,Banner):
            print(type(b.pic))
            return {"id":b.id,"title":b.title,"status":(lambda x: "展示" if x else "不展示")(b.status),"create_time":str(b.create_time),"pic":str(b.pic) }

    rows = request.GET.get("rows")
    page_num = request.GET.get("page")
    Banner.objects.all()
    pagtor = Paginator(Banner.objects.all(),rows)
    page = pagtor.page(page_num)
    data = {
        "page":page_num,
        "total":pagtor.num_pages,
        "records":pagtor.count,
        "rows":list(page)
    }
    return JsonResponse(data=data,safe=False,json_dumps_params={"default":mydefault})

@csrf_exempt
def banner_opera(request):
    '''
    轮播图的增删改
    :param request:
    :return:
    '''
    '''
    获取oper参数,判断是增删改哪种操作,进行相应的代码书写
    '''
    oper = request.POST.get('oper')
    if oper == 'add':
        title = request.POST.get('title')
        status = request.POST.get('status')
        pic = request.FILES.get('pic')
        pic.name = str(uuid.uuid4())+"."+pic.name.split(".")[1]
        print(pic.name)
        # print(title,status,pic,type(pic))
        Banner.objects.create(title=title,status=(lambda x:1 if x=="展示" else 0)(status),create_time=datetime.now().strftime("%Y-%m-%d"),pic=pic )
    elif oper == "edit":
        id = request.POST.get('id')
        title = request.POST.get('title')
        status = request.POST.get('status')
        banner = Banner.objects.get(id=id)
        banner.title=title
        banner.status=1 if status=="展示" else 0
        banner.create_time=datetime.now().strftime("%Y-%m-%d")
        banner.save()
    elif oper == 'del':
        id = request.POST.get('id')
        Banner.objects.get(id=id).delete()
    return HttpResponse('ok')