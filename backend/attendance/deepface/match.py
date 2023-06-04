from users.models import *
from deepface import DeepFace
import cv2
import base64
from PIL import Image
import io
from tempfile import NamedTemporaryFile
import os



def save_image_to_tempfile(image_data):
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(image_data.read())
        temp_file_path = temp_file.name
        print(temp_file_path)
    return temp_file_path

def delete_tempfile(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)





def face_match(image,user):
    User_images = UserImage.objects.filter(user=user)
    print("User_images",User_images)
    u_i=save_image_to_tempfile(image)
    result=False
    flag=[]
    for i in User_images:
        refrence_image=i.image.path
        result = DeepFace.verify(refrence_image, u_i, enforce_detection=False)
        flag.append(result["verified"])
    print(flag)   
    r_i=delete_tempfile(u_i)     
    if any(flag):
        print("At least one value is True")
        return True
    else:
        return False