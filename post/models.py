from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class PostManager(models.Manager):
	def published(self):
		return super().all().filter(draft=False)

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length = 500)
	content = models.TextField()
	image = models.ImageField(null=True, blank = True, width_field = 'image_width', height_field = 'image_height')
	image_height = models.IntegerField(default = 0)
	image_width = models.IntegerField(default = 0)
	slug = models.SlugField(unique=True)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)
	updated = models.DateTimeField(auto_now = True, auto_now_add = False)
	draft = models.BooleanField(default=False)

	objects = PostManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post:details', kwargs = {'slug':self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	class Meta:
		ordering = ['-updated','-created']

def profile_picture(instance, filename):
	return 'profile_pic/%s/%s' % (instance.user.username, filename)

def cover_picture(instance, filename):
	return 'cover_pic/%s/%s' % (instance.user.username, filename)

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_pic = models.ImageField(upload_to=profile_picture, default= 'profile_pic/profile_pic.png')
	cover_pic = models.ImageField(upload_to=cover_picture, default= '1.jpg')
	website = models.URLField(null=True, blank = True)
	date_of_birth = models.DateField(null=True, blank=True)
	bio = models.TextField(null=True, blank=True)
	follows = models.ManyToManyField('self', blank=True, related_name='followed_by', symmetrical=False)

	def __str__(self):
		return self.user.username
