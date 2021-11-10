# Custom autoscaling for ec2/fargate

---

# Problem statement

---

There are 2 parts in order to perform this process

1. `rulegen` serverless code to shedule cloudwatch events for autoscaling.

2. `rulegen-scale` serverless code which gets invoked by `rulegen` cloudwatch rules to perform autoscaling on defined autoscaling groups.

## logical flow

- sheduled events for multiple resource and time, autoscaling will be defined by use in for of json as the syntax defined in [rulegen](https://github.com/electromech-117/schoolG/tree/main/event_rule_gen)

- This json will be uploaded to s3 bucket, before uploading bucket-arn and file name has to be defined in `serverless.yml` file as defined in [rulegen](https://github.com/electromech-117/schoolG/tree/main/event_rule_gen)

- On s3 bucket put event for that file `rulegen` lambda will generate cloudwatch event rules based on shedules and minimum count defined in json file by the user.

- This rules will trigger next lambda [rulegen-scale](https://github.com/electromech-117/schoolG/tree/main/scale) which will perform task of modifing autoscaling minimum count of ec2/fargate and after updating autoscaling count, event rule will be removed as it was been made to run once only.


## Flow Diagram

![Diagram flow](https://raw.githubusercontent.com/electromech-117/schoolG/test/.github/images/customAutoScaling.jpeg?token=AVCSZ6N6PQG7K5TRHS6ZEATBRNZAQ)

## prerequisite
1. [Nodejs](https://nodejs.org/en/)
2. [npm](http://npmjs.org/install.sh)

To install nodejs [click here](https://github.com/nodesource/distributions)

---

## Steps for implementation

1. Install serverless on your local device.
        
    - `sudo npm install -G serverless`

    - Now inside git repo directory run: `npm i -D serverless-dotenv-plugin`

2. Create a s3 bucket on your aws account where you will upload your sheduled scaling json file.

3. provide required variables values at `.env.dev` file as follows

        ENV_AWS_REGION="us-east-1"
        ENV_AWS_PROFILE="electromech"

        BUCKET_NAME="shedule-event-ec2"
        BUCKET_FILE="test.json"

4. run `serverless deploy`
