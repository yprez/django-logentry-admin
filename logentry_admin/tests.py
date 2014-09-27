from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


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
        self.assertIn('Log entries', res.content)

    def test_admin_logentry_list_view(self):
        client = Client()
        client.login(username='admin', password='test')

        ContentType.objects.get_for_model(User)
        LogEntry.objects.log_action(
            user_id=self.user.id, content_type_id=ContentType.objects.get_for_model(User).id,
            object_id=self.user.id, object_repr=repr(self.user), action_flag=2)

        res = client.get('/admin/admin/logentry/')
        self.assertEquals(res.status_code, 200)
        self.assertIn('Log entries', res.content)
