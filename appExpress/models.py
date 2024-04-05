from django.db import models
from django.db.models.base import ModelState
from django.db.models.deletion import CASCADE
from django.http import JsonResponse
# Create your models here.
class users(models.Model):
    id_admin=models.CharField(max_length=20,verbose_name="管理员id",default='admin')
    pwd_admin=models.CharField(max_length=20,verbose_name="管理员密码",default='123456')
    Time=models.DateTimeField(verbose_name="time",default="false")

class Message(models.Model):
    Time=models.DateTimeField(verbose_name="time",default="false")
    Eui=models.CharField(max_length=100,verbose_name="eui",default="")
    Name=models.CharField(max_length=100,verbose_name="name",default="")
    Client=models.CharField(max_length=100,verbose_name="client",default="")
    Gateway=models.CharField(max_length=100,verbose_name='gateway',default="")
    Arrtime=models.DateTimeField(max_length=100,verbose_name='arrtime',default="false")
    Text=models.TextField(max_length=1000,verbose_name="text",default='')
    latitude=models.DecimalField(max_digits=38,decimal_places=35,verbose_name="latitude",default=0)
    longitude=models.DecimalField(max_digits=38,decimal_places=35,verbose_name="longitude",default=0)

class Gateway(models.Model):
    G_id=models.CharField(max_length=100,verbose_name="g_id",default="")
    latitude = models.DecimalField(max_digits=38, decimal_places=35, verbose_name="latitude", default=0)
    longitude = models.DecimalField(max_digits=38, decimal_places=35, verbose_name="longitude",default=0)
    Time=models.DateTimeField(verbose_name="time",default="false")

class Client(models.Model):
    C_id=models.CharField(max_length=100,verbose_name="c_id",default="")
    C_type=models.CharField(max_length=10,verbose_name='c_type',default='D') #Distress 求救人员  Rescuer 救援人员 
    C_situation = models.CharField(max_length=100,verbose_name='c_situation',default='help')
    C_latitude=models.DecimalField(max_digits=38,decimal_places=35,verbose_name="c_latitude",default=0)
    C_longitude=models.DecimalField(max_digits=38,decimal_places=35,verbose_name="c_longitude",default=0)
    C_lasttime=models.DateTimeField(max_length=100,verbose_name='c_lasttime',default="false")