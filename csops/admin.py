from django.contrib import admin
from csops import models
from csops.admin_base import site,BaseAdmin
# Register your models here.


class JobAdmin(BaseAdmin):
    list_display = ("number","title","pool__name","problem_type","status","ops_people","dev_people","problem","resolvents","resolvent","transfer"
                    "timeout","timeout_cause","resolventplan","nextresolvent","testing_job","dev_job","estimate_time",
                    "refailure","start_time","resolve_time")

    list_filter = ["工单编号", "问题标题", "开始时间", "资源池", "状态", "工单移交","运维处理人"]
    list_search_filter = ("status","resolvents","problem_type","timeout",)
    sort_filter = ["number","titel","start_time","pool",'status','transfer','ops_people',"timeout"]
    list_per_page = 15
    search_fields = ["number","titel","pool__name","status"]

class PoolAdmin(BaseAdmin):
    list_display = ("name")
    list_filter = ['资源池']
    list_per_page = 3
    search_fields = ["name" ]
    sort_filter = ["name" ]

class DepartmentAdmin(BaseAdmin):
    list_display = ("name")
    list_filter = ['资源池']
    list_per_page = 3
    search_fields = ["name"]
    sort_filter = ["name"]

site.register(models.Job,JobAdmin)
site.register(models.Pool,PoolAdmin)
site.register(models.Department,DepartmentAdmin)