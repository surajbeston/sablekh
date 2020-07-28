from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

User._meta.get_field('email')._unique = True


class Visitor(User):
    hid = models.CharField(max_length = 56, primary_key= True)

class Library(models.Model):
    hid = models.CharField(max_length = 56, primary_key= True)
    title = models.CharField(max_length = 300)
    user = models.ForeignKey(Visitor, on_delete = models.CASCADE, blank = True, null = True)
    description = models.CharField(max_length = 1500)
    datetime = models.DateTimeField(auto_now=True)
    no_files = models.IntegerField(default = 0)

class File(models.Model):
    hid = models.CharField(max_length = 56, primary_key= True)
    title = models.CharField(max_length = 300)
    library = models.ForeignKey(Library, on_delete = models.CASCADE)
    _file  = models.FileField(upload_to="files")
    size = models.IntegerField(default = 0)

class DownloadLot(models.Model):
    zip_name = models.CharField(max_length = 56, primary_key= True)
    visitor = models.ForeignKey(Visitor, on_delete = models.CASCADE, blank = True, null = True)
    library = models.ForeignKey(Library, on_delete = models.CASCADE)
    datetime = models.DateTimeField(auto_now = True)
    files = ArrayField(models.CharField(max_length = 300))
    downloads = models.IntegerField(default = 0)

class Like(models.Model):
    user = models.ForeignKey(Visitor, on_delete = models.CASCADE, blank = True, null = True)
    library = models.ForeignKey(Library, on_delete = models.CASCADE)
    datetime = models.DateTimeField(auto_now = True)
