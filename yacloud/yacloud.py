import requests

def obtainIAMtoken(JWTtoken=None):
    if JWTtoken == None:
        headers = { 'Metadata-Flavor': 'Google' }
        r = requests.get(' http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token', headers=headers)
    headers = {}
    r = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens' , {"jwt": JWTtoken})
    return r