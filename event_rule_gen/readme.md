# sheduled Autocaling generator

sudo npm install -G serverless
npm i -D serverless-dotenv-plugin

service_type: `ec2 | fargate`


## input json data

### ec2

`scaling_group_name = NAME OF EC2 SCALIGING GROUP`

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

`ecs_cluster = YOUR CLUSTER NAME`

`ecs_service = YOUR SERVICE NAME`

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

## env vars in `.env.dev`

        ENV_AWS_PROFILE="electromech"
        ENV_AWS_REGION="us-east-1"
        AUTOSCALE_LAMBDA_ARN="arn:aws:lambda:us-east-1:303373580614:function:shedule-eventscale-dev-autoscale"
        BUCKET_NAME="shedule-event-ec2"
        BUCKET_FILE="test.json"

### lambda 2

Example input to s3 file:

    [
        {
            "service_type": "fargate",
            "scaling_group_name": "service/scale/demo",
            "shedule_table":  {
                "date": "17/09/2021",
                "shedule": [
                    {
                        "start": "11:55:00",
                        "end": "11:57:00",
                        "count": 4
                    },
                    {
                        "start": "11:45:00",
                        "end": "13:57:00",
                        "count": 40
                    }
                ]
            }
        },
        {
            "service_type": "ec2",
            "scaling_group_name": "demo",
            "shedule_table":  {
                "date": "17/09/2021",
                "shedule": [
                    {
                        "start": "12:55:00",
                        "end": "12:57:00",
                        "count": 4
                    },
                    {
                        "start": "12:45:00",
                        "end": "13:57:00",
                        "count": 40
                    }
                ]
            }
        }
    ]
