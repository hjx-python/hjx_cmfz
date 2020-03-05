from django.db import models

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=32)
    status = models.NullBooleanField()
    create_time = models.DateTimeField()
    pic = models.ImageField(upload_to="pic")
    class Meta:
        db_table = 'banner'