from django.db import models
from django.urls import reverse

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length = 500)
	content = models.TextField()
	created = models.DateTimeField(auto_now = False, auto_now_add = True)
	updated = models.DateTimeField(auto_now = True, auto_now_add = False)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post:details', kwargs = {'pk':self.id})
