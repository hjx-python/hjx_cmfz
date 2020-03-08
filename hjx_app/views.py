import datetime
import random

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from hjx_app.models import User
from hjx_cmfz import settings
from gongju.yun import YunPian
from redis import Redis


red=Redis(host='127.0.0.1',port=6379)
# Create your views here.


def index(request):
    return render(request,'index.html')


def login(request):
    return render(request,'login.html',{'login':'login'})


def login_logic(request):
    u_code=request.GET.get('u_code')
    mobile=request.GET.get('mobile')
    if len(mobile)!=11:
        return HttpResponse('0')
    try:
        print(red.get(mobile+'code').decode())
        if u_code==red.get(mobile+'code').decode():
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    except:
        return HttpResponse('0')


@csrf_exempt
def code(request):
    mobile=request.POST.get('mobile')
    print(mobile)
    if len(mobile)!=11 or mobile[0]!='1':
        return HttpResponse('0')
    if red.get(mobile+'sj'):
        return HttpResponse('0')
    else:
        if red.get(mobile+'code'):
            code1=red.get(mobile+'code').decode()
        else:
            code1=''.join(random.sample('1234567890',6))
            red.setex(mobile + 'code', 60 * 5, code1)
        yunpian=YunPian(settings.APIKEY)
        print(code1)
        red.setex(mobile+'sj',60,1)
        yunpian.send_message(mobile,code1)
        return HttpResponse('1')


def show_userlist(request):
    '''
    用户信息列表,展示每页的用户信息
    :param request:
    :return:
    '''
    '''
    接收rows(每页展示的用户条数),page(第几页)
    构建分页器,得到分页对象
    根据数据格式,构造data
    返回
    '''
    def mydefault(u):
        if isinstance(u,User):
            return {"id":u.id,"username":u.username,"phone":u.phone,"sex":u.sex,"create_time":str(u.create_time),"province":u.province,"addr":u.addr,"rank":u.rank,"status":(lambda x:"激活" if x==1 else "冻结")(u.status),"pic":str(u.pic)}
    rows = request.GET.get('rows')
    page_num = request.GET.get("page")
    user_all = User.objects.all()
    pagtor = Paginator(user_all,rows)
    page = pagtor.page(page_num)
    data = {
        "page":page_num,
        "total":pagtor.num_pages,
        "records":pagtor.count,
        "rows":list(page)
    }
    return JsonResponse(data=data,safe=False,json_dumps_params={"default":mydefault})


@csrf_exempt
def update(request):
    '''
    管理员修改用户状态函数
    :param request:
    :return:
    '''
    '''
    获取用户id,status,根据id修改statis
    '''
    id = request.POST.get('id')
    status = request.POST.get('status')
    u = User.objects.get(id=id)
    u.status = int(status)
    u.save()
    return HttpResponse('ok')


@csrf_exempt
def bar_list(request):
    '''
    展示柱状图函数
    :param request:
    :return:
    '''
    '''
    计算出每个星期增加的人数,按顺序放入一个列表中,返回
    '''
    res = []
    now = datetime.datetime.now()
    for i in range(7,36,7):
        delta = datetime.timedelta(days=i)
        delta1 = datetime.timedelta(days=i-7)
        count = len(list(User.objects.filter(create_time__gt=(now - delta).strftime("%Y-%m-%d"), create_time__lte=(now - delta1).strftime("%Y-%m-%d"))))
        res.append(count)
    else:
        count = len(list(User.objects.filter(create_time__gt=(now - datetime.timedelta(days=35)).strftime("%Y-%m-%d"))))
        res.append(count)
    return JsonResponse(data={"result":res})


def map_data(request):
    '''
    展示地图函数
    :param request:
    :return:
    '''
    '''
    计算出每个省市的人数,按照格式{name:省市名,value:总人数},全部放到一个列表里返回
    '''
    data = []
    u = list(User.objects.values("province").annotate(Count('province')))
    print(u)
    for i in range(len(u)):
        # print('分组查询结果', u[i]["province"])
        # print('分组查询结果', u[i]["province__count"])
        data.append({"name":u[i]["province"],"value":u[i]["province__count"]})
    return JsonResponse(data={"result":data})