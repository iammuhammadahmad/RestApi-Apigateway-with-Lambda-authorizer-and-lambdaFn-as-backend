import json


def lambda_handler(event, context):
    http_method = event['context']['http-method']

    if http_method == 'GET':
        username = event['params']['path']['value']
        # TODO implement
        return {
            'statusCode': 200,
            'Request': http_method,
            'username': username
        }

    elif http_method == 'POST':
        username = event['params']['querystring']['username']
        # TODO implement
        return {
            'statusCode': 200,
            'Request': http_method,
            'username': username
        }

