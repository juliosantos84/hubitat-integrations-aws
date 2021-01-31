import json
import pytest
from unittest.mock import patch, MagicMock

from device_cacher import s3_cacher

@pytest.fixture()
def schedule_event():
    """ Generates API GW Event"""

    return {}

def test_lambda_handler(schedule_event):
    with patch('device_cacher.s3_cacher.requests') as req_mock:
        resp_mock = MagicMock()
        resp_mock.status_code = 200
        resp_mock.json = [{"id":"1","name":"Inovelli Z-Wave Smart Scene Switch S2","label":"Gym Lights"}]
        req_mock.get.return_value = resp_mock
        with patch('device_cacher.s3_cacher.boto3.client') as boto_mock:
            s3_mock = MagicMock()
            boto_mock.return_value = s3_mock
            s3_cacher.lambda_handler(schedule_event, "")
            req_mock.get.assert_called_with("https://cloud.hubitat.com/api/UUID_NOT_CONFIGURED/apps/9/devices?access_token=ACCESS_TOKEN_NOT_CONFIGURED")
            s3_mock.put_object.assert_called_with(
                Bucket=s3_cacher.DEVICE_CACHE_BUCKET,
                Key='devices/nameToIdMap.json',
                Body=json.dumps({"Gym Lights":"1"}).encode("utf-8")
            )
