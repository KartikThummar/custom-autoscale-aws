# sheduled Autocaling generator

sudo npm install -G serverless
npm i -D serverless-dotenv-plugin

service_type: `ec2 | fargate`


## input json data

    {
        "service_type": "ec2",
        "scaling_group_name": "scl-ec2-group",
        "shedule_table":  {
            "date": "08/09/2021",
            "shedule": [
                {
                    "start": "18:10:00",
                    "end": "18:12:00",
                    "count": 2
                }
            ]
        }
    }

## env vars

### lambda 1

- EVENT_RULE_PREFIX="test_scale"

- AUTOSCALE_LAMBDA_ARN="arn:aws:lambda:ap-south-1:163742846785:function:testing-shedule-event-dev-testing-autoscale"

- AUTO_SCALE_GROUP_NAME="automation-auto-scaling-testing"

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