import json
import urllib3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda handler for Amazon Lex gold rate bot
    """
    try:
        # Log the incoming event
        logger.info(f"Event: {json.dumps(event)}")

        # Extract sessionId or use default if not provided
        session_id = event.get('sessionId', 'defaultSessionId')

        # Get the intent name
        intent_name = event['sessionState']['intent']['name']

        if intent_name == 'GetGoldRate':
            return get_gold_rate(event, session_id)
        else:
            return close(event, 'Failed', 'Intent not recognized', session_id)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return close(event, 'Failed', 'Sorry, I encountered an error while processing your request.', 'defaultSessionId')


def get_gold_rate(event, session_id):
    """
    Fetch current gold rate and convert it to INR per 10 grams
    """
    try:
        http = urllib3.PoolManager()

        # API key and URL
        api_key = "74a9922dd8343668bbc6cd1c935a505d"
        api_url = f"https://api.metalpriceapi.com/v1/latest?api_key={api_key}&base=USD&currencies=INR,XAU"

        # Make the request
        response = http.request('GET', api_url)

        if response.status == 200:
            data = json.loads(response.data.decode('utf-8'))
            logger.info(f"API Response: {data}")

            rates = data.get("rates", {})
            usd_to_inr = rates.get("INR")
            xau_rate = rates.get("XAU")  # This is how much gold (in oz) you get for 1 USD

            if usd_to_inr and xau_rate and xau_rate != 0:
                # Convert to USD per ounce
                gold_price_usd_per_ounce = 1 / xau_rate

                # Convert to INR per ounce
                gold_price_inr_per_ounce = gold_price_usd_per_ounce * usd_to_inr

                # Convert ounce to grams (1 troy ounce = 31.1035 grams)
                gold_price_inr_per_gram = gold_price_inr_per_ounce / 31.1035

                # Calculate price per 10 grams
                price_per_10_grams = round(gold_price_inr_per_gram * 10, 2)
                gold_price_usd_formatted = round(gold_price_usd_per_ounce, 2)

                message = f"The current gold rate is ₹{price_per_10_grams} per 10 grams (${gold_price_usd_formatted} per ounce)."
                return close(event, 'Fulfilled', message, session_id)
            else:
                return close(event, 'Failed', 'Failed to fetch valid gold rate or INR conversion.', session_id)
        else:
            logger.error(f"API Error: Status {response.status}")
            return close(event, 'Failed', 'Sorry, I could not fetch the current gold rate. Please try again later.', session_id)

    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return close(event, 'Failed', 'Sorry, there was an error fetching the gold rate.', session_id)


def close(event, fulfillment_state, message, session_id):
    """
    Close the session with a message - Updated to include sessionId
    """
    response = {
        'sessionId': session_id,
        'sessionState': {
            'dialogAction': {
                'type': 'Close'
            },
            'intent': {
                'name': event['sessionState']['intent']['name'],
                'state': fulfillment_state
            }
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': message
            }
        ]
    }

    # Optionally include additional attributes
    if 'requestAttributes' in event:
        response['requestAttributes'] = event['requestAttributes']
    if 'sessionAttributes' in event:
        response['sessionAttributes'] = event['sessionAttributes']

    logger.info(f"Response: {json.dumps(response)}")
    return response
