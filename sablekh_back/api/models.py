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

User._meta.get_field('email')._unique = True

class Visitor(User):
    hid = models.CharField(max_length = 56, primary_key= True)

class Library(models.Model):
    hid = models.CharField(max_length = 56, primary_key= True)
    title = models.CharField(max_length = 300)
    user = models.ForeignKey(Visitor, on_delete = models.CASCADE, blank = True, null = True)
    description = models.CharField(max_length = 1500)
    link_str = models.CharField(max_length = 350, unique=True)
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

stem_ana = StemmingAnalyzer()
WHOOSH_SCHEMA = Schema(hid = KEYWORD(stored = True), title=TEXT(analyzer = stem_ana, stored=True), description=TEXT(analyzer = stem_ana, stored = True))

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
