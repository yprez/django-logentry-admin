from django.contrib import admin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter


action_names = {
    ADDITION: _('Addition'),
    DELETION: _('Deletion'),
    CHANGE: _('Change'),
}


class ActionListFilter(SimpleListFilter):
    title = _('Action')
    parameter_name = 'action_flag'

    def lookups(self, request, model_admin):
        return action_names.items()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                action_flag=self.value()
            )
        else:
            return queryset


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    readonly_fields = LogEntry._meta.get_all_field_names() + \
                      ['object_link', 'action_description']

    list_filter = [
        'user',
        'content_type',
        ActionListFilter
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_description',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            try:
                link = u'<a href="%s">%s</a>' % (
                    reverse(
                        'admin:%s_%s_change' % (ct.app_label, ct.model),
                        args=[obj.object_id]
                    ),
                    escape(obj.object_repr),
                )
            except:
                link = escape(obj.object_repr)
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def action_description(self, obj):
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'


admin.site.register(LogEntry, LogEntryAdmin)
