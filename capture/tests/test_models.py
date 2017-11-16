from django.test import TestCase
from django.utils import six
from django_dynamic_fixture import N

from .. import models


class LeadDetailTest(TestCase):
    def test_str(self):
        lead = N(models.LeadDetail)
        self.assertEqual(
            six.text_type(lead),
            '%s %s - %s' % (
                lead.first_name,
                lead.last_name,
                lead.email,
            )
        )
