from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core import serializers
from django.db import models
from django.db import connection
import json
import re


##################################################################
# DJANGO MODELS CREATE

class Task(models.Model):
	task_title = models.CharField(max_length=20,unique=True)
	Status = models.BooleanField(default=0)


class Comment(models.Model):
	###DB :: Don't Depend On Django's Auto Create Feature, 
	###Change on_update, on_delete To Cascade Manually In DB If Required

	task = models.ForeignKey(Task)
	task_comment = models.CharField(max_length=500)
	task_timestamp = models.DateTimeField(auto_now_add=True)

# END MODELS
#################################################################



# Create Task
def create_task(title):
	try:
		if not re.match(r'^[A-Za-z ]+$', str(title)):
			raise Exception('Validation Failure : Only Alphabets Allowed !')
		obj = Task(task_title=str(title))
		obj.save()
		data = json.dumps({'Status':'Success','id':int(obj.id)},indent=4)
		return HttpResponse(data,content_type="application/json")
	except Exception,e:
		data = json.dumps({'Status':'Fail','Message':str(e)},indent=4)
		return HttpResponse(data,content_type="application/json")



# Create Comment
def create_comment(c_id,comment):
	try:
		if not re.match(r'^[A-Za-z 0-9]+$', str(comment)):
			raise Exception('Validation Failure : Only Alphabets/Digits Allowed !')
		obj = Task.objects.get(pk=int(c_id))
		obj.comment_set.create(task_comment=str(comment))
		temp = obj.comment_set.filter(task_comment=str(comment)).get()
		t = str(temp.task_timestamp)
		data = json.dumps({'Status':'Success','id':int(obj.id),'time_stamp':t},indent=4)
		return HttpResponse(data,content_type="application/json")
	except Exception,e:
		data = json.dumps({'Status':'Fail','Message':str(e)},indent=4)
		return HttpResponse(data,content_type="application/json")



# Get All Task
def get_tasks():
	try:
		obj =  Task.objects.all().order_by('-id')
		# SERIALIZER TO CONVERT DATA TO OTHER FORMAT XML, JSON .... 
		serialize_obj = serializers.serialize('json',obj)
		data = json.dumps({'data':json.loads(serialize_obj)},indent=4)
		return HttpResponse(data,content_type="application/json")
	except Exception,e:
		data = json.dumps({'Status':'Fail','Message':str(e)},indent=4)
		return HttpResponse(data,content_type="application/json")



# Get Comment By Task ID
def get_comment(t_id):
	try:
		if not re.match(r'^[0-9]+$',t_id):
			raise Exception('Failure : API Received Anomaly Request!')
		obj = Comment.objects.filter(task_id=t_id)
		# SERIALIZER TO CONVERT DATA TO OTHER FORMAT XML, JSON .... 
		serialize_obj = serializers.serialize('json',obj)
		data = json.dumps({'data':json.loads(serialize_obj)},indent=4)
		return HttpResponse(data,content_type="application/json")
	except Exception,e:
		data = json.dumps({'Status':'Fail','Message':str(e)},indent=4)
		return HttpResponse(data,content_type="application/json")



# Update Task Status
def task_status(t_id,t_status):
	try:
		if not re.match(r'^[0-9]+$',t_status):
			raise Exception('Failure : API Received Anomaly Request!')
		obj = Task.objects.get(pk=t_id)
		obj.Status = int(t_status)
		obj.save()
		data = json.dumps({'Status':'Success'},indent=4)
		return HttpResponse(data,content_type="application/json")
	except Exception,e:
		data = json.dumps({'Status':'Fail','Message':str(e)},indent=4)
		return HttpResponse(data,content_type="application/json")