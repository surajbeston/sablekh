from django.contrib import admin
from .models import Library, File, DownloadLot, Like, Visitor, ImplicitData, RestrictedIP, PwResetToken, LibraryGroup

admin.site.site_header = 'Sablekh Admin'
admin.site.site_title = 'Sablekh Admin'

admin.site.register(Library)
admin.site.register(Visitor)
admin.site.register(File)
admin.site.register(DownloadLot)
admin.site.register(Like)
admin.site.register(ImplicitData)
admin.site.register(RestrictedIP)
admin.site.register(PwResetToken)
admin.site.register(LibraryGroup)