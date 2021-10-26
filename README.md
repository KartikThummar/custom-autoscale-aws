# This code is to perform Automation on custom single time sheduled autoscaling for ec2/fargate

There are 2 parts in order to perform this process

1. `event_rule_gen` serverless code to shedule cloudwatch events for autoscaling.

2. `scale` serverless code which gets invoked by `event_rule_gen` cloudwatch rules to perform autoscaling on defined autoscaling groups.

## logical flow

- sheduled events for multiple resource and time, autoscaling will be defined by use in for of json as the syntax defined in [event_rule_gen](https://github.com/electromech-117/schoolG/tree/main/event_rule_gen)

- This json will be uploaded to s3 bucket, before uploading bucket-arn and file name has to be defined in `serverless.yml` file as defined in [event_rule_gen](https://github.com/electromech-117/schoolG/tree/main/event_rule_gen)

- On s3 bucket put event for that file `event_rule_gen` lambda will generate cloudwatch event rules based on shedules and minimum count defined in json file by the user.

- This rules will trigger next lambda [scale](https://github.com/electromech-117/schoolG/tree/main/scale) which will perform task of modifing autoscaling minimum count of ec2/fargate and after updating autoscaling count, event rule will be removed as it was been made to run once only.

## Steps for implementation

schoolG

    {
        "shedule_table":  {
                "date": "08/08/2021",
                "shedule": [
                    {
                        "start": "18:10:00",
                        "end": "18:12:00",
                        "count": 2
                    }
                ]
        }
    }

1. deploy scale

copy scale arn > event_rule_gen/.env.dev

2. deploy event_rule_gen
