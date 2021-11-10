import json
from bson import json_util
import boto3
import botocore.exceptions


def event_data(event):
    try:
        data = json.loads(event["body"])
    except KeyError:
        data = event
    return data


class ApiGatewayResponse:

    """
    api_response = {
        "statusCode": status_code,
        "body": json.dumps(
            {
                "body": body
            },
            default=json_util.default
        )
    }
    """

    def body(self, data, status_code=200):
        self.BODY = json.dumps({"body": data or ""}, default=json_util.default)
        self.status_code = status_code
        return self.BODY

    def response(self):
        return {
            "statusCode": self.status_code,
            "body": json.dumps({"body": self.BODY}, default=json_util.default),
        }


class botoSession:
    def __init__(self, profile_name=None, region_name=None):
        if profile_name:
            self.profile_name = profile_name
            try:
                return boto3.Session(profile_name=profile_name, region_name=region_name)
            except botocore.exceptions.ProfileNotFound:
                return boto3.Session()
        else:
            return boto3.Session()
