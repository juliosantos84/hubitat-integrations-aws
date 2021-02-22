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
    "doorbell@automation.everythingbiig.com"
]

HUBITAT_ACCESS_TOKEN = os.getenv("HUBITAT_ACCESS_TOKEN", "ACCESS_TOKEN_NOT_CONFIGURED")
HUBITAT_UUID = os.getenv("HUBITAT_UUID", "UUID_NOT_CONFIGURED")
HUBITAT_BASE_URL = f"https://cloud.hubitat.com/api/{HUBITAT_UUID}/apps/159"
HUBITAT_DOORBELL_EVENT_URL = f"{HUBITAT_BASE_URL}/trigger?access_token={HUBITAT_ACCESS_TOKEN}"



def lambda_handler(event, context):
    """
    Expects an SNS event with Records representing SES Email notifications.

    Emails have the subject:
    JULIO SANTOS's System: The button on Doorbell was pushed at 6:52 pm
    """
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
    if "Doorbell was pushed" in mailSubject:
        print("Received doorbell event, sending notification")
        sendHubitatDoorbellEvent()

def sendHubitatDoorbellEvent():
    r = requests.get(HUBITAT_DOORBELL_EVENT_URL)
    if r.status_code > 200:
        print ("Something bad happened.")
    else:
        print ("Command sent")
    return

def getSubject(headerList):
    for header in headerList:
        if header['name'] == 'Subject':
            return header['value']
    return None