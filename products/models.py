from django.db import models
from django_countries.fields import CountryField

# Create your models here.
class Products(models.Model):
    title = models.CharField(max_length=200)
    discription = models.TextField(blank=True)
    origin = CountryField(blank_label="(Select Country)")
    package_size = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    price = models.FloatField(default=0.00)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        ordering = ['-list_date']
        indexes = [models.Index(fields=['list_date'])]
        
    def __str__(self):
        return self.title