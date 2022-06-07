import requests
import time, jwt

def obtainIAMtoken(JWTtoken=None):
    try:
        if JWTtoken == None:
            print("obtaining token")
            headers = { 'Metadata-Flavor': 'Google' }
            r = requests.get(' http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token', headers=headers, timeout=5)

        return r.json("access_token")
    except:
        service_account_id = "ajegng4l26ojveihgs0c"
        key_id = "ajegng4l26ojveihgs0c"  # ID ресурса Key, который принадлежит сервисному аккаунту.

        with open("backup-account-key.pem", 'r') as private:
            private_key = private.read()  # Чтение закрытого ключа из файла.

        now = int(time.time())
        payload = {
            'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            'iss': service_account_id,
            'iat': now,
            'exp': now + 360}

        encoded_token = jwt.encode(
            payload,
            private_key,
            algorithm='PS256',
            headers={'kid': key_id})
        return encoded_token