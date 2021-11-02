import sys
sys.path.append("../")

from utils.event import botoClient
import json
import time

client = botoClient()
sess = client.session(profile_name='electromech',region_name='us-east-1')

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
    event = sess.client('events')
    prefix_rules = event.list_rules(
        NamePrefix=prefix,
    )
    
    for rule in prefix_rules['Rules']:
        response = event.delete_rule(
            Name=rule['Name'],
            Force=True
        )

    return response


def remove_attached_rules(attached_function:str, rule_prefix:str):
    t = list_lambda_triggers(attached_function)
    if t.get('Statement'):
        for sid in t['Statement']:
            print(sid['Sid'])
            detach_lambda_rule(attached_function, sid['Sid'])
    time.sleep(3)
    del_rule(prefix=rule_prefix)


rule_function_name="rulegen-scale"

t = list_lambda_triggers(rule_function_name)
if t.get('Statement'):
    for sid in t['Statement']:
        print(sid['Sid'])
        detach_lambda_rule(rule_function_name, sid['Sid'])
