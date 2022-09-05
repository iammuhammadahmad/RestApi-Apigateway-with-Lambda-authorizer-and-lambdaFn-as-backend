import json

def lambda_handler(event, context):
    username=event['params']['querystring']['username']
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(username)
    }
