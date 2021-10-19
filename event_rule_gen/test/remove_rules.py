import boto3

sess = boto3.session.Session(profile_name='electromech',region_name='us-east-1')



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

x=del_rule('event-scale')

print(x)
