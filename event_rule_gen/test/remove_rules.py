import sys

sys.path.append("../")

from utils.event import botoSession
import json
import time

boto = botoSession()
sess = boto.session(profile_name="electromech", region_name="us-east-1")


def list_lambda_triggers(FunctionName):
    client = sess.client("lambda")
    try:
        resp = client.get_policy(
            FunctionName=FunctionName,
        )
        return json.loads(resp["Policy"])
    except client.exceptions.ResourceNotFoundException:
        return {}


def detach_lambda_rule(function_name, statement_id):
    client = sess.client("lambda")

    response = client.remove_permission(
        FunctionName=function_name,
        StatementId=statement_id,
    )
    return response

def del_rule(prefix):
    event = sess.client("events")
    prefix_rules = event.list_rules(
        NamePrefix=prefix,
    )

    for rule in prefix_rules["Rules"]:
        response = remove_cloudwatch_rule(rule["Name"])

    return response

def remove_cloudwatch_rule(name):

    client = sess.client("events")

    list_targets = client.list_targets_by_rule(
        Rule=name,
    )

    ids = []

    for target in list_targets["Targets"]:
        ids.append(target["Id"])

    client.remove_targets(
        Rule=name,
        Ids=ids,
        # Force=True|False
    )

    response = client.delete_rule(Name=name)

    return response


def remove_attached_rules(attached_function: str, rule_prefix: str):
    t = list_lambda_triggers(attached_function)
    if t.get("Statement"):
        for sid in t["Statement"]:
            print(sid["Sid"])
            detach_lambda_rule(attached_function, sid["Sid"])
    time.sleep(3)
    del_rule(prefix=rule_prefix)


remove_attached_rules("rulegen-scale", rule_prefix="event-scale")