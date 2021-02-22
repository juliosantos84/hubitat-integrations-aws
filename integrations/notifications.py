import json
import os
import requests
import boto3

# TODO Parameterize these
ALLOWED_SOURCES = [
    "notifications@adtcontrol.com",
    "julio.r.santos.jr@gmail.com"
]

DESTINATION_ADDRESSES = [
    "doors@automation.everythingbiig.com"
]

# Externalize this config
DOOR_TO_DEVICE_MAP = {
    "Basement Front Door": ["Basement Front Door Light", "Basement Entry Light"],
    "Basement Back Door": ["Backyard Light", "Backyard Outlet"]
}

HUBITAT_ACCESS_TOKEN = os.getenv("HUBITAT_ACCESS_TOKEN", "ACCESS_TOKEN_NOT_CONFIGURED")
HUBITAT_UUID = os.getenv("HUBITAT_UUID", "UUID_NOT_CONFIGURED")
HUBITAT_BASE_URL = f"https://cloud.hubitat.com/api/{HUBITAT_UUID}/apps/9"
HUBITAT_DEVICES_URL = f"{HUBITAT_BASE_URL}/devices?access_token={HUBITAT_ACCESS_TOKEN}"

HUBITAT_SWITCH_ON_URL = f"{HUBITAT_BASE_URL}/devices/%s/on?access_token={HUBITAT_ACCESS_TOKEN}"

HUBITAT_SWITCH_OFF_URL = f"{HUBITAT_BASE_URL}/devices/%s/off?access_token={HUBITAT_ACCESS_TOKEN}"

DEVICE_CACHE = {}
DEVICE_CACHE_BUCKET = os.getenv('DEVICE_CACHE_BUCKET','com.everythingbiig.hubitat')

def lambda_handler(event, context):
    """
    Expects an SNS event with Records representing SES Email notifications.

    Emails have the format:
    Subject: # JULIO SANTOS's System: The Basement Front Door was Opened at 8:04 pm
    Subject: # JULIO SANTOS's System: The [DEVICE NAME] was [ACTION] at [TIME]
    """
    s3 = boto3.client('s3')
    response = s3.get_object(
        Bucket=DEVICE_CACHE_BUCKET,
        Key='devices/nameToIdMap.json',
    )
    if response and response['Body']:
        print ("Loaded devices from s3 cache.")
        global DEVICE_CACHE
        DEVICE_CACHE = json.loads(response['Body'].read().decode("utf-8"))
        print (f"Device Cache: {DEVICE_CACHE}")

    print (response)
    for record in event['Records']:
        handleRecord(record)
    return

def handleRecord(record):
    eventSource = record['EventSource']
    messageString = record['Sns']['Message']
    messageJson = json.loads(messageString)
    # should be notifications@adtcontrol.com
    mailSource = messageJson['mail']['source']
    # should be something like JULIO SANTOS's System: The Basement Front Door was Opened at 8:04 pm
    mailSubject = getSubject(messageJson['mail']['headers'])
    print (f"Source: {mailSource}\nSubject: {mailSubject}")

    for door in DOOR_TO_DEVICE_MAP.keys():
        print (f"Evaluating {door}")
        if door in mailSubject:
            print ("Door is in mail subject")
            lights = DOOR_TO_DEVICE_MAP.get(door)
            for light in lights:
                print (f"Evaluating light {light}")
                turnOnDevice(light)

def turnOnDevice(lightName):
    deviceId = getDeviceId(lightName)
    if deviceId is not None:
        deviceUrl = HUBITAT_SWITCH_ON_URL % (deviceId)
        print (f"DeviceUrl: {deviceUrl}")
        r = requests.get(deviceUrl)
        if r.status_code > 200:
            print ("Something bad happened.")
        else:
            print ("Command sent")
        return
    else:
        raise ValueError("The configured light could not be found, check DEVICE_CACHE")

def getDeviceId(deviceName):
    return DEVICE_CACHE[deviceName]

def getSubject(headerList):
    for header in headerList:
        if header['name'] == 'Subject':
            return header['value']
    return None