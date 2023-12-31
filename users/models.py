from django.db import models

from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    face = models.ImageField()
    check_face = models.ImageField(null=True, blank=True)
    