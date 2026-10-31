from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import path

from logentry_admin.admin import LogEntryAdmin

# A second admin site under its own name, as a project with a custom
# AdminSite has.
other_site = admin.AdminSite(name="other_admin")
other_site.register(User, UserAdmin)
other_site.register(LogEntry, LogEntryAdmin)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("other-admin/", other_site.urls),
]
