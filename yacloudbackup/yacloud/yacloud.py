import requests
import time, datetime, jwt, psycopg2, json

class yacloudmanager:
    '''
    Class for executing Yandex API calls. It keeps the IAM token and refreshes it at the call if the token is expired.
    '''

    IAMtoken = None
    tokenExpiration = None
    APItimeout = 5
    isIAMrole = True
    headers = {'Metadata-Flavor': 'Google'}

    def __init__(self):
        self.IAMtoken = self.obtainIAMtoken()
        self.headers = {'Metadata-Flavor': 'Google', 'Authorization': 'Bearer ' + self.IAMtoken}
        return

    def checkTokenAlive(self):
        '''
        Checks if the token is still valid or expired.
        :return: Token expiration datetime var or renews and returns an expired token.
        '''
        if self.tokenExpiration - datetime.datetime.utcnow() > datetime.timedelta(seconds=60):
            return self.tokenExpiration
        else:
            self.headers = {'Metadata-Flavor': 'Google'}
            return self.obtainIAMtoken()

    def obtainIAMtoken(self):
        '''
        Obtains IAM token needed for API calls by trying: pulling token from the IAM role or using local key in debug mode.
        :return: String value of the IAM token
        '''
        try:
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
        '''
        :return: (JSON data) List of dicts with clouds' data
        '''
        self.checkTokenAlive()
        r = requests.get('https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds',
                         headers=self.headers, timeout=self.APItimeout)
        if r.json() != {}:
            return r.json()['clouds']
        else:
            return {}

    def listOrganizations(self):
        self.checkTokenAlive()
        r = requests.get('https://organization-manager.api.cloud.yandex.net/organization-manager/v1/organizations',
                         headers=self.headers, timeout=self.APItimeout)
        if r.json() != {}:
            return r.json()
        else:
            return {}

    def listFolders(self, cloudId):
        '''
        Lists cloud folders data filtered by cloudId
        :param cloudId: String value of cloudId
        :return: (JSON data) List of dicts with folders' data
        '''
        self.checkTokenAlive()
        r = requests.get('https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders',
                         params={'cloudId': cloudId},
                         headers=self.headers, timeout=self.APItimeout)
        if r.json() != {}:
            return r.json()['folders']
        else:
            return {}

    def listInstances(self, folderId):
        '''
        Lists VM instances in the cloud folder
        :param folderId: String value of folderId
        :return: (JSON data) List of dicts with instances' data
        '''
        self.checkTokenAlive()
        r = requests.get('https://compute.api.cloud.yandex.net/compute/v1/instances', params={'folderId': folderId},
                         headers=self.headers, timeout=self.APItimeout)

        if r.json() != {}:
            return r.json()['instances']
        else:
            return {}

    def getVm(self, vmId):
        self.checkTokenAlive()
        r = requests.get('https://compute.api.cloud.yandex.net/compute/v1/instances/' + vmId,
                         headers=self.headers, timeout=self.APItimeout)

        if r.json() != {}:
            return r.json()
        else:
            return {}

    def listDisks(self, folderId):
        self.checkTokenAlive()
        r = requests.get('https://compute.api.cloud.yandex.net/compute/v1/disks', params={'folderId': folderId},
                         headers=self.headers, timeout=self.APItimeout)

        if r.json() != {}:
            return r.json()['disks']
        else:
            return {}

    def findDiskById(self, diskId):

        #temp code
        for cloud in self.listClouds():
            for folder in self.listFolders(cloud['id']):
                for disk in self.listDisks(folder['id']):
                    if disk['id'] == diskId:
                        return {'folderId': folder['id'], 'diskId': disk['id']}
        #endtempcode

    def createDiskSnapshot(self, diskId, folderId):
        r = requests.post('https://compute.api.cloud.yandex.net/compute/v1/snapshots', json={'folderId': folderId, 'diskId': diskId},
                         headers=self.headers, timeout=self.APItimeout)

        if r.status_code == 200:
            return True
        else:
            if r.json() != {}:
                return r.json()
            else:
                return('Unknown error')

    def attachDisk(self, instanceId, diskId):
        data = {"attachedDiskSpec": {"autoDelete": True, "diskId": diskId} }

        r = requests.post('https://compute.api.cloud.yandex.net/compute/v1/instances/' + instanceId + ':attachDisk', json=data,
                         headers=self.headers, timeout=self.APItimeout)

        if r.status_code == 200:
            return True
        else:
            if r.json() != {}:
                return r.json()
            else:
                return('Unknown error')

    def snpashotVM(self, vmId):
        vm = self.getVm(vmId)
        print(self.createDiskSnapshot(vm['bootDisk']['diskId'], vm['folderId']))

        for disk in vm['secondaryDisks']:
            print(self.createDiskSnapshot(disk['diskId'], vm['folderId']))
        return

    def scanResources(self):
        '''

        :return: True if the SQL executed correctly
        '''
        folders = self.listFolders(self.listClouds()[0]['id'])

        conn = psycopg2.connect(
            host="localhost",
            database="yacloudbackup",
            user="postgres",
            password="7ujMko0admin!")

        cur = conn.cursor()

        for current_folderid in folders:
            if current_folderid['name'] == 'mtop-test-cloud':
                vm = self.listInstances(current_folderid['id'])[0]
                sql = 'INSERT INTO dashboard_cachedresources ("vm_id", "vm_name", "zone_id", "folder_id", "cloud_id") VALUES(' + "'" + str(vm['id']) + "','" + str(vm['name']) + "','" + str(vm['zoneId']) + "','" + str(vm['folderId']) + "','" + "mycloud');"
                cur.execute(sql) #, (str(vm['id']), str(vm['name']), str(vm['zoneId']), str(vm['folderId']), 'mycloud'))
        conn.commit()
        conn.close()

        return True;