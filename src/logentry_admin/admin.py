from django.contrib import admin
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import NoReverseMatch, reverse
from django.utils.encoding import force_str
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

action_names = {
    ADDITION: pgettext_lazy("logentry_admin:action_type", "Addition"),
    DELETION: pgettext_lazy("logentry_admin:action_type", "Deletion"),
    CHANGE: pgettext_lazy("logentry_admin:action_type", "Change"),
}


class ActionListFilter(admin.SimpleListFilter):
    title = _("action")
    parameter_name = "action_flag"

    def lookups(self, request, model_admin):
        return action_names.items()

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(action_flag=self.value())
        return queryset


class UserListFilter(admin.SimpleListFilter):
    title = _("staff user")
    parameter_name = "user"

    def lookups(self, request, model_admin):
        staff = get_user_model().objects.filter(is_staff=True)
        return ((s.id, force_str(s)) for s in staff)

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(
                user_id=self.value(), user__is_staff=True
            )
        return queryset


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = "action_time"

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

    list_filter = (
        UserListFilter,
        "content_type",
        ActionListFilter,
    )

    search_fields = (
        "object_repr",
        "change_message",
    )

    list_select_related = ("content_type", "user")

    list_display_links = (
        "action_time",
        "get_change_message",
    )
    list_display = (
        "action_time",
        "user_link",
        "content_type",
        "object_link",
        "action_description",
        "get_change_message",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        object_link = escape(obj.object_repr)
        content_type = obj.content_type

        if obj.action_flag != DELETION and content_type is not None:
            # try returning an actual link instead of object repr string
            try:
                url = reverse(
                    f"admin:{content_type.app_label}_{content_type.model}_change",
                    args=[obj.object_id],
                )
                object_link = f'<a href="{url}">{object_link}</a>'
            except NoReverseMatch:
                pass
        return mark_safe(object_link)

    object_link.admin_order_field = "object_repr"
    object_link.short_description = _("object")

    def user_link(self, obj):
        content_type = ContentType.objects.get_for_model(type(obj.user))
        user_link = escape(force_str(obj.user))
        try:
            # try returning an actual link instead of object repr string
            url = reverse(
                f"admin:{content_type.app_label}_{content_type.model}_change",
                args=[obj.user.pk],
            )
            user_link = f'<a href="{url}">{user_link}</a>'
        except NoReverseMatch:
            pass
        return mark_safe(user_link)

    user_link.admin_order_field = "user"
    user_link.short_description = _("user")

    def action_description(self, obj):
        return action_names[obj.action_flag]

    action_description.short_description = _("action")

    def get_change_message(self, obj):
        return obj.get_change_message()

    get_change_message.short_description = _("change message")


admin.site.register(LogEntry, LogEntryAdmin)
