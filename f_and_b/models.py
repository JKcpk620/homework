from django.db import models

# Create your models here.
class F_and_b(models.Model):
    title = models.CharField(max_length=200)
    discription = models.TextField(blank=True)
    veggie = models.BooleanField(default=False)
    spicy = models.BooleanField(default=False)
    allegy_ingredient = models.CharField(max_length=200)
    price = models.FloatField(default=0.00)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-list_date']
        indexes = [models.Index(fields=['list_date'])]
    
    def __str__(self):
        return self.title