from boto3 import client
import boto3
from botocore.exceptions import ClientError
from utils.event import event_data, ApiGatewayResponse
import shedule_table as st
from shedule_event import datetime_to_cron, put_rule, attach_event_rule
import os

api_return = ApiGatewayResponse()


def generate_cloud_watch_rules(event, handler):

    # cloud watch event rule
    event_rule_prefix = os.environ.get("EVENT_RULE_PREFIX") or "event-scale-emc-"

    # next lambda
    lambda_arn = os.environ.get("AUTOSCALE_LAMBDA_ARN")

    lambda_name = lambda_arn.split(":")[-1]

    # scaling target
    autoscaling_group_name = os.environ.get("AUTO_SCALE_GROUP_NAME")

    # extra info
    aws_region  = lambda_arn.split(":")[3]
    account_id = lambda_arn.split(":")[4]

    # main
    data = event_data(event=event)

    shedule_time = data["shedule_table"]

    df = st.get_shedule(shedule_time)

    tf, end_time = st.shedule(df)
    
    api_return.body({"response": ""}, status_code=200)

    for index, row in tf.iterrows():

        utc_time = row["utc_time"]
        min_count = row["count"]

        print(datetime_to_cron(utc_time))
        print(min_count)
        # print(index)

        r = put_rule(
            
            name=f"{event_rule_prefix}-{index}",
            time=utc_time,
            input_data={
                "min_count": min_count,
                "autoscaling_group_name": autoscaling_group_name,
                "event_rule_arn": f"arn:aws:events:{aws_region}:{account_id}:rule/{event_rule_prefix}-{index}",
                "event_rule_name": f"{event_rule_prefix}-{index}",
                "statement_id": f"statement-id-{event_rule_prefix}-{index}",
                "lambda_function_name": lambda_name
            },
            
            lambda_arn=lambda_arn,
        )

        if r:
            a = attach_event_rule(
            
                lambda_arn=lambda_arn,
                event_arn=r["rule"]["RuleArn"],
                statement_id=f"statement-id-{event_rule_prefix}-{index}",
            )
    
    api_return.body({"response": {"rule":r,"lambda":a}}, status_code=200)
    
    return api_return.response()
