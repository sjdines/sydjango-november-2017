from django import forms
from . import models


class LeadDetailForm(forms.ModelForm):
    """Lead capturing form."""
    class Meta:
        model = models.LeadDetail
        fields = [
            'email',
            'first_name',
            'last_name',
        ]
