from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

import pytest

from logentry_admin.admin import LogEntryAdmin


@pytest.fixture
def admin():
    return LogEntryAdmin(LogEntry, AdminSite())


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


def test_object_link(admin, admin_user):
    log_entry = LogEntry(
        content_type_id=ContentType.objects.get_for_model(User).id,
        action_flag=ADDITION,
        object_id=admin_user.id,
        object_repr='OBJ_REPR'
    )
    assert 'OBJ_REPR' in admin.object_link(log_entry)
    assert '<a href="' in admin.object_link(log_entry)


def test_object_link_deleted(admin, admin_user):
    log_entry = LogEntry(object_repr='OBJ_REPR', action_flag=DELETION)
    assert admin.object_link(log_entry) == 'OBJ_REPR'


def test_object_link_no_reverse(admin, admin_user):
    log_entry = LogEntry(
        content_type_id=ContentType.objects.get(model='session').id,
        action_flag=CHANGE,
        object_id=5,
        object_repr='OBJ_REPR'
    )
    assert admin.object_link(log_entry) == 'OBJ_REPR'


def test_user_link(admin_user):
    admin = LogEntryAdmin(LogEntry, AdminSite())
    logentry = LogEntry(object_repr='OBJ_REPR', action_flag=DELETION,
                        user_id=admin_user.id)

    assert '<a href="' in admin.user_link(logentry)
    assert admin_user.username in admin.user_link(logentry)
