"""task_list_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib import admin
from task_app import views
from task_app import models

urlpatterns = [

    # INDEX ROUTES
    url(r'^$',views.v_index,name='v_index'),
    
    # GET ROUTES
    url(r'^get-task$',views.v_gettask,name='v_gettask'),
    url(r'^get-comment/(?P<c_id>[0-9]+)/$',views.v_getcomment,name='v_getcomment'),

    #POST ROUTES AJAX
    url(r'^create-task$',views.v_createtask,name='v_createtask'),
    url(r'^create-comment$',views.v_createcomment,name='v_createcomment'),
    url(r'^update-task$',views.v_updatetask,name='v_updatetask'),

]
