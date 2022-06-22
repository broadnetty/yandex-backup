from .models import CachedResources
from django.forms import ModelForm

class CachedResourcesForm(ModelForm):
    class Meta:
        model = CachedResources
        fields = ["VMid", "VMName", "ZoneId"]
    '''def __init__(self, VMid = None, VMName = None, ZoneId = None):
        self.VMid = VMid
        self.VMName = VMName
        self.ZoneId = ZoneId'''