from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from users.views import LoginView, RegisterView, CheckFaceID, SuccessView, FailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/<int:pk>/', CheckFaceID.as_view(), name='home'),
    path('success/', SuccessView.as_view(), name='success'),
    path('fail/', FailView.as_view(), name='fail'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)