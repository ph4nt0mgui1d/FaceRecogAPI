from django.db import models

class FacRecogGroup(models.Model):   
    group_image_path = models.ImageField(upload_to='GroupImages/')

class FacRecogTarget(models.Model):
    target_image_path = models.ImageField(upload_to='TargetImage/')
  
    