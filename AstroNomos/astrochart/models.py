from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class React(models.Model):
    firebase_uid = models.CharField(max_length=255, null=True)
    birth_date = models.DateField()
    birth_time = models.TimeField()
    birth_location = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"React Object: {self.firebase_uid} - {self.name},  {self.birth_date}, {self.birth_time}, {self.birth_location}"
"----------------------------------------------------------------------------------------------------------------------"

class TransitChart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Utilise une clé étrangère vers UserProfile
    birth_date = models.DateField()
    birth_time = models.TimeField()
    birth_location = models.CharField(max_length=255)
    transit_start_date = models.DateField()
    transit_end_date = models.DateField()
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Transit Chart for {self.name} from {self.transit_start_date} to {self.transit_end_date}"

    def __str__(self):
        return f"Transit Chart for {self.name} from {self.transit_start_date} to {self.transit_end_date}"
class UserProfileManager(BaseUserManager):
    def create_user(self, firebase_uid, name=None, password=None):
        if not firebase_uid:
            raise ValueError('Users must have a Firebase UID')

        user = self.model(firebase_uid=firebase_uid, name=name)
        user.set_password(password)  # Vous pouvez ajuster selon vos besoins
        user.save(using=self._db)
        return user

    def create_superuser(self, firebase_uid, name=None, password=None):
        user = self.create_user(firebase_uid=firebase_uid, name=name, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
    firebase_uid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'firebase_uid'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"UserProfile: {self.name} ({self.firebase_uid})"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin




