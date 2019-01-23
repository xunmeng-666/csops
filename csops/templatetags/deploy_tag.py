# -*- coding:utf-8-*-
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

@register.simple_tag
def build_project_name(admin_class):
    return admin_class.model._meta.model_name

@register.simple_tag
def build_project_verbose_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_filter_condtions_string(filter_conditions,q_val):
    condtion_str = ""
    for k,v in filter_conditions.items():
        condtion_str += "&%s=%s" %(k,v)
    if q_val:#拼接search 字段
        condtion_str += "&_q=%s" % q_val
    return condtion_str

@register.simple_tag
def generate_orderby_icon(new_order_key):
    if new_order_key.startswith('-'):
        icon_ele = """<i class="fa fa-angle-down" aria-hidden="true"></i>"""
    else:
        icon_ele = """<i class="fa fa-angle-up" aria-hidden="true"></i>"""
    return mark_safe(icon_ele)

@register.simple_tag
def get_abs_value(loop_num , curent_page_number):
    """返回当前页与循环loopnum的差的绝对值"""
    return abs(loop_num - curent_page_number)

@register.simple_tag
def build_filter_ele(filter_column,admin_class,filter_conditions):
    """
    1.拿到要过滤字段的对象field_obj
    2. 调用field_obj.get_choices()
    3. 生成select元素
    4.循环choices列表，生成option元素
    :param filter_column:
    :param model_class:
    :return:
    """

    field_obj = admin_class.model._meta.get_field(filter_column)
    select_ele = "<select class='form-control'  name=%s>"% filter_column
    filter_option = filter_conditions.get(filter_column) #1.None 代表没有对这个字段过滤，2.有值，选中的具体的option的val
    if filter_option:#代表此字段过滤了
        try:
            for choice in field_obj.get_choices():
                if filter_option == str(choice[0]):
                    selected = 'selected'
                else:
                    selected = ''
                option_ele = "<option value=%s  %s>%s</option>" % (choice[0],selected,choice[1])
                select_ele += option_ele
        except AttributeError:
            if filter_column == 'timeout':
                select_ele = "<input type='checkbox' name='timeout' value='1'>"
            elif filter_column == 'vip':
                select_ele = "<input type='checkbox' name='vip' value='1'>"
            return mark_safe(select_ele)

    else:
        try:
            for choice in field_obj.get_choices():
                option_ele = "<option value=%s >%s</option>" % (choice[0],choice[1])
                select_ele += option_ele
        except AttributeError:
            if filter_column == 'timeout':
                select_ele = "<input type='checkbox' name='timeout' id='screen_timeout',value='0'>"
            elif filter_column == 'vip':
                select_ele = "<input type='checkbox' name='vip' id='screen_vip',value='0'>"
            return mark_safe(select_ele)

    select_ele += "</select>"
    return mark_safe(select_ele)

@register.simple_tag
def get_readonly_field_val(field_name,obj_instance):
    """
    1.根据obj_instance反射出field_name 的值
    :param field_name:
    :param obj_instance:
    :return:
    """
    field_type =  obj_instance._meta.get_field(field_name).get_internal_type()
    if field_type == "ManyToManyField":
        m2m_obj = getattr(obj_instance,field_name)
        return ",".join([ i.__str__() for i in m2m_obj.all()])
    return getattr(obj_instance,field_name)

@register.simple_tag
def get_selected_m2m_objects(form_obj,field_name):
    """
    1.根据field_name反射出form_obj.instance里的字段对象
    2. 拿到字段对象关联的所有数据
    :param form_obj:
    :param field:
    :return:
    """

    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance, field_name)
        return field_obj.all()
    else:
        return []

@register.simple_tag
def get_m2m_objects(admin_class,field_name,selected_objs):
    """
    1.根据field_name从admin_class.model反射出字段对象
    2.拿到关联表的所有数据
    3.返回数据
    :param admin_class:
    :param field_name:
    :return:
    """

    field_obj = getattr(admin_class.model,field_name)
    all_objects = field_obj.rel.to.objects.all()
    return set(all_objects) - set(selected_objs)

@register.simple_tag
def build_job_detail(admin_class,row):
    ele = ""
    ele_tr = "<tr>"
    ele_td = "<td>"+row.label+"</td>"
    if type(row.value()) is int:
        for choice in admin_class.model._meta.get_field(row.name).get_choices():
            if choice[0] == row.value():
                ele_td+= "<td>" + choice[1] +"</td>"
    else:
        if row.value() is None:
            ele_td += "<td></td>"
        elif row.value() is False:
            ele_td += "<td>否</td>"
        elif row.value() is True:
            ele_td += "<td style='color: red'>是</td>"
        else:
            ele_td += "<td>"+str(row.value())+"</td>"
        ele_tr += ele_td +"</tr>"
    ele += ele_tr
    return mark_safe(ele)

@register.simple_tag
def build_job_image(admin_class,number):
    ele = ""
    imagepath = admin_class.model.objects.get(number=number).image.values("imagepath")
    for path in imagepath:
        ele_li = "<li class='span2' style='width: 200px;'>"
        ele_li += "<a><img  style='wigth: 100%;height: 100%' alt='' src="+path.get('imagepath')+"></a>"
        ele_li += "<div class='actions'>"
        ele_li += "<a class='lightbox_trigger' href=%s>" %path.get('imagepath')
        ele_li += "<i class='icon-search'></i>"
        ele_li += "</a>"
        ele_li += "</div>"
        ele_li += "</li>"
        ele += ele_li
    return mark_safe(ele)


@register.simple_tag
def build_start_date(admin_class):
    datelist = []
    for date in admin_class.model.objects.values("start_time"):
        if date['start_time'].strftime('%Y-%m-%d') not in datelist:
            datelist.append(date['start_time'].strftime('%Y-%m-%d'))
    ele_option = ""
    for date in datelist:
        ele_option += "<option value='%s'>%s</option>"%(date,date)
    return mark_safe(ele_option)