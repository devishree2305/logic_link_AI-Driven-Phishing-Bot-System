# myapp/models.py

from django.db import models

class UserData(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class testUserData(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
