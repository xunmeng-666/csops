"""gongdan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(\w+)/list/', views.list,name='csops-list'),
    url(r'^(\w+)/add/', views.add,name='csops-add'),
    url(r'^(\w+)/change/', views.change,name='csops-change'),
    url(r'^(\w+)/delete/', views.delete,name='csops-delete'),
    url(r'^(\w+)/detail/(\w+)/', views.detail),
    url(r'^(\w+)/screen/', views.screen),
    url(r'^(\w+)/export/', views.export),
    url(r'^(\w+)/upimg/', views.upload),

]
