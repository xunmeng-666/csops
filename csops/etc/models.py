# -*- coding:utf-8-*-
import datetime


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

def screens(admin_class,date):
    end_date = datefunc(date)
    obj_list = []
    obj = admin_class.model.objects.filter(start_time__gt=end_date).values('id','number','titel','start_time','pool__name','status','transfer','ops_people__username','timeout')
    for lists in obj:
        if type(lists['start_time']) is datetime.datetime:
            lists['start_time']=str(lists['start_time'].strftime('%Y-%m-%d'))
        obj_list.append(lists)
    return obj_list
