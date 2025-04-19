from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    address = models.CharField(max_length = 255, blank = True, null = True)
    phone_number = models.CharField(max_length = 20, blank = True, null = True)
    profile_photo = models.ImageField(
        upload_to = 'profile_photos/',
        blank = True,
        null = True
    )
    def __str__(self):
        return self.user.username


