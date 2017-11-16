from django.contrib import admin as django_admin
from django.contrib.auth import get_user_model
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django_dynamic_fixture import G
from django_webtest import WebTest
from mock import Mock, patch

from . import admin, models
from .management.commands import post_office_enabler


User = get_user_model()


class Admin(WebTest):
    def setUp(self):
        self.post_admin = admin.PostOfficeEnablerAdmin(models.PostOfficeEnabler, django_admin.site)
        self.post_office_enabler, created = models.PostOfficeEnabler.objects.get_or_create()

    def tearDown(self):
        self.post_office_enabler.delete()

    def test_admin_can_be_viewed(self):
        user = G(
            User,
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        response = self.app.get(
            reverse('admin:post_office_enabler_postofficeenabler_history'),
            user=user
        )
        self.assertEqual(response.status_code, 200)

        response = self.app.get(
            reverse('admin:post_office_enabler_postofficeenabler_changelist'),
            user=user
        )
        self.assertEqual(response.status_code, 200)

    def test_has_add_permission(self):
        # This should only ever return `False`.
        self.assertFalse(self.post_admin.has_add_permission(None), False)

    def test_has_delete_permission(self):
        # This should only ever return `False`.
        self.assertFalse(self.post_admin.has_add_permission(None), False)

    def test_get_urls(self):
        patterns = self.post_admin.get_urls()
        # Check the returned URLs are the two for the history and the changelist only and the id
        # of the object is always `1`.
        self.assertEqual(len(patterns), 3)
        self.assertEqual(patterns[0].name, 'post_office_enabler_postofficeenabler_history')
        self.assertEqual(patterns[0].default_args, {'object_id': '1'})
        self.assertEqual(patterns[0].regex.pattern, '^history/$')
        self.assertEqual(patterns[1].name, 'post_office_enabler_postofficeenabler_changelist')
        self.assertEqual(patterns[1].default_args, {'object_id': '1'})
        self.assertEqual(patterns[1].regex.pattern, '^$')
        self.assertEqual(patterns[2].name, 'post_office_enabler_postofficeenabler_change')
        self.assertEqual(patterns[2].default_args, {'object_id': '1'})
        self.assertEqual(patterns[2].regex.pattern, '^(.+)/change/$')

    def test_response_change(self):
        request = HttpRequest()
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)

        # Ensure a message and the correct path is provided if no continue parameter is passed.
        response = self.post_admin.response_change(request, self.post_office_enabler)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, '../../')
        messages = [a for a in request._messages]
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].message,
            'Disabled was changed successfully.'
        )

        # Check the redirect works for a passed parameter to continue.
        request.POST = {
            '_continue': 'test',
        }
        request.path = 'test path'

        response = self.post_admin.response_change(request, self.post_office_enabler)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, 'test%20path')
        messages = [a for a in request._messages]
        self.assertEqual(len(messages), 2)
        self.assertEqual(
            messages[1].message,
            'Disabled was changed successfully. You may edit it again below.'
        )

    def test_change_view(self):
        models.PostOfficeEnabler.objects.all().delete()
        self.assertEqual(models.PostOfficeEnabler.objects.count(), 0)

        # Ensure an object of id not equal to `1` does not create an object.
        self.post_admin.change_view(HttpRequest(), '2')
        self.assertEqual(models.PostOfficeEnabler.objects.count(), 0)

        # Ensure an object of id equal to `1` does create an object.
        self.post_admin.change_view(HttpRequest(), '1')
        self.assertEqual(models.PostOfficeEnabler.objects.count(), 1)

        # Ensure an object of id equal to `1` does not create more than one object
        self.post_admin.change_view(HttpRequest(), '1')
        self.assertEqual(models.PostOfficeEnabler.objects.count(), 1)


class Models(WebTest):
    def test_str(self):
        models.PostOfficeEnabler.objects.all().delete()
        instance = models.PostOfficeEnabler.objects.create()
        self.assertEqual(str(instance), 'Disabled')

        instance.is_enabled = True
        instance.save()
        self.assertEqual(str(instance), 'Enabled')

    def test_save(self):
        models.PostOfficeEnabler.objects.all().delete()
        instance = models.PostOfficeEnabler.objects.create()

        self.assertEqual(instance.id, 1)
        instance.id = 2
        instance.save()
        self.assertEqual(instance.id, 1)

    def test_delete(self):
        models.PostOfficeEnabler.objects.all().delete()
        self.assertEqual(models.PostOfficeEnabler.objects.count(), 0)
        instance = models.PostOfficeEnabler.objects.create()
        self.assertEqual(models.PostOfficeEnabler.objects.count(), 1)
        instance.delete()
        self.assertEqual(models.PostOfficeEnabler.objects.count(), 1)
        self.assertEqual(instance, models.PostOfficeEnabler.objects.get())


class ManagementCommand(WebTest):
    @patch('post_office_enabler.management.commands.post_office_enabler.logger')
    def test_post_office_enabler(self, mock_logger):
        # Monkey patch `PostCommand` to `Mock` so we don't send anything out.
        original_command = post_office_enabler.PostCommand
        mock = Mock()
        post_office_enabler.PostCommand = mock

        models.PostOfficeEnabler.objects.all().delete()
        instance = models.PostOfficeEnabler.objects.create()

        post_office_enabler.Command().handle()

        self.assertEqual(mock_logger.info.call_count, 1)
        mock_logger.info.assert_called_with(
            'Post office trigger currently disabled, terminating now.'
        )

        instance.is_enabled = True
        instance.save()

        post_office_enabler.Command().handle()
        self.assertEqual(mock.call_count, 1)

        # End monkey patching
        post_office_enabler.PostCommand = original_command
