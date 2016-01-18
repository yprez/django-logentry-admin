from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from logentry_admin.admin import LogEntryAdmin


class LogentryAdminTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='admin')
        user.is_superuser = True
        user.is_staff = True
        user.set_password('test')
        user.save()
        self.user = user

    def test_admin_list_apps(self):
        client = Client()
        client.login(username='admin', password='test')

        res = client.get('/admin/')
        self.assertEquals(res.status_code, 200)
        self.assertIn('Log entries', res.content.decode())

    def test_admin_logentry_list_view(self):
        client = Client()
        client.login(username='admin', password='test')

        ContentType.objects.get_for_model(User)
        LogEntry.objects.log_action(
            user_id=self.user.id, content_type_id=ContentType.objects.get_for_model(User).id,
            object_id=self.user.id, object_repr=repr(self.user), action_flag=CHANGE)

        res = client.get('/admin/admin/logentry/')
        self.assertEquals(res.status_code, 200)
        self.assertIn('Log entries', res.content.decode())

    def test_object_link(self):
        admin = LogEntryAdmin(LogEntry, AdminSite())
        deleted = LogEntry(object_repr='OBJ_REPR', action_flag=DELETION)
        self.assertEquals(admin.object_link(deleted), 'OBJ_REPR')

        created = LogEntry(
            content_type_id=ContentType.objects.get_for_model(User).id,
            action_flag=ADDITION,
            object_id=self.user.id,
            object_repr='OBJ_REPR'
        )
        self.assertIn('OBJ_REPR', admin.object_link(created))
        self.assertIn('<a href="', admin.object_link(created))

        no_reverse = LogEntry(
            content_type_id=ContentType.objects.get(model='session').id,
            action_flag=CHANGE,
            object_id=5,
            object_repr='OBJ_REPR'
        )
        self.assertEquals(admin.object_link(no_reverse), 'OBJ_REPR')

    def test_user_link(self):
        admin = LogEntryAdmin(LogEntry, AdminSite())
        logentry = LogEntry(object_repr='OBJ_REPR', action_flag=DELETION, user_id=self.user.id)

        self.assertIn('<a href="', admin.user_link(logentry))
        self.assertIn(self.user.username, admin.user_link(logentry))
