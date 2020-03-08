from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    sex = models.CharField(max_length=5)
    create_time = models.DateField()
    province = models.CharField(max_length=32)
    addr = models.CharField(max_length=100)
    rank = models.CharField(max_length=32)
    status = models.IntegerField()
    pic = models.ImageField(upload_to='user_pic')
    sinature = models.CharField(max_length=32)
    class Meta:
        db_table = 'user'