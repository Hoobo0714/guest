from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.

def index(request):
    return render(request,'index.html')

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user) #登录
            request.session['user'] = username #记录session到浏览器
            response = HttpResponseRedirect('/event_manage/')
            #response.set_cookie('user',username,3600)
            return response

        else:
            return render(request,'index.html',{'error':'username or password error!!'})

#发布会管理
@login_required
def event_manage(request):
    #username = request.COOKIES.get('user','')
    event_list = Event.objects.all()
    username = request.session.get('user','')
    return render(request,'event_manage.html',{'user':username,'events':event_list})

#发布会搜索
@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,'event_manage.html',{'user':username,'events':event_list})

#嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user','')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts =paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer,deliver first page
        contacts = paginator.page(1)
    except EmptyPage:
        #if page is out of range,deliver last page of results
        contacts = paginator.page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,"guests":contacts})

#嘉宾搜索
@login_required
def search_realname(request):
    username = request.session.get('user','')
    search_realname = request.GET.get('name','')
    guest_list =Guest.objects.filter(realname__contains=search_realname)
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contracts = paginator.page(page)
    except PageNotAnInteger:
        contracts = paginator.page(1)
    except EmptyPage:
        contracts = paginator.page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,'guests':contracts})

#签到页面
@login_required
def sign_index(request,event_id):
    event = get_object_or_404(Event,id = event_id)
    return render(request,'sign_index.html',{'event':event})

#签到动作
@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    phone = request.POST.get('phone','')

    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error'})

    result =Guest.objects.filter(phone = phone,event_id=event_id)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'event id or phone error.'})

    result = Guest.objects.get(phone=phone,event_id=event_id)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':'user has sign in'})

    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign = '1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success','guest':result})

#退出登录
@login_required
def logout(request):
    auth.logout(request)   #退出登录
    response = HttpResponseRedirect('/index/')
    return response
