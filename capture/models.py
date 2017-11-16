from disposable_email_checker.fields import DisposableEmailField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class LeadDetail(models.Model):
    """Capture lead details."""
    email = DisposableEmailField()
    first_name = models.CharField(
        max_length=255,
    )
    last_name = models.CharField(
        max_length=255,
    )

    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)

    chase_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Date to chase up lead.')
    )

    def __str__(self):
        return '{first_name} {last_name} - {email}'.format(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
        ).strip()
