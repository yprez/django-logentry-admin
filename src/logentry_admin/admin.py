"""A read-only admin for the log of actions taken in the Django admin."""

from django.contrib import admin
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.admin.utils import quote
from django.contrib.auth import get_user_model
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

action_names = {
    ADDITION: pgettext_lazy("logentry_admin:action_type", "Addition"),
    DELETION: pgettext_lazy("logentry_admin:action_type", "Deletion"),
    CHANGE: pgettext_lazy("logentry_admin:action_type", "Change"),
}


class ActionListFilter(admin.SimpleListFilter):
    """Filter the log by action: addition, change or deletion."""

    title = _("action")
    parameter_name = "action_flag"

    def lookups(self, request, model_admin):
        return action_names.items()

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(action_flag=self.value())
        return queryset


class UserListFilter(admin.SimpleListFilter):
    """Filter the log by the staff user who took the action."""

    title = _("staff user")
    parameter_name = "user"

    def lookups(self, request, model_admin):
        staff = get_user_model().objects.filter(is_staff=True)
        return [(user.pk, str(user)) for user in staff]

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(
                user_id=self.value(), user__is_staff=True
            )
        return queryset


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """List and show log entries, which cannot be added, changed or
    deleted."""

    date_hierarchy = "action_time"

    # The page is read-only without it, since change permission is always
    # refused. It stays for subclasses that build on it.
    readonly_fields = [f.name for f in LogEntry._meta.fields] + [
        "object_link",
        "action_description",
        "user_link",
        "get_change_message",
    ]

    fieldsets = (
        (
            _("Metadata"),
            {
                "fields": (
                    "action_time",
                    "user_link",
                    "action_description",
                    "object_link",
                )
            },
        ),
        (
            _("Details"),
            {
                "fields": (
                    "get_change_message",
                    "content_type",
                    "object_id",
                    "object_repr",
                )
            },
        ),
    )

    list_filter = [
        UserListFilter,
        "content_type",
        ActionListFilter,
    ]

    search_fields = [
        "object_repr",
        "change_message",
    ]

    list_select_related = ["content_type", "user"]

    list_display_links = [
        "action_time",
        "get_change_message",
    ]
    list_display = [
        "action_time",
        "user_link",
        "content_type",
        "object_link",
        "action_description",
        "get_change_message",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description=_("object"), ordering="object_repr")
    def object_link(self, obj):
        content_type = obj.content_type
        url = None
        if obj.action_flag != DELETION and content_type is not None:
            url = self._change_url(
                content_type.app_label, content_type.model, obj.object_id
            )
        return self._link(url, obj.object_repr)

    @admin.display(description=_("user"), ordering="user")
    def user_link(self, obj):
        opts = obj.user._meta
        url = self._change_url(opts.app_label, opts.model_name, obj.user.pk)
        return self._link(url, obj.user)

    @admin.display(description=_("action"))
    def action_description(self, obj):
        return action_names[obj.action_flag]

    @admin.display(description=_("change message"))
    def get_change_message(self, obj):
        return obj.get_change_message()

    def _change_url(self, app_label, model_name, object_id):
        """Return the object's change page on this admin site, or None
        when the site does not register its model."""
        try:
            return reverse(
                f"{self.admin_site.name}:{app_label}_{model_name}_change",
                args=[quote(object_id)],
            )
        except NoReverseMatch:
            return None

    @staticmethod
    def _link(url, text):
        if url is None:
            return format_html("{}", text)
        return format_html('<a href="{}">{}</a>', url, text)
