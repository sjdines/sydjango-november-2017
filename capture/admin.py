from django.contrib import admin
from django_object_actions import DjangoObjectActions, takes_instance_or_queryset
from import_export.admin import ImportExportModelAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from . import emailing, models, resources


@admin.register(models.LeadDetail)
class LeadDetailsAdmin(DjangoObjectActions, ImportExportModelAdmin):
    """Admin configuration for `LeadDetails`."""
    change_list_template = 'capture/admin/change_list.html'
    resource_class = resources.LeadDetailResource
    list_display = [
        'email',
        'first_name',
        'last_name',
        'chase_date',
        'created_date_time',
    ]
    list_filter = (
        ('chase_date', DateRangeFilter),
        ('created_date_time', DateTimeRangeFilter),
    )

    change_actions = [
        'send_introduction_email',
    ]
    actions = [
        'send_introduction_email',
    ]

    @takes_instance_or_queryset
    def send_introduction_email(self, request, queryset):
        not_sent_to = []
        for instance in queryset:
            if not emailing.introduction_email(instance.email, instance.first_name):
                not_sent_to.append(instance.email)

        if not_sent_to:
            self.message_user(
                request,
                'Emails were not successfully sent to: %s' % '\n'.join(not_sent_to)
            )
        else:
            self.message_user(request, 'Emails were successfully sent.')
