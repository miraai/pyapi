from django.conf import settings
from requests.auth import HTTPBasicAuth
import requests

def check_email_hunter(email):
    email_check = requests.get(settings.EMAIL_HUNTER_BASE_URL + 'email-verifier',
        params = {
            'email': email,
            'api_key': settings.EMAIL_HUNTER_API_KEY
        })    
    if email_check.status_code != 200:
        return None, 'Invalid email'
    
    # Convert API data to json
    hunter_data = email_check.json()
    if hunter_data['data']['smtp_check']:
        return hunter_data, None
    else:
        return None, 'Email bounced'

def user_enrichment_clearbit(email):
    additional_user_data = requests.get(settings.CLEARBIT_BASE_URL + 'combined/find',
        params = {
            'email': email
        }, auth=HTTPBasicAuth(settings.CLEARBIT_API_KEY, ''))

    if additional_user_data != 200:
        print(additional_user_data.json())
        return None, 'Something went wrong'

    user_data = additional_user_data.json()
    # Just print it
    print(user_data)