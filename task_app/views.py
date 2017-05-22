from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template import loader,RequestContext
from django.views.decorators.csrf import csrf_exempt
from task_app.models import *
import json
import time
import re


default_msg = 'Method Not Allowed' 

# INDEX VIEW
def v_index(request):
	template = loader.get_template('index.html')
	return HttpResponse(template.render())


# GET TASKS VIEW
def v_gettask(request):
	if  request.method == 'GET' and request.is_ajax():
		return get_tasks()
	else:
		return HttpResponse(json.dumps({'status':False,'message':default_msg},indent=4))

# GET COMMENT AS PER TASK VIEW
def v_getcomment(request,c_id):
	if  request.method == 'GET' and request.is_ajax():
		return get_comment(c_id)
	else:
		return HttpResponse(json.dumps({'status':False,'message':default_msg},indent=4))

# UPDATE TASK VIEW
@csrf_exempt
def v_updatetask(request):
	if  request.method == 'POST' and request.is_ajax():
	 	return task_status(request.GET.get('t_id'),request.GET.get('t_status'))
	else:
		return HttpResponse(json.dumps({'status':False,'message':default_msg},indent=4))


# CREATE TASK VIEW
@csrf_exempt
def v_createtask(request):
 	if  request.method == 'POST' and request.is_ajax():
	 	return create_task(request.GET.get('new_task'))
	else:
		return HttpResponse(json.dumps({'status':False,'message':default_msg},indent=4))


# CREATE COMMENT VIEW
@csrf_exempt
def v_createcomment(request):
 	if  request.method == 'POST' and request.is_ajax():
	 	return create_comment(request.GET.get('c_id'),request.GET.get('new_comment'))
	else:
		return HttpResponse(json.dumps({'status':False,'message':default_msg},indent=4))
