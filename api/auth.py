from django.conf import settings
from jwt import decode, encode, PyJWTError, ExpiredSignatureError

import time

def encode_jwt(user_id, user_email):
  try:
    current_timestamp = int(time.time()) 
    # JWT Payload
    payload = {
      'user_id': user_id,
      'user_email': user_email,
      'iat': current_timestamp,
      'exp': current_timestamp + settings.JWT_EXPIRE
    }
    encoded = encode(payload, settings.JWT_KEY, algorithm='HS256')
  except PyJWTError as error:
    return None, 'Error occured while validating JWT'
    
  return encoded, None

def decode_jwt(payload):
  try:
    decoded = decode(payload, settings.JWT_KEY, algorithm='HS256')
  except PyJWTError as error:
    if isinstance(error, ExpiredSignatureError):
      return None, 'JWT Expired'

    return None, 'Error occured while validating JWT'
  
  return decoded, None