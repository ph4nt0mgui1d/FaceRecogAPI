from django.http import JsonResponse
from .models import FacRecogGroup, FacRecogTarget
from .serializers import FacRecogGroupSerializer, FacRecogTargetSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from django.shortcuts import render

import cv2
import face_recognition as fr
import numpy as np
import json

class group(APIView):
    def get(self,request):
        qs = FacRecogGroup.objects.all()
        serializer = FacRecogGroupSerializer(qs, many = True)
        result = []
        # print(type(result))
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['group_image_path'])
            # result.append(serializer.data[i])

        return JsonResponse(result, safe=False)
        # return result
  
    def post(self,request):
        try:
            serializer = FacRecogGroupSerializer(data = request.data)
            if(serializer.is_valid()):
                serializer.save()
                # print(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
                # return "test"
        except json.JSONDecodeError:
            return JsonResponse({'message':'error'})
        



class target(APIView):
    def get(self,request):
        qs = FacRecogTarget.objects.all()
        serializer = FacRecogTargetSerializer(qs, many = True)
        result = serializer.data[0]['target_image_path']
        # return JsonResponse(result, safe=False)
        return result
    
    def post(self,request):
        try:
            FacRecogTarget.objects.all().delete()
            serializer = FacRecogTargetSerializer(data = request.data)
            if(serializer.is_valid()):
                serializer.save()
                print('success')

                # getting data of group images
                group_images = group()
                group_images = group_images.get(self)
                group_images = json.loads(group_images.content)
                # print(group_images)
                # getting target image data
                target_image = self.get(self)
                # print(target_image)
                # Face recog script
                group_photos = group_images

                target_photo = target_image
                target_photo = cv2.imread('/Users/ph4nt0mgui1d/Desktop/Django api' + target_photo)
                
                target_face_encoding = fr.face_encodings(target_photo)

                matching_filenames = []

                threshold = 0.6
                
                for group_photo_filename in group_photos:
                    group_photo = cv2.imread('/Users/ph4nt0mgui1d/Desktop/Django api' + group_photo_filename)
                    
                    group_face_locations = fr.face_locations(group_photo)
                    group_face_encodings = fr.face_encodings(group_photo, group_face_locations)
                    
                    matching_face_indices = []
                    
                    for i, face_encoding in enumerate(group_face_encodings):
                        distance = np.linalg.norm(np.array(face_encoding) - np.array(target_face_encoding))
                        
                        if distance < threshold:
                            matching_face_indices.append(i)
                    
                    if matching_face_indices:
                        matching_filenames.append(group_photo_filename)
                    
                    for i in matching_face_indices:
                        top, right, bottom, left = group_face_locations[i]
                        cv2.rectangle(group_photo, (left, top), (right, bottom), (0, 255, 0), 2)

                    # print(matching_filenames)

                    json_result = json.dumps(matching_filenames)
                    # print(json_result)
                return JsonResponse(json_result, safe=False)
                # return JsonResponse(serializer.data, safe=False)

            else:
                print("eroororor")
                return JsonResponse({'message':'Invalid image'})
        
        except json.JSONDecodeError:
            return JsonResponse({'message':'error'})

def temp(request):
    return render(request, "facial_api/temp.html")