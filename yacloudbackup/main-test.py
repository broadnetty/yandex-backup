#!/usr/bin/python3
from yacloud import yacloud

yacm = yacloud.yacloudmanager()

print(yacm.listClouds())
"""
encoded_token = yacloud.obtainIAMtoken()

cloudId = yacloud.listClouds(encoded_token)['clouds'][0]['id']

print(cloudId)

folders = yacloud.listFolders(encoded_token, cloudId)['folders']

print(folders)

for folder in folders:
    if folder['name'] == 'mtop-test-cloud':
        print(yacloud.listInstances(encoded_token, folder['id']))
"""