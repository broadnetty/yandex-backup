import time
import jwt
import yandexcloud

from yandex.cloud.resourcemanager.v1.cloud_service_pb2 import ListCloudsRequest
from yandex.cloud.resourcemanager.v1.cloud_service_pb2_grpc import CloudServiceStub


def handler(event, context):
    cloud_service = yandexcloud.SDK().client(CloudServiceStub)
    clouds = {}
    for c in cloud_service.List(ListCloudsRequest()).clouds:
        clouds[c.id] = c.name
    return clouds

print(clouds)

service_account_id = "ajegng4l26ojveihgs0c"
key_id = "aje5b9tqno8kbkeq3d9m" # The ID of the Key resource belonging to the service account.

with open("backup-account-key.pem", 'r') as private:
  private_key = private.read() # Reading the private key from the file.

now = int(time.time())
payload = {
        'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        'iss': service_account_id,
        'iat': now,
        'exp': now + 360}

# JWT generation.
encoded_token = jwt.encode(
    payload,
    private_key,
    algorithm='PS256',
    headers={'kid': key_id})

print(encoded_token)

