# sheduled Autocaling generator

sudo npm install -G serverless
npm i -D serverless-dotenv-plugin

service_type: `ec2 | fargate`


## input json data

### ec2

    {
        "service_type": "ec2",
        "scaling_group_name": "scl",
        "shedule_table":  {
            "date": "09/09/2021",
            "shedule": [
                {
                    "start": "15:00:00",
                    "end": "15:30:00",
                    "count": 4
                },
                {
                    "start": "15:15:00",
                    "end": "16:05:00",
                    "count": 5
                },
                {
                    "start": "16:00:00",
                    "end": "16:05:00",
                    "count": 2
                }
            ]
        }
    }

### fargate

ecs_cluster = YOUR CLUSTER NAME
ecs_service = YOUR SERVICE NAME

    {
        "service_type": "fargate",
        "scaling_group_name": "service/ecs_cluster/ecs_service",
        "shedule_table":  {
            "date": "09/09/2021",
            "shedule": [
                {
                    "start": "15:00:00",
                    "end": "15:30:00",
                    "count": 4
                },
                {
                    "start": "15:15:00",
                    "end": "16:05:00",
                    "count": 5
                },
                {
                    "start": "16:00:00",
                    "end": "16:05:00",
                    "count": 2
                }
            ]
        }
    }

## env vars

### lambda 1


- EVENT_RULE_PREFIX="test_scale"

- AUTOSCALE_LAMBDA_ARN="arn:aws:lambda:ap-south-1:163742846785:function:testing-shedule-event-dev-testing-autoscale"

- BUCKET_NAME="testing-event-shedule"

- BUCKET_FILE="hi"

{
    "min_count": 2,
    "autoscaling_group_name": "automation-auto-scaling-testing",
    "event_rule_arn": "arn:aws:events:ap-south-1:163742846785:rule/test_autoscale-0",
    "event_rule_name": "test_autoscale-0",
    "statement_id": "statement-id-test_autoscale-0",
    "lambda_function_name": "testing-shedule-event-dev-testing-autoscale"
}
