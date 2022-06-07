import requests
from yacloud import yacloud

encoded_token = yacloud.obtainIAMtoken()

print(encoded_token)


