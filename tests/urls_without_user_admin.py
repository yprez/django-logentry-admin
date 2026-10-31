"""An admin site that registers the log entries and nothing else."""

from django.contrib.admin import AdminSite
from django.contrib.admin.models import LogEntry
from django.urls import path

from logentry_admin.admin import LogEntryAdmin

site = AdminSite()
site.register(LogEntry, LogEntryAdmin)

urlpatterns = [
    path("admin/", site.urls),
]
