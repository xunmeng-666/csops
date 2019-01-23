from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin,User
)
# Create your models here.

class Pool(models.Model):
    name = models.CharField(verbose_name='名称',max_length=32,unique=True)

    class Meta:
        verbose_name = '资源池'
        verbose_name_plural = verbose_name

    def __str__(self):
        return  "%s" %self.name

class Department(models.Model):
    name = models.CharField(verbose_name='名称',max_length=64,unique=True)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Job(models.Model):

    choice_resolvent = (
        (0,'临时解决'),
        (1,'最终解决'),
    )
    cs_status = (
        (0,'未进行'),
        (1,'进行中'),
        (2,'已完成'),
    )


    number = models.CharField(verbose_name='工单编号',max_length=128,unique=True)
    titel = models.CharField(verbose_name='工单标题',max_length=64)
    account = models.CharField(verbose_name='客户账号',max_length=64,blank=True,null=True,)
    start_time = models.DateTimeField(verbose_name='提交时间', auto_now_add=False)
    pool = models.ForeignKey(Pool,verbose_name='资源池',on_delete=models.CASCADE,related_name='job')
    problem_type = models.ForeignKey(Department,verbose_name='问题分类',related_name='job',on_delete=models.CASCADE)
    ops_people = models.ForeignKey(User,verbose_name='运维处理人',related_name='job')
    dev_people = models.CharField(verbose_name='研发处理人',max_length=32,blank=True,null=True)
    vip = models.BooleanField(verbose_name='VIP',default=False,blank=True)
    problem = models.CharField(verbose_name='分析原因', max_length=2000, blank=True, null=True)
    resolvents = models.SmallIntegerField(verbose_name='解决方案',choices=choice_resolvent,default=0)
    resolvent = models.CharField(verbose_name='解决方法',max_length=2000,blank=True,null=True)
    status = models.SmallIntegerField(verbose_name='状态',choices=cs_status,default=1)
    transfer = models.CharField(verbose_name='工单移交',max_length=64,blank=True,null=True)
    timeout = models.BooleanField(verbose_name='超时',)
    timeout_cause = models.CharField(verbose_name='超时原因', max_length=128, blank=True, null=True)
    resolventplan = models.CharField(verbose_name='处理计划', max_length=2000, blank=True, null=True)
    nextresolvent = models.CharField(verbose_name='进一步解决方案', max_length=2000, blank=True, null=True)
    testing_job = models.CharField(verbose_name='测试对接任务', max_length=2000, blank=True, null=True)
    dev_job = models.CharField(verbose_name='开发对接任务', max_length=2000, blank=True, null=True)
    estimate_time = models.DateTimeField(verbose_name='预计解决时间', auto_now_add=False, blank=True, null=True)
    refailure = models.BooleanField(verbose_name='复发故障')
    resolve_time = models.DateTimeField(verbose_name='最终解决时间', auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name = '工单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" %(self.number)

class Image(models.Model):
    imagepath = models.CharField(verbose_name='路径',max_length=128,blank=True,null=True)
    job = models.ForeignKey(Job,verbose_name='工单',related_name='image',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" %self.imagepath