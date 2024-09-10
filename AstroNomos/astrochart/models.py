from django.db import models
class React(models.Model):
    firebase_uid = models.CharField(max_length=255, unique=True , null=True)
    birth_date = models.DateField()
    birth_time = models.TimeField()
    birth_location = models.CharField(max_length=255)


    def __str__(self):
        return f"React Object: {self.firebase_uid} - {self.birth_date}, {self.birth_time}, {self.birth_location}"