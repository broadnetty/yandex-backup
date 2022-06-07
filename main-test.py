#!/usr/bin/python3
import requests
from yacloud import yacloud

encoded_token = yacloud.obtainIAMtoken()

cloudId = yacloud.listClouds(encoded_token)['clouds'][0]['id']

print(id)



