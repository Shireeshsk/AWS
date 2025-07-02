import json
import boto3
from datetime import datetime

# Initialize AWS clients
sns = boto3.client('sns')
sqs = boto3.client('sqs')

# Hardcoded values
SNS_TOPIC_ARN = 'arn:aws:sns:eu-north-1:797320052697:canteen-orders-topic'
SQS_QUEUE_URL = 'https://sqs.eu-north-1.amazonaws.com/797320052697/canteen-orders-queue'

def lambda_handler(event, context):
    for record in event.get('Records', []):
        try:
            # Extract message details
            message_id = record['messageId']
            receipt_handle = record['receiptHandle']
            message_body = record['body']
            
            print(f"Processing message: {message_id}")
            
            # Parse JSON message
            try:
                order_data = json.loads(message_body)
                
                # Format timestamp
                order_time = datetime.strptime(
                    order_data['timestamp'], 
                    '%Y-%m-%dT%H:%M:%S.%fZ'
                ).strftime('%Y-%m-%d %H:%M:%S')
                
                # Generate items summary
                items_summary = "\n".join(
                    [f"  - {item['name']} × {item['quantity']}" 
                     for item in order_data['items']]
                )
                
                # Create formatted email content
                email_body = f"""
🍽️ NEW CANTEEN ORDER NOTIFICATION

Customer: {order_data['customer']}
Order Time: {order_time}

ORDER SUMMARY:
{items_summary}

TOTAL COST: ${order_data['totalCost']:.2f}
----------------------------------------
Message ID: {message_id}
"""
                # Send SNS notification
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject="🍽️ New Canteen Order",
                    Message=email_body
                )
                
                # Delete processed message
                sqs.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=receipt_handle
                )
                
                print(f"Successfully processed message: {message_id}")
                
            except json.JSONDecodeError:
                print(f"Invalid JSON in message: {message_id}")
                # Handle non-JSON messages differently if needed
                
        except Exception as e:
            print(f"ERROR processing message {message_id}: {str(e)}")
            # Consider DLQ for permanent failures
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processed successfully')
    }
