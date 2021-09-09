from botocore.exceptions import ClientError
import logging
import boto3


# boto_sess = Session(profile_name='school_guru')
# client = boto_sess.client('autoscaling')

# ARN = """automation-auto-scaling-testing"""


def update_ec2_autoscale(autoscaling_group_name, count):

    # auto scaling data

    autoscale_grp_arn = autoscaling_group_name

    # event rule data

    try:
        client = boto3.client("autoscaling")

    except ClientError as e:
        logging.error(e)
        return False

    scale_response = client.update_auto_scaling_group(
        AutoScalingGroupName=autoscale_grp_arn,
        MinSize=count,
    )

    return scale_response
