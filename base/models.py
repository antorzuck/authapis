from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	gender = models.CharField(max_length=20, null=True, blank=True)
	profile_pc = models.FileField(null=True, blank=True, upload_to='dp')
	address = models.CharField(max_length=500, null=True, blank=True)
	mobile = models.CharField(max_length=100, null=True, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	forgot_code = models.CharField(max_length=10, null=True, blank=True)
	
	

	
	
