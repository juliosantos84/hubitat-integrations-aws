import json
import boto3
import requests

HUBITAT_ACCESS_TOKEN = os.getenv("HUBITAT_ACCESS_TOKEN", "ACCESS_TOKEN_NOT_CONFIGURED")
HUBITAT_UUID = os.getenv("HUBITAT_UUID", "UUID_NOT_CONFIGURED")
HUBITAT_BASE_URL = f"https://cloud.hubitat.com/api/{HUBITAT_UUID}/apps/9"
HUBITAT_DEVICES_URL = f"{HUBITAT_BASE_URL}/devices?access_token={HUBITAT_ACCESS_TOKEN}"

def lambda_handler(event, context):
    r = requests.get(HUBITAT_DEVICES_URL)
    if r.status_code > 200:
        raise Exception("Unable to retrieve device list")

    nameToIdMap = mapNamesToIds(r.json)

    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=os.getenv(DEVICE_CACHE_BUCKET,'com.everythingbiig.hubitat'),
        Key='devices/nameToIdMap.json',
        Body=json.dumps(nameIdMap).encode("utf-8")
    )

def mapNamesToIds(devices):
    nameToIdMap = {}
    if devices is not None:
        for device in devices:
            name = device['label']
            deviceId = device['id']
            nameToIdMap[name] = deviceId
    return nameToIdMap

