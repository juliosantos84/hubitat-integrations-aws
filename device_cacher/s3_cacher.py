import json
import boto3

def lambda_handler(event, context):
    print ("Ran!")
    # s3 = boto3.client('s3')
    # s3.put_object(
    #     Bucket=os.getenv(DEVICE_CACHE_BUCKET,'com.everythingbiig.hubitat'),
    #     Key='devices/cached.json',
    #     Body=json.dumps({
    #         "id": 139,
    #         "label": "Basement Front Door Light"
    #     }).encode("utf-8")
    # )
