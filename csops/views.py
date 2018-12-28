from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . import forms
from .admin_base import site
from .etc.models import screens
import json
# Create your views here.

@login_required
def index(request):
    return render(request,'index.html')

def account_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return  redirect(request.GET.get('next') or '/')
    return render(request, 'login.html', locals())

def account_logout(request,**kwargs):
    request.session.clear()
    logout(request)
    return redirect('/accounts/login/')


def admin_func(model_name):
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        return admin_class


def get_filter_objs(request, admin_class):
    """返回filter的结果queryset"""

    filter_condtions = {}
    for k, v in request.GET.items():
        if k in ['_page', '_q', '_o']:
            continue
        if v:  # valid condtion
            filter_condtions[k] = v

    queryset = admin_class.model.objects.filter(**filter_condtions)
    return queryset, filter_condtions

def get_search_objs(request, querysets, admin_class):
    """
    1.拿到_q的值
    2.拼接Q查询条件
    3.调用filter(Q条件)查询
    4. 返回查询结果
    :param request:
    :param querysets:
    :param admin_class:
    :return:
    """
    q_val = request.GET.get('_q')  # None
    if q_val:
        q_obj = Q()
        q_obj.connector = "OR"
        for search_field in admin_class.search_fields:  # 2
            q_obj.children.append(("%s__contains" % search_field, q_val))
        search_results = querysets.filter(q_obj)  # 3
    else:
        search_results = querysets

    return search_results, q_val

def get_orderby_objs(request, querysets):
    """
    排序
    1.获取_o的值
    2.调用order_by(_o的值)
    3.处理正负号，来确定下次的排序的顺序
    4.返回
    :param request:
    :param querysets:
    :return:
    """
    orderby_key = request.GET.get('_o')  # -id
    last_orderby_key = orderby_key or ''
    if orderby_key:
        order_column = orderby_key.strip('-')
        order_results = querysets.order_by(orderby_key)
        print('ordd',orderby_key)
        if orderby_key.startswith('-'):
            new_order_key = orderby_key.strip('-')
        else:
            new_order_key = "-%s" % orderby_key

        return order_results, new_order_key, order_column, last_orderby_key
    else:
        return querysets, None, None, last_orderby_key



@login_required
def list(request,model_name):
    admin_class = admin_func(model_name)
    querysets, filter_conditions = get_filter_objs(request, admin_class)
    querysets, q_val = get_search_objs(request, querysets, admin_class)
    querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
    paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
    page = request.GET.get('_page')
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        querysets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        querysets = paginator.page(paginator.num_pages)
    return render(request,'globle_form/list_forms.html',locals())

@login_required
def add(request,model_name):
    admin_class = admin_func(model_name)
    form = forms.create_dynamic_modelform(admin_class.model)
    if request.method == 'POST':
        form_obj = form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("apps/%s/list" %model_name)

    else:
        form_obj = form()
    return render(request,'globle_form/add_forms.html',locals())

@login_required
def change(request,model_name):
    id = request.GET.get('idAll')
    admin_class = admin_func(model_name)
    objects = admin_class.model.objects.get(id=id)
    form = forms.create_dynamic_modelform(admin_class.model)
    if request.method == "GET":
        form_obj = form(instance=objects)
    elif request.method == "POST":
        form_obj = form(instance=objects,data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/apps/%s/list" %model_name)
    return render(request,'globle_form/change_forms.html',locals())

@login_required
def detail(request,model_name,number):
    admin_class = admin_func(model_name)
    objects = admin_class.model.objects.get(number=number)
    form = forms.create_dynamic_modelform(admin_class.model)
    form_obj = form(instance=objects)
    return render(request,'globle_form/detail_forms.html',locals())

@login_required
@csrf_exempt
def delete(request,model_name):
    admin_class = admin_func(model_name)
    obj_id = request.GET.get('idAll')
    if ',' in obj_id:
        for ids in obj_id.split(','):
            obj = admin_class.model.objects.get(id=ids.strip())
            obj.delete()
        return HttpResponse({"status": "删除成功"})

    else:
        admin_class.model.objects.get(id=obj_id).delete()
    return HttpResponse({"status":"删除成功"})

@login_required
@csrf_exempt
def screen(request,model_name):
    admin_class = admin_func(model_name)
    date = request.GET.get('screenDate')
    datefunc = screens(admin_class,date)
    return HttpResponse(json.dumps({'data':datefunc}))

