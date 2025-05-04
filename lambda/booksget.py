import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('books')

def lambda_handler(event, context):
    # Log the entire event object to check what is received
    print("Event: ", json.dumps(event))
    
    try:
        # Ensure pathParameters exist before accessing 'id'
        if 'pathParameters' in event and 'id' in event['pathParameters']:
            id = event['pathParameters']['id']
        else:
            raise KeyError('pathParameters or id missing in the event object')
        
        # Query the DynamoDB table by 'id'
        response = table.get_item(Key={'id': id})
        
        # Check if the item exists
        if 'Item' in response:
            item = response['Item']
            return {
                'statusCode': 200,
                'body': json.dumps(item),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'  # CORS headers if needed
                }
            }
        else:
            # Return a 404 if the item is not found
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Item not found'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
    
    except Exception as e:
        # Log the exception for debugging
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
