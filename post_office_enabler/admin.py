from functools import update_wrapper
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from . import models


class PostOfficeEnablerAdmin(admin.ModelAdmin):
    """
    Default `PostOfficeEnabler` admin.

    Most of the overwritten functions are to make the object work as a
    singleton style object.
    """
    change_form_template = 'admin/post_office_enabler/change_form.html'

    def has_add_permission(self, request):
        """
        Singleton pattern: prevent addition of new objects

        :param request: Django request which will be ignored.
        :return: False.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Singleton pattern: prevent addition of new objects

        :param request: Django request which will be ignored.
        :param obj: The requested object.
        :return: False.
        """
        return False

    def get_urls(self):
        """
        Redirect the change list and history to the change page.

        Overwrites the default URLs provided.

        :return: URL patterns.
        """
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(
                r'^history/$',
                wrap(self.history_view),
                {'object_id': '1'},
                name='%s_%s_history' % info
            ),
            url(
                r'^$',
                wrap(self.change_view),
                {'object_id': '1'},
                name='%s_%s_changelist' % info
            ),
            url(
                r'^(.+)/change/$',
                wrap(self.change_view),
                {'object_id': '1'},
                name='%s_%s_change' % info
            ),
        ]
        return urlpatterns

    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.

        :param request: Django request object.
        :param obj: `PostOfficeEnabler` instance.
        :return: `HttpResponseRedirect`.
        """
        msg = _('%(obj)s was changed successfully.') % {'obj': force_text(obj)}
        if '_continue' in request.POST:
            self.message_user(request, _('%(msg)s You may edit it again below.') % {'msg': msg})
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)
            return HttpResponseRedirect('../../')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Override the change view to create singleton style object.

        :param request: Django request object.
        :param object_id: Will always be overwritten to `1`.
        :param form_url: A URL to the a form to use.
        :param extra_context: Additional context to add.
        :return: View.
        """
        if object_id == '1':
            self.model.objects.get_or_create(pk=1)
        return super(PostOfficeEnablerAdmin, self).change_view(
            request,
            object_id,
            extra_context=extra_context,
        )

admin.site.register(models.PostOfficeEnabler, PostOfficeEnablerAdmin)
