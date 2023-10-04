from rest_framework import serializers
from .models import FacRecogGroup, FacRecogTarget

class FacRecogGroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = FacRecogGroup
    fields = ['group_image_path']

class FacRecogTargetSerializer(serializers.ModelSerializer):
  class Meta:
    model = FacRecogTarget
    fields = ['target_image_path']