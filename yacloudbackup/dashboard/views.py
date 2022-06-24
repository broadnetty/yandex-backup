from django.shortcuts import render
from .models import CachedResources

from yacloud import yacloud



def dashboard(request):
    return render(request, 'dashboard/resources.html')

def resources(request):
    ya = yacloud.yacloudmanager()
    folders = ya.listFolders(ya.listClouds()[0]['id'])
    for current_folderid in folders:
        if current_folderid['name'] == 'mtop-test-cloud':
            resources = ya.listInstances(current_folderid['id'])

    #resources = CachedResources.objects.all()
    return render(request, 'dashboard/resources.html', {'resources' : resources })

def policies(request):
    return render(request, 'dashboard/policies.html')

def sessions(request):
    return render(request, 'dashboard/sessions.html')
