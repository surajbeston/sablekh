from django.contrib import admin
from .models import Library, File, DownloadLot, DownloadLot, Like, Visitor

admin.site.register(Library)
admin.site.register(Visitor)
admin.site.register(File)
admin.site.register(DownloadLot)
admin.site.register(Like)