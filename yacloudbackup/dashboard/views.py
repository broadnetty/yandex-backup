from django.shortcuts import render
from django.http import HttpResponse

from yacloud import yacloud



# Create your views here.
def dashboard(reueqst):
    ya = yacloud.yacloudmanager()
    for i in range(1,40):
        ya.listClouds()
    return HttpResponse(str(ya.listClouds()) + '<br>' + str(ya.listFolders(str(ya.listClouds()['clouds'][0]['id']))))