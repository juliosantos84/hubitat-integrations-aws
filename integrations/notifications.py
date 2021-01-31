import json
import os
import requests

ALLOWED_SOURCES = [
    "notifications@adtcontrol.com",
    "julio.r.santos.jr@gmail.com"
]

DESTINATION_ADDRESSES = [
    "doors@automation.everythingbiig.com"
]

DOOR_TO_LIGHT_MAP = {
    "Basement Front Door": ["Basement Front Door Light"],
    "Basement Back Door": ["Backyard Light", "Backyard Outlet"]
}

HUBITAT_ACCESS_TOKEN = os.getenv("HUBITAT_ACCESS_TOKEN", "ACCESS_TOKEN_NOT_CONFIGURED")
HUBITAT_UUID = os.getenv("HUBITAT_UUID", "UUID_NOT_CONFIGURED")
HUBITAT_BASE_URL = f"https://cloud.hubitat.com/api/{HUBITAT_UUID}/apps/9"
HUBITAT_DEVICES_URL = f"{HUBITAT_BASE_URL}/devices?access_token={HUBITAT_ACCESS_TOKEN}"

# https://cloud.hubitat.com/api/10bd8767-6e19-4812-86a8-440a2cdbf442/apps/9/devices/1/on?access_token=7b7fb058-a08e-4d23-b9c4-ae990524519e
HUBITAT_SWITCH_ON_URL = f"{HUBITAT_BASE_URL}/devices/%s/on?access_token={HUBITAT_ACCESS_TOKEN}"

HUBITAT_SWITCH_OFF_URL = f"{HUBITAT_BASE_URL}/devices/%s/off?access_token={HUBITAT_ACCESS_TOKEN}"

# TODO
DEVICE_CACHE = [{"id":"1","name":"Inovelli Z-Wave Smart Scene Switch S2","label":"Gym Lights"},{"id":"2","name":"Inovelli Z-Wave Smart Scene Switch S2","label":"Living Room Light"},{"id":"131","name":"Inovelli Z-Wave Smart Scene Switch S2","label":"Basement Entry Light"},{"id":"3","name":"Inovelli Z-Wave Smart Scene Switch S2","label":"Julio's Office Light"},{"id":"67","name":"Julio\u2019s iPhone","label":"Julio\u2019s iPhone"},{"id":"4","name":"Inovelli Z-Wave Smart Scene Switch S2","label":"Backyard Light"},{"id":"5","name":"hueBridge","label":"Hue Bridge (2F208D)"},{"id":"6","name":"hueBridgeBulb","label":"hallway light"},{"id":"102","name":"Inovelli Z-Wave Smart Scene Switch S2","label":"Master Bedroom Ceiling Fan"},{"id":"135","name":"Generic Z-Wave Smart Switch","label":"Backyard Outlet"},{"id":"7","name":"hueBridgeBulb","label":"hallway light"},{"id":"8","name":"hueBridgeBulb","label":"Julio's lamp"},{"id":"136","name":"Generic Z-Wave Smart Dimmer","label":"Movie Room Lights"},{"id":"137","name":"Generic Z-Wave Smart Dimmer","label":"Dining Room Lights"},{"id":"9","name":"hueBridgeBulb","label":"Living room floor lamp"},{"id":"138","name":"GE Smart Fan Control","label":"Dining Room Fan"},{"id":"10","name":"hueBridgeBulb","label":"Living Room Floor Lamp"},{"id":"139","name":"Inovelli Z-Wave Smart Scene Switch S2","label":"Basement Front Door Light"},{"id":"11","name":"hueBridgeBulb","label":"Marissa's lamp"},{"id":"142","name":"GE Enbrighten Z-Wave Smart Switch","label":"Laundry Room Light"},{"id":"143","name":"GE Enbrighten Z-Wave Smart Switch","label":"Guest Bathroom Light"},{"id":"144","name":"GE Enbrighten Z-Wave Smart Switch","label":"Guest Bathroom Fan"}]

def lambda_handler(event, context):
    """
    Handles an SES email receipient action
    
    Expects an email from ADT, for example:
    
    Subject:
    JULIO SANTOS's System: Panel was Disarmed by Remote User at 5:46 pm
    
    Body:
    JULIO SANTOS's System: The Panel was Disarmed by Remote User at 5:46 pm on Sunday, January 24 2021.
    
    This is a monitoring message from ADT Security. Log in at https://www.adt.com/control-login to manage your system and view other recent activity.
    
    
    
    Smart Security Technology backed by 24/7 Monitoring. ADT. Real Protection.
    
    Ref: M39867042062 - 10362591
    """
    # print (f"Devices Url: {HUBITAT_DEVICES_URL}")
    for record in event['Records']:
        handleRecord(record)
    return {
        'statusCode': 200,
        'body': json.dumps('Processed records')
    }

def handleRecord(record):
    eventSource = record['EventSource']
    messageString = record['Sns']['Message']
    messageJson = json.loads(messageString)
    # should be notifications@adtcontrol.com
    mailSource = messageJson['mail']['source']
    # should be something like
    # JULIO SANTOS's System: The Basement Front Door was Opened at 8:04 pm
    # JULIO SANTOS's System: The [DEVICE NAME] was [ACTION] at [TIME]
    mailSubject = getSubject(messageJson['mail']['headers'])
    print (f"Source: {mailSource}\nSubject: {mailSubject}")

    for door in DOOR_TO_LIGHT_MAP.keys():
        print (f"Evaluating {door}")
        if door in mailSubject:
            print ("Door is in mail subject")
            lights = DOOR_TO_LIGHT_MAP.get(door)
            for light in lights:
                print (f"Evaluating light {light}")
                turnOnLight(light)

def turnOnLight(lightName):
    lightId = getDeviceId(lightName)
    if lightId is not None:
        deviceUrl = HUBITAT_SWITCH_ON_URL % (lightId)
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
    print (f"Getting {deviceName} id")
    for device in DEVICE_CACHE:
        print (f"Evaluating {device}")
        if device['label'] == deviceName:
            id = device['id']
            print (f"Returning {id}")
            return id

def getSubject(headerList):
    for header in headerList:
        if header['name'] == 'Subject':
            return header['value']
    return None