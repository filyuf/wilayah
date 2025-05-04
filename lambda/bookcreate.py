import json
import boto3
import uuid

# Initializing the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('books')  # The name of your DynamoDB table

def lambda_handler(event, context):
    try:
        # Print the event to see the structure
        print("Received event:", json.dumps(event))
        
        # Accessing the body of the event directly
        body = event  # No longer using json.loads(event['body'])
        title = body['title']
        
        # Creating an Item with a unique id and the passed title
        item = {
            'id': str(uuid.uuid4()),
            'title': title
        }
        
        # Inserting an item into the table
        table.put_item(Item=item)
        
        response = {
            'statusCode': 201,  # Use 201 Created for successful creation
            'body': json.dumps({'message': 'Item created successfully', 'id': item['id']})
        }
        return response  # Returning a 201 if the item has been inserted
    except Exception as e:
        error_response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        return error_response
