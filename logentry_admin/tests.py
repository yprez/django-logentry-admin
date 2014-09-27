from django.contrib.auth import get_user_model
from django.test import TestCase, Client


User = get_user_model()


class LogentryAdminTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='admin')
        user.is_superuser = True
        user.is_staff = True
        user.set_password('test')
        user.save()

    def test_admin_list(self):
        client = Client()
        client.login(username='admin', password='test')

        res = client.get('/admin/')
        self.assertEquals(res.status_code, 200)
        self.assertIn('Log entries', res.content)
