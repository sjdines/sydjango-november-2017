from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _


@python_2_unicode_compatible
class PostOfficeEnabler(models.Model):
    """
    Should `post_office` send email?

    This is designed to be a singleton type model where a boolean is
    enabled to send email out or if it is false emails will just queue
    and not be sent.

    The post office enabler provides administration access to turn off
    the sending of emails by the admin. It will still queue all of the
    emails but turn off the actual sending component which happens via
    a management command. The management command will still run but
    will check to see if the sending is enabled or disabled. If it is
    enabled the emails will send as per the normal process otherwise if
    it is disabled it will exit the function without performing any
    operations.
    """
    is_enabled = models.BooleanField(
        verbose_name=_('Email sending enabled'),
        default=False,
        help_text=_('Should emails be sent to users? If enabled it will send the queued emails.'),
    )

    class Meta:
        verbose_name_plural = _('Post Office Enabler')

    def __str__(self):
        """
        String representation of `PostOfficeEnabler` instance.

        :return: String.
        """
        return 'Enabled' if self.is_enabled else 'Disabled'

    def save(self, *args, **kwargs):
        """
        Always set the `id` to `1`.

        This means that only one instance of the object can exist at a
        time e.g. a singleton.

        :param args: arguments
        :param kwargs: keyword arguments.
        :return: None.
        """
        self.id = 1
        super(PostOfficeEnabler, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Don't allow this instance to be deleted.

        We always require 1 and only 1 instance of this object.

        :param args: arguments
        :param kwargs: keyword arguments.
        :return: None.
        """
        pass

