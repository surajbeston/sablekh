from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

import os
from django.db.models import signals
from django.conf import settings
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer

from django.db.models.signals import class_prepared

from pytz import timezone 

User._meta.get_field('email')._unique = True

class Visitor(User):
    hid = models.CharField(max_length = 56, primary_key= True)

class Library(models.Model):
    hid = models.CharField(max_length = 56, primary_key= True)
    title = models.CharField(max_length = 300)
    user = models.ForeignKey(Visitor, on_delete = models.CASCADE, blank = True, null = True)
    description = models.CharField(max_length = 1500)
    thumbnail = models.URLField(default="https://postimg.cc/qNT1Hgy5")
    link_str = models.CharField(max_length = 350, unique=True)
    tags = ArrayField(models.CharField(max_length = 150), blank = True, null = True)
    finished = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now=True)
    no_files = models.IntegerField(default = 0)

class File(models.Model):
    hid = models.CharField(max_length = 56, primary_key= True)
    title = models.CharField(max_length = 300)
    library = models.ForeignKey(Library, on_delete = models.CASCADE, blank = "true", null = "true")
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

class Tag(models.Model):
    title = models.CharField(max_length = 150)
    datetime = models.DateTimeField(auto_now=True)

class PwResetToken(models.Model):
    token = models.CharField(max_length=150)
    user = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    is_used = models.BooleanField(default = True)
    datetime = models.DateTimeField(auto_now=True)    

class ImplicitData(models.Model):
    user = models.ForeignKey(Visitor, on_delete = models.CASCADE, null = True, blank = True)
    user_agent = models.CharField(max_length = 600)
    referer = models.CharField(max_length = 300)
    link = models.CharField(max_length=200)
    origin = models.CharField(max_length = 150)
    method = models.CharField(max_length=200)
    api_link = models.CharField(max_length = 100)
    ip = models.CharField(max_length = 20)
    time_taken = models.FloatField()
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        nepal_time = self.datetime.astimezone(timezone("Asia/Katmandu"))
        return nepal_time.strftime("%c")

class RestrictedIP(models.Model):
    ip = models.CharField(max_length = 20)
    reason = models.CharField(max_length = 300)
    datetime = models.DateTimeField(auto_now= True)

stem_ana = StemmingAnalyzer()
WHOOSH_SCHEMA = Schema(hid = KEYWORD(stored = True), title=TEXT(analyzer = stem_ana), description=TEXT(analyzer = stem_ana))

def create_index(sender=None, **kwargs):
    if not os.path.exists(settings.WHOOSH_INDEX):
        os.mkdir(settings.WHOOSH_INDEX)

create_index()

def update_index(sender, instance, created, **kwargs):
    # Code below is just for development.
    all_libraries = Library.objects.all()
    if len(all_libraries) <= 1:
        ix = create_in("index", WHOOSH_SCHEMA)
    else:
        ix = open_dir("index")
    writer = ix.writer()
    if created:
        writer.add_document(hid = instance.hid, title=instance.title, description=instance.description)
        writer.commit()
    else:
        writer.update_document(hid = instance.hid, title=instance.title, description=instance.description)
        writer.commit()

signals.post_save.connect(update_index, sender=Library)

def longer_token(sender, *args, **kwargs):
    if sender.__name__ == "Token":
        sender._meta.get_field("key").max_length = 70

class_prepared.connect(longer_token)
