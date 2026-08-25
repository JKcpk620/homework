from django.db import models
from .choices import f_or_b_choices, cooking_type_choices, beverage_choices

# Create your models here.
class F_and_b(models.Model):
    title = models.CharField(max_length=200)
    discription = models.TextField(blank=True)
    F_or_b = models.CharField(max_length=50, choices = f_or_b_choices.items(), default='')
    cooking_type = models.CharField(max_length=50, choices = cooking_type_choices.items(), default='', blank=True)
    beverage_type = models.CharField(max_length=50, choices = beverage_choices.items(), default='', blank=True)
    veggie = models.BooleanField(default=False)
    halal = models.BooleanField(default=False)
    spicy = models.BooleanField(default=False)
    allegy_ingredient = models.CharField(max_length=200, blank=True)
    price = models.FloatField(default=0.00)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-list_date']
        indexes = [models.Index(fields=['list_date'])]
    
    def __str__(self):
        return self.title