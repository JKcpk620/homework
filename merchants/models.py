from django.db import models

# Create your models here.
class Merchants(models.Model):
    title = models.CharField(max_length=200)
    district = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    cuisine_choices = models.CharField(max_length=50)
    acommodate = models.IntegerField(blank=True)
    has_wifi = models.BooleanField(default=True)
    has_delivery = models.BooleanField(default=True)
    average_spend = models.IntegerField(blank=True)
    promo_badge_text = models.CharField(max_length=100, blank=True, null=True)
    accept_reservations = models.BooleanField(default=True)
    pre_order = models.BooleanField(default=True)
    catering_service = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=20, blank=True)
    has_Whatspp = models.BooleanField(default=True)
    opening_hours = models.TimeField(default=None)
    closing_hours = models.TimeField(default=None)
    rating = models.FloatField(default=0.0)
    description = models.TextField(blank=True)
    signature_dish = models.CharField(max_length=200, blank=True)
    sign_dish_photo1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    sign_dish_photo2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    sign_dish_photo3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-list_date']
        indexes = [models.Index(fields=['list_date'])]

    def __str__(self):
        return self.title