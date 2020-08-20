from django.contrib import admin
from .models import Library, File, DownloadLot, Like, Visitor, ImplicitData, RestrictedIP, PwResetToken

admin.site.register(Library)
admin.site.register(Visitor)
admin.site.register(File)
admin.site.register(DownloadLot)
admin.site.register(Like)
admin.site.register(ImplicitData)
admin.site.register(RestrictedIP)
admin.site.register(PwResetToken)