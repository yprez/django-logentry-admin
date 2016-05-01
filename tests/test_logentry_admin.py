from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

from logentry_admin.admin import LogEntryAdmin


def test_admin_list_apps(admin_client):
    res = admin_client.get('/admin/')
    assert res.status_code == 200
    assert 'Log entries' in res.content.decode()


def test_admin_logentry_list_view(admin_client, admin_user):
    LogEntry.objects.log_action(
        user_id=admin_user.id,
        content_type_id=ContentType.objects.get_for_model(User).id,
        object_id=admin_user.id,
        object_repr=repr(admin_user),
        action_flag=CHANGE
    )

    res = admin_client.get('/admin/admin/logentry/')
    assert res.status_code == 200
    assert 'Log entries' in res.content.decode()


def test_admin_logentry_list_view_filters(admin_client, admin_user):
    LogEntry.objects.log_action(
        user_id=admin_user.id,
        content_type_id=ContentType.objects.get_for_model(User).id,
        object_id=admin_user.id,
        object_repr=repr(admin_user),
        action_flag=CHANGE
    )

    res = admin_client.get('/admin/admin/logentry/', {
        'action_flag': CHANGE,
        'user': admin_user.id,
    })
    assert res.status_code == 200
    assert 'Log entries' in res.content.decode()


def test_object_link(admin_user):
    admin = LogEntryAdmin(LogEntry, AdminSite())

    deleted = LogEntry(object_repr='OBJ_REPR', action_flag=DELETION)
    assert admin.object_link(deleted) == 'OBJ_REPR'

    created = LogEntry(
        content_type_id=ContentType.objects.get_for_model(User).id,
        action_flag=ADDITION,
        object_id=admin_user.id,
        object_repr='OBJ_REPR'
    )
    assert 'OBJ_REPR' in admin.object_link(created)
    assert '<a href="' in admin.object_link(created)

    no_reverse = LogEntry(
        content_type_id=ContentType.objects.get(model='session').id,
        action_flag=CHANGE,
        object_id=5,
        object_repr='OBJ_REPR'
    )
    assert admin.object_link(no_reverse) == 'OBJ_REPR'


def test_user_link(admin_user):
    admin = LogEntryAdmin(LogEntry, AdminSite())
    logentry = LogEntry(object_repr='OBJ_REPR', action_flag=DELETION,
                        user_id=admin_user.id)

    assert '<a href="' in admin.user_link(logentry)
    assert admin_user.username in admin.user_link(logentry)
