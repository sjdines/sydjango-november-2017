from import_export import resources
from . import models


class LeadDetailResource(resources.ModelResource):
    """`import-export` resource for `LeadDetail` model."""
    class Meta:
        model = models.LeadDetail
        fields = [
            'email',
            'first_name',
            'last_name',
            'chase_date',
        ]
        export_order = fields
        import_id_fields = [
            'email',
        ]
