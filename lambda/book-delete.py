import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('books')

def lambda_handler(event, context):
    try:
        # Log the incoming event for debugging
        print("Received event: ", json.dumps(event))

        # Extract path parameters (id)
        if 'pathParameters' in event and 'id' in event['pathParameters']:
            id = event['pathParameters']['id']
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing id in path parameters'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'  # CORS header
                }
            }
        
        # Delete the item from DynamoDB
        response = table.delete_item(
            Key={'id': id}
        )
        
        # Check the response for errors
        if 'ConsumedCapacity' in response:
            # Item was deleted successfully
            return {
                'statusCode': 200,
                'body': json.dumps({'message': f'Book with id {id} deleted successfully'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'  # CORS header
                }
            }
        else:
            # Item was not found or there was an issue deleting
            return {
                'statusCode': 404,
                'body': json.dumps({'error': f'Book with id {id} not found'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'  # CORS header
                }
            }
    except Exception as e:
        # Log the exception for debugging
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # CORS header
            }
        }
