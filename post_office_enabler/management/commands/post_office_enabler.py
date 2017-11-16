from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
from optparse import make_option
from post_office.logutils import setup_loghandlers
from post_office.management.commands.send_queued_mail import Command as PostCommand
from ...models import PostOfficeEnabler


logger = setup_loghandlers()


class Command(BaseCommand):
    """
    Refer to help message below.
    """
    help = _(
        'A command that will send emails with a fail safe switch in the admin ('
        '`PostOfficeEnabler`).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--processes',
            type='int',
            help='Number of processes used to send emails',
            default=1
        )
        parser.add_argument(
            '-L',
            '--lockfile',
            type='string',
            help='Absolute path of lockfile to acquire'
        )
        parser.add_argument(
            '-l',
            '--log-level',
            type='int',
            help='"0" to log nothing, "1" to only log errors'
        )

    def handle(self, *args, **options):
        """
        Check if the `PostOfficeEnabler` is turned on to send email.

        Refer to `post_office_enabler.models.PostOfficeEnabler` for
        further information.

        :param args: arguments.
        :param options: options from the command line.
        :return: None
        """
        trigger, _ = PostOfficeEnabler.objects.get_or_create(id=1)

        # Only send email if the trigger is enabled.
        if trigger.is_enabled:
            PostCommand().handle(*args, **options)
        else:
            logger.info('Post office trigger currently disabled, terminating now.')
