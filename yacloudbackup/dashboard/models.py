from django.db import models

# Create your models here.
class CachedResources(models.Model):
    vm_id = models.CharField('vm_id', max_length=35)
    vm_name = models.CharField('vm_name', max_length=50)
    zone_id = models.CharField('zone_id', max_length=50)
    folder_id = models.CharField('folder_id', max_length=50)
    cloud_id = models.CharField('cloud_id', max_length=50)

    def __str__(self):
        return self.VMName

    class Meta:
        verbose_name = 'Cached Resource'
        verbose_name_plural = 'Cached Resources'

class CloudAuthAccounts(models.Model):
    cloud_id = models.CharField('cloud_id', max_length=48)
    folder_id = models.CharField('folder_id', max_length=50)
    account_id = models.CharField('account_id', max_length=50)
    account_key_id = models.CharField('account_key_id', max_length=50)
    lockbox_id = models.CharField('lockbox_id', max_length=50)
    kms_key_id = models.CharField('kms_key_id', max_length=50)

    def __str__(self):
        return self.account_id

class CloudVMs(models.Model):
    vm_id = models.CharField('vm_id', max_length=48)
    vm_name = models.CharField('vm_name', max_length=50)
    zone_id = models.CharField('zone_id', max_length=50)
    folder_id = models.CharField('folder_id', max_length=50)
    cloud_id = models.CharField('cloud_id', max_length=50)

    vm_template = models.CharField('vm_template')

    def __str__(self):
        return self.vm_name

class VMdisks(models.Model):
    vm_id = models.CharField('vm_id', max_length=48)
    disk_id = models.CharField('disk_id', max_length=48)
    disk_name = models.CharField('disk_name', max_length=70)
    folder_id = models.CharField('folder_id', max_length=50)
    cloud_id = models.CharField('cloud_id', max_length=50)
    zone_id = models.CharField('zone_id', max_length=50)
    type_id = models.CharField('type_id', max_length=50)
    size = models.CharField('size', max_length=50)

    vm_template = models.CharField('vm_template')

    def __str__(self):
        return self.vm_name