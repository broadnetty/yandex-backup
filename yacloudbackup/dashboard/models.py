from django.db import models

# Create your models here.
class CachedResources(models.Model):
    VMid = models.CharField('vmid', max_length=35)
    VMName = models.CharField('vmname', max_length=50)
    ZoneId = models.CharField('zoneid', max_length=50)
    FolderId = models.CharField('folderid', max_length=50)
    CloudId = models.CharField('cloudid', max_length=50)

    def __str__(self):
        return self.VMName

    class Meta:
        verbose_name = 'Cached Resource'
        verbose_name_plural = 'Cached Resources'