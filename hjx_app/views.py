import random
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
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