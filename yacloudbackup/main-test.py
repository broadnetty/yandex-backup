#!/usr/bin/python3
from yacloud import yacloud


def scanResources():
    ya = yacloud.yacloudmanager()
    folders = ya.listFolders(ya.listClouds()[0]['id'])
    for current_folderid in folders:
        if current_folderid['name'] == 'default':
            return ya.listInstances(current_folderid['id'])

ya = yacloud.yacloudmanager()

print(ya.snpashotVM('epddmtr29rvmidinjn92'))
#print(ya.attachDisk('epddmtr29rvmidinjn92', 'epd3tf0t60cv3l493g6l'))

""" epd85d6da4qem8sb37pv
encoded_token = yacloud.obtainIAMtoken()

cloudId = yacloud.listClouds(encoded_token)['clouds'][0]['id']

print(cloudId)

folders = yacloud.listFolders(encoded_token, cloudId)['folders']

print(folders)

for folder in folders:
    if folder['name'] == 'mtop-test-cloud':
        print(yacloud.listInstances(encoded_token, folder['id']))
"""