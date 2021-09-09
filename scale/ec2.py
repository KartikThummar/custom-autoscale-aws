from botocore.exceptions import ClientError
from utils.event import event_data, ApiGatewayResponse
import logging
import boto3
from remove_event import remove_cloudwatch_rule, detach_lambda_rule

api_return = ApiGatewayResponse()

# boto_sess = Session(profile_name='school_guru')
# client = boto_sess.client('autoscaling')

# ARN = """automation-auto-scaling-testing"""

    
def update_ec2_autoscale(event, handler):

    api_return.body({"response": ""},status_code=200)

    data = event_data(event=event)

    # auto scaling data
    min = int(data["min_count"])
    
    min_scale = 1
    # dont't let desired count be 0
    if min == 0:
        min = min_scale
    
    autoscale_grp_arn = data["autoscaling_group_name"]
    
    # event rule data
    rule_name = data.get("event_rule_name")
    event_statement_id = data.get("statement_id")
    lambda_name = data.get("lambda_function_name")


    try:
        client = boto3.client('autoscaling')

    except ClientError as e:
        logging.error(e)
        return False

    scale_response = client.update_auto_scaling_group(
        AutoScalingGroupName=autoscale_grp_arn,
        # LaunchConfigurationName='string',
        # LaunchTemplate={
        #     'LaunchTemplateId': 'string',
        #     'LaunchTemplateName': 'string',
        #     'Version': 'string'
        # },
        # MixedInstancesPolicy={
        #     'LaunchTemplate': {
        #         'LaunchTemplateSpecification': {
        #             'LaunchTemplateId': 'string',
        #             'LaunchTemplateName': 'string',
        #             'Version': 'string'
        #         },
        #         'Overrides': [
        #             {
        #                 'InstanceType': 'string',
        #                 'WeightedCapacity': 'string',
        #                 'LaunchTemplateSpecification': {
        #                     'LaunchTemplateId': 'string',
        #                     'LaunchTemplateName': 'string',
        #                     'Version': 'string'
        #                 }
        #             },
        #         ]
        #     },
        #     'InstancesDistribution': {
        #         'OnDemandAllocationStrategy': 'string',
        #         'OnDemandBaseCapacity': 123,
        #         'OnDemandPercentageAboveBaseCapacity': 123,
        #         'SpotAllocationStrategy': 'string',
        #         'SpotInstancePools': 123,
        #         'SpotMaxPrice': 'string'
        #     }
        # },
        # DefaultCooldown=123,
        # AvailabilityZones=[
        #     'string',
        # ],
        # HealthCheckType='string',
        # HealthCheckGracePeriod=123,
        # PlacementGroup='string',
        # VPCZoneIdentifier='string',
        # TerminationPolicies=[
        #     'string',
        # ],
        # NewInstancesProtectedFromScaleIn=True|False,
        # ServiceLinkedRoleARN='string',
        # MaxInstanceLifetime=123,
        # CapacityRebalance=True|False,
        # Context='string'
        # MaxSize=123,
        # MinSize=1,
        DesiredCapacity=min,
    )
    
    removed_event = False

    if scale_response and rule_name != None:
        detach_lambda_rule(
            function_name=lambda_name,
            statement_id=event_statement_id
        )
        removed_event = remove_cloudwatch_rule(name=rule_name)



    api_return.body({"response": {"scaled":scale_response, "event_removed": removed_event}}, status_code=200)
    
    return api_return.response()
