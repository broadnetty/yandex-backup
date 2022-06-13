import requests
import time, datetime, jwt

class yacloudmanager:

    IAMtoken = None
    tokenExpiration = None
    APItimeout = 5
    isIAMrole = True
    headers = {'Metadata-Flavor': 'Google'}

    def __init__(self):
        self.IAMtoken = self.obtainIAMtoken()
        self.headers = {'Metadata-Flavor': 'Google', 'Authorization': 'Bearer ' + self.IAMtoken}
        return

    #checks if the token is still valid or expired
    def checkTokenAlive(self):
        if self.tokenExpiration - datetime.datetime.utcnow() > datetime.timedelta(seconds=60):
            return self.tokenExpiration
        else:
            self.headers = {'Metadata-Flavor': 'Google'}
            return self.obtainIAMtoken()

    def obtainIAMtoken(self, JWTtoken=None):
        try:
            if JWTtoken == None:
                r = requests.get('http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token',
                                 headers=self.headers, timeout=self.APItimeout)

            return r.json()["access_token"]

        except:

            self.isIAMrole = False
            service_account_id = "ajegng4l26ojveihgs0c"
            key_id = "aje5b9tqno8kbkeq3d9m"  # ID ресурса Key, который принадлежит сервисному аккаунту.

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

            headers = {'Content-Type': 'application/json'}
            r = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens',
                              headers=headers, json={"jwt": encoded_token}, timeout=self.APItimeout)


            self.tokenExpiration = datetime.datetime.fromisoformat(r.json()["expiresAt"].split('.')[0])
            return r.json()["iamToken"]

    def listClouds(self):
        self.checkTokenAlive()
        r = requests.get('https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds',
                         headers=self.headers, timeout=self.APItimeout)
        return r.json()

    def listOrganizations(self):
        self.checkTokenAlive()
        r = requests.get('https://organization-manager.api.cloud.yandex.net/organization-manager/v1/organizations',
                         headers=self.headers, timeout=self.APItimeout)
        return r.json()

    def listClouds(self):
        self.checkTokenAlive()
        r = requests.get('https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds',
                         headers=self.headers, timeout=self.APItimeout)
        return r.json()

    def listFolders(self, cloudId):
        self.checkTokenAlive()
        r = requests.get('https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders',
                         params={'cloudId': cloudId},
                         headers=self.headers, timeout=self.APItimeout)
        return r.json()

    def listInstances(self, folderId):
        self.checkTokenAlive()
        r = requests.get('https://compute.api.cloud.yandex.net/compute/v1/instances', params={'folderId': folderId},
                         headers=self.headers, timeout=self.APItimeout)
        return r.json()