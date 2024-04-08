from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.





class CustomUser(AbstractUser):
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    groups = models.ManyToManyField('auth.Group', related_name='myapp_users', blank=True, verbose_name='groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='myapp_users', blank=True, verbose_name='user permissions')



#para cargar las fotos 
class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')  

    def __str__(self):
        return self.title


