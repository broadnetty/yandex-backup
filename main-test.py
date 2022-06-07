#!/usr/bin/python3
import requests
from yacloud import yacloud

encoded_token = yacloud.obtainIAMtoken()

print(encoded_token)


