# -*- coding:utf-8-*-
import datetime
import xlwt
from config.config import *

def datefunc(date):
    now_date = datetime.datetime.now()
    if date == 'one':
        end_date = now_date + datetime.timedelta(days=-1)
    elif date == 'three':
        end_date = now_date + datetime.timedelta(days=-3)

    elif date == 'seven':
        end_date = now_date + datetime.timedelta(days=-7)
    elif date == 'fifteen':
        end_date = now_date + datetime.timedelta(days=-15)
    elif date == 'thirty':
        try:
            end_date = datetime.datetime(year=now_date.year,month=now_date.month-1,day=now_date.day)
        except ValueError:
            end_date = datetime.datetime(year=now_date.year - 1, month=12 + 1 - now_date.month, day=now_date.day)
    elif date == 'six_months':
        try:
            end_date = datetime.datetime(year=now_date.year, month=now_date.month - 6, day=now_date.day)
        except ValueError:
            end_date = datetime.datetime(year=now_date.year - 1, month=12 + 6 - now_date.month , day=now_date.day)
    elif date == 'year':
        end_date = datetime.datetime(year=now_date.year - 1,month=now_date.month,day=now_date.day)

    return end_date.strftime("%Y-%m-%d")

def now_date():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d_%H%M%S")

def screens(admin_class,date):
    end_date = datefunc(date)
    obj_list = []
    obj = admin_class.model.objects.filter(start_time__gt=end_date).values('id','number','titel','start_time','pool__name','status','transfer','ops_people__username','timeout')
    for lists in obj:
        if type(lists['start_time']) is datetime.datetime:
            lists['start_time']=str(lists['start_time'].strftime('%Y-%m-%d'))
        obj_list.append(lists)
    return obj_list


def exportfile(admin_class,startdate=None,enddate=None):
    '''导出Excel表'''
    ws = xlwt.Workbook(encoding='utf-8')
    w = ws.add_sheet(admin_class.model._meta.model_name, cell_overwrite_ok=True)
    objects = admin_class.model.objects.filter(start_time__gt=startdate.strip()).filter(start_time__lt=enddate.strip()) \
        .values("number","titel","account","vip","pool__name","status","start_time","resolve_time","ops_people__username",
                "dev_people","problem","resolvent","timeout","timeout_cause","nextresolvent")
    for index in range(0, len(admin_class.export_fields)):
        w.write(0, index, admin_class.export_fields[index])

    excel_row = 1
    for contents in objects:
        for index, content in enumerate(contents):
            if index == 0:
                dated = str(contents['start_time'].strftime('%Y/%m/%d'))
                w.write(excel_row, index, dated)
                w.write(excel_row, index+1, contents[content])
            else:
                if type(contents[content]) is datetime.datetime:
                    contents[content] = str(contents[content].strftime('%Y/%m/%d %H:%M:%S'))
                elif content == 'status':
                    contents[content] = admin_class.model.objects.filter(status=contents[content])[0].get_status_display()
                w.write(excel_row, index+1, contents[content])
        excel_row += 1
    startdate = datetime.datetime.strptime(startdate,'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d_%H:%M:%S')
    enddate = datetime.datetime.strptime(enddate,'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d_%H:%M:%S')
    _export_file = os.path.join(export_file,"工单系统_%s-%s.xls")%(startdate,enddate)

    if os.path.exists(_export_file):
        os.remove(_export_file)
    ws.save(_export_file)
    return _export_file

def download(admin_class):
    now_date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    ws = xlwt.Workbook(encoding='utf-8')
    w = ws.add_sheet(admin_class.model._meta.model_name, cell_overwrite_ok=True)
    objects = admin_class.model.objects.values("number", "titel", "account", "vip", "pool__name", "status", "start_time", "resolve_time",
                "ops_people__username",
                "dev_people", "problem", "resolvent", "timeout", "timeout_cause", "nextresolvent")
    for index in range(0, len(admin_class.export_fields)):
        w.write(0, index, admin_class.export_fields[index])

    excel_row = 1
    for contents in objects:
        for index, content in enumerate(contents):
            if index == 0:
                dated = str(contents['start_time'].strftime('%Y/%m/%d'))
                w.write(excel_row, index, dated)
                w.write(excel_row, index + 1, contents[content])
            else:
                if type(contents[content]) is datetime.datetime:
                    contents[content] = str(contents[content].strftime('%Y/%m/%d %H:%M:%S'))
                elif content == 'status':
                    contents[content] = admin_class.model.objects.filter(status=contents[content])[
                        0].get_status_display()
                w.write(excel_row, index + 1, contents[content])
        excel_row += 1

    _export_file = os.path.join(export_file, "工单系统_all_data-%s.xls") % (now_date)

    if os.path.exists(_export_file):
        os.remove(_export_file)
    ws.save(_export_file)
    return _export_file