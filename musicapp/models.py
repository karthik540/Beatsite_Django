from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    songlist = models.CharField(max_length = 1000 , default = '' , blank = True)
    def __str__(self):
        return self.email
    
