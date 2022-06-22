from django.shortcuts import render
from .models import CachedResources
from .forms import CachedResourcesForm

from yacloud import yacloud

def scanResources():
    ya = yacloud.yacloudmanager()
    folders = ya.listFolders(ya.listClouds()['clouds'][0]['id'])['folders']
    for current_folderid in folders:
        if current_folderid['name'] == 'mtop-test-cloud':
            return ya.listInstances(current_folderid['id'])


def dashboard(request):
    return render(request, 'dashboard/resources.html')

def resources(request):
    '''cloud_resources = scanResources()['instances'][0]
    form = CachedResourcesForm()
    form.VMName = cloud_resources['name']
    form.VMid = cloud_resources['id'],
    form.ZoneId = cloud_resources['zoneId']
    form.save()'''
    resources = CachedResources.objects.all()
    return render(request, 'dashboard/resources.html', {'resources' : resources })

def policies(request):
    return render(request, 'dashboard/policies.html')

def sessions(request):
    return render(request, 'dashboard/sessions.html')

    """ya = yacloud.yacloudmanager()
    for i in range(1,40):
        ya.listClouds()
    return HttpResponse(str(ya.listClouds()) + '<br>' + str(ya.listFolders(str(ya.listClouds()['clouds'][0]['id']))))"""