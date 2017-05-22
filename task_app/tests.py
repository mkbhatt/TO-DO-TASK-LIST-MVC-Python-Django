from django.test import TestCase
from task_app.models import *

class TaskTestCase(TestCase):
	
	def setUp(self):

		task_a = Task.objects.create(task_title="Task A")
		task_b = Task.objects.create(task_title="Task B",Status=1)

		task_aid = task_a.id
		task_bid = task_b.id

		task_a = Task.objects.get(pk=task_aid)
		task_a.comment_set.create(task_comment='Task A Comment')

		task_b = Task.objects.get(pk=task_bid)
		task_b.comment_set.create(task_comment='Task B Comment')

	
	def test_task_get(self):
		
		task_a = Task.objects.get(task_title="Task A")
		task_b = Task.objects.get(task_title="Task B")

		self.assertEqual(task_a.task_title, 'Task A')
		self.assertEqual(task_b.task_title, 'Task B')
		self.assertEqual(task_a.Status,0)
		self.assertEqual(task_b.Status,1)
		get_tasks()


	
	def test_comment_get(self):
		
		task_a_comment = Comment.objects.get(task_comment='Task A Comment')
		task_b_comment = Comment.objects.get(task_comment='Task B Comment')

		self.assertEqual(task_a_comment.task_comment, 'Task A Comment')
		self.assertEqual(task_b_comment.task_comment, 'Task B Comment')