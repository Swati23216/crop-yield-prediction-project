from django.db import models
from django.contrib.auth.models import User

class Crop(models.Model):
    name = models.CharField(max_length=100)
    nitrogen = models.FloatField()
    phosphorous = models.FloatField()
    potash = models.FloatField()
    rainfall = models.FloatField()
    temperature = models.FloatField()
    soil_ph = models.FloatField()
    image = models.ImageField(upload_to='crops/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class UserPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nitrogen = models.FloatField()
    phosphorous = models.FloatField()
    potash = models.FloatField()
    rainfall = models.FloatField()
    temperature = models.FloatField()
    soil_ph = models.FloatField()
    predicted_crop = models.CharField(max_length=100)
    date_predicted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s prediction - {self.predicted_crop}"