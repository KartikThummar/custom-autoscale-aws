import boto3
from botocore.exceptions import ClientError
import logging
from utils.event import event_data, ApiGatewayResponse

api_return = ApiGatewayResponse()


def update_ecs_autoscale(service_name, cluster_name, min_count):
    
    client = boto3.client('application-autoscaling')

    response = client.register_scalable_target(
        ServiceNamespace='ecs',
        ResourceId=f'service/{cluster_name}/{service_name}',
        ScalableDimension='ecs:service:DesiredCount',
        MinCapacity=min_count,
        # MaxCapacity=10,
    )
    
    return response


# def update_service(event, handler):

#     api_return.body({"response": ""},status_code=200)

#     data = event_data(event=event)

#     # required inputs
#     cluster_name = data["cluster_name"]
#     service_name = data["service_name"]
#     desired_count = int(data["desired_count"])
#     min_count = int(data["min_count"])
#     max_count = int(data["max_count"])
#     # capacity_provider = int(data["capacity_provider"])


#     # don't go to 0
#     if 0 in [min_count, desired_count, max_count]:

#         api_return.body("Cannot set count to 0",status_code=400)
#         return api_return.response()

#     # main
#     try:
#         client = boto3.client("ecs")

#     except ClientError as e:
#         logging.error(e)
#         return False

#     # this won't work if autocaling is set
#     update_count = client.update_service(
#         cluster=cluster_name,
#         service=service_name,
#         desiredCount=desired_count,
#         forceNewDeployment=True,
#         # enableExecuteCommand=True|False
#     )


#     api_return.body([update_count])

#     return api_return.response()


# def describe_service(event, handler):

#     api_return.body({"response": ""},status_code=200)
#     data = event_data(event=event)

#     cluster_name = data["cluster_name"]
#     service_name = data["service_name"]

#     try:
#         client = boto3.client("ecs")

#     except ClientError as e:
#         logging.error(e)
#         return False

#     describe_service = client.describe_services(
#         cluster=cluster_name,
#         services=[
#             service_name,
#         ]
#     )

#     api_return.body(describe_service, status_code= 200)

#     return api_return.response()