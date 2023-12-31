from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import os

from users.models import User


import face_recognition as fr # this is a library


# compare 2 faces
def face_match(known_image_path, unknown_image_path):
    known_image = fr.load_image_file(known_image_path)
    unknown_image = fr.load_image_file(unknown_image_path)
    known_encoding = fr.face_encodings(known_image)[0]
    unknown_encoding = fr.face_encodings(unknown_image)[0]
    return fr.compare_faces([known_encoding], unknown_encoding)[0]



class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        # image = request.POST.get('image_data')

        user = authenticate(request, username=username, password=password)

        if user is not None:
        
            return redirect('home', user.pk)


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        face = request.FILES.get('face')

        User.objects.create_user(
            username=username,
            password=password,
            face=face
        )

        return redirect('login')


class CheckFaceID(View):
    def get(self, request, pk):
        return render(request, 'face_id.html')
        
    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        img = request.FILES.get('image')
        user.check_face = img
        user.save()

        try:
            result = face_match(user.face, user.check_face)
        except:
            return redirect('fail')
        
        self.delete_image(str(user.check_face))
        print(user.check_face)
        user.check_face=None

        if result:
            login(request, user)
            return redirect("success")

        return redirect("fail")


    def delete_image(self, image):
        image_path = os.path.join(settings.MEDIA_ROOT, image)
        # Delete the file if it exists
        if os.path.isfile(image_path):
            os.remove(image_path)


class SuccessView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'success.html')


class FailView(View):
    def get(self, request):
        return render(request, 'fail.html')
