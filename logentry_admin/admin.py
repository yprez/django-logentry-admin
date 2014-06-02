from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _


action_names = {
    ADDITION: _('Addition'),
    DELETION: _('Deletion'),
    CHANGE: _('Change'),
}


class ActionListFilter(admin.SimpleListFilter):
    title = _('Action')
    parameter_name = 'action_flag'

    def lookups(self, request, model_admin):
        return action_names.items()

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(action_flag=self.value())
        return queryset


class UserListFilter(admin.SimpleListFilter):
    title = _('staff user')
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        staff = get_user_model().objects.filter(is_staff=True)
        return (
            (s.id, force_text(s))
            for s in staff
        )

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(user_id=self.value(), user__is_staff=True)
        return queryset


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    readonly_fields = (LogEntry._meta.get_all_field_names() +
                       ['object_link', 'action_description', 'user_link'])

    fieldsets = (
        (_(u'Metadata'), {
            'fields': (
                'action_time',
                'user_link',
                'action_description',
                'object_link',
            )
        }),
        (_(u'Detail'), {
            'fields': (
                'change_message',
                'content_type',
                'object_id',
                'object_repr',
            )
        }),
    )

    list_filter = [
        UserListFilter,
        'content_type',
        ActionListFilter
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display_links = [
        'action_time',
        'change_message',
    ]
    list_display = [
        'action_time',
        'user_link',
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
            except NoReverseMatch:
                link = escape(obj.object_repr)
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def user_link(self, obj):
        try:
            ct = ContentType.objects.get_for_model(obj.user._meta.model)
            link = u'<a href="%s">%s</a>' % (
                reverse(
                    'admin:%s_%s_change' % (ct.app_label, ct.model),
                    args=[obj.user.pk]
                ),
                escape(force_text(obj.user)),
            )
        except NoReverseMatch:
            link = escape(force_text(obj.user))
        return link
    user_link.allow_tags = True
    user_link.admin_order_field = 'user'
    user_link.short_description = u'user'

    def queryset(self, request):
        queryset = super(LogEntryAdmin, self).queryset(request)
        return queryset.prefetch_related('content_type')

    def get_actions(self, request):
        actions = super(LogEntryAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def action_description(self, obj):
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'


admin.site.register(LogEntry, LogEntryAdmin)
