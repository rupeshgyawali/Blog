from django.db import models
from django.contrib.auth.models import User


# Create your models here.
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
