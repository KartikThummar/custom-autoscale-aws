import json
from bson import json_util
import boto3
import botocore.exceptions
import os

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
    """
    For not caring about having aws profiles been managed while testing code locally
    and while sharing code to others or to aws resource eg: lambda, ec2, ecs
    """

    def __init__(self):
        self.profile_name: str = ""
        self.region_name: str = ""

    def config(self, conf_path: str = ""):
        """
        search for aws profile configs in json file present at `conf_path`
        for boto3 sesstion to consider profile name defined in that json file
        example config.json:
            {
                "aws_profile_name": "myprofile",
                "aws_region_name": "us-east-1"
            }
        """
        if os.path.exists(conf_path):
            with open(f"{conf_path}", "r") as c:
                conf = json.loads(c.read())
            self.profile_name = conf.get("aws_profile_name") or ""
            self.region_name = conf.get("aws_region_name") or ""

    def session(self, profile_name: str = "", region_name: str = ""):
        """
        check for boto3 Session profile, if not present, set to default
        """

        if self.profile_name != "":
            pass
        elif profile_name != "":
            self.profile_name = profile_name
            self.region_name = region_name
        else:
            return boto3.Session()

        try:
            if self.region_name != "":
                return boto3.Session(
                    profile_name=self.profile_name, region_name=self.region_name
                )
            else:
                return boto3.Session(profile_name=self.profile_name)

        except botocore.exceptions.ProfileNotFound:
            return boto3.Session()