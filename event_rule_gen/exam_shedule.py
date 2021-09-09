import boto3
from botocore.exceptions import ClientError
from utils.event import event_data, ApiGatewayResponse
import shedule_table as st
from shedule_event import datetime_to_cron, put_rule, attach_event_rule
import os
import json
from datetime import datetime
import time
import uuid

api_return = ApiGatewayResponse()


def get_s3_file(bucket_name, file_name):

    print(f"bucket: {bucket_name} / {file_name}")
    s3 = boto3.resource("s3")

    file = s3.Object(bucket_name, file_name)

    shed = file.get()["Body"].read()

    return json.loads(shed)


def generate_cloud_watch_rules(event, handler):

    print("current time:")
    print(datetime.now().time())

    print("current timezone")
    print(time.tzname)

    bucket_name = os.environ.get("BUCKET_NAME")
    bucket_file = os.environ.get("BUCKET_FILE")

    # cloud watch event rule
    event_rule_prefix = os.environ.get("EVENT_RULE_PREFIX") or "event-scale"

    # next lambda
    lambda_arn = os.environ.get("AUTOSCALE_LAMBDA_ARN")
    lambda_name = lambda_arn.split(":")[-1]

    # extra info
    aws_region = lambda_arn.split(":")[3]
    account_id = lambda_arn.split(":")[4]

    # main
    data = event_data(event=event)

    if data.get("shedule_table"):
        shedule_time = data["shedule_table"]
        # scaling target
        autoscaling_group_name = data["scaling_group_name"]
        service_type = data["service_type"]
    else:
        d = get_s3_file(bucket_name, bucket_file)
        shedule_time = d["shedule_table"]
        # scaling target
        autoscaling_group_name = d["scaling_group_name"]
        service_type = d["service_type"]
        del d

    df = st.get_shedule(shedule_time)

    tf, end_time = st.shedule(df)

    api_return.body({"response": ""}, status_code=200)

    for index, row in tf.iterrows():

        utc_time = row["utc_time"]
        min_count = row["count"]

        print("utc_time: " + datetime_to_cron(utc_time))
        print("time: " + datetime_to_cron(row["time"]))
        print(min_count)
        # print(index)

        rule_name = f"{event_rule_prefix}-{uuid.uuid4()}"
        r = put_rule(
            name=rule_name,
            time=utc_time,
            input_data={
                "min_count": min_count,
                "autoscaling_group_name": autoscaling_group_name,
                "service_type": service_type,
                "event_rule_arn": f"arn:aws:events:{aws_region}:{account_id}:rule/{event_rule_prefix}-{index}",
                "event_rule_name": rule_name,
                "statement_id": f"id-{rule_name}",
                "lambda_function_name": lambda_name,
            },
            lambda_arn=lambda_arn,
        )

        if r:
            a = attach_event_rule(
                lambda_arn=lambda_arn,
                event_arn=r["rule"]["RuleArn"],
                statement_id=f"statement-{rule_name}",
            )

    api_return.body({"response": {"rule": r, "lambda": a}}, status_code=200)

    return api_return.response()
