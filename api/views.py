# coding=utf-8
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

import json
from api import database, auth
#import api.database, api.auth

def index(request):
  return JsonResponse({"status": "Hello World"})

@csrf_exempt
def register_user(request):
  if request.method == 'POST':
    # Check the request, request must not be empty
    if not request.body:
      return JsonResponse({
        'message': 'Please provide needed data'
      }, status = 400)
      
    # Convert string to dict
    json_data = json.loads(request.body)
    # Check for the needed data
    if 'email' not in json_data or 'password' not in json_data:
      return JsonResponse({
        'message': 'Email or password not provided'
      }, status = 400)
    
    user, error = database.register_user(json_data['email'], json_data['password'])
    if error:
      # Duplicate email address error
      if isinstance(error, IntegrityError):
        return JsonResponse({
          'message': 'User already exists'
        }, status = 500)
      # Generic error
      return JsonResponse({
        'message': 'Something went wrong'
      }, status = 400)

    return JsonResponse({
      'email': user.email,
      'message': 'User registered'
    }, status = 201)
    
  return JsonResponse({
    'message': 'HTTP method not allowed'
  }, status = 405)

@csrf_exempt
def login_user(request):
  if request.method == 'POST':
    # Check the request, request must not be empty
    if not request.body:
      return JsonResponse({
        'message': 'Please provide needed data'
      }, status = 400)
      
    # Convert string to dict
    json_data = json.loads(request.body)
    # Check for the needed data
    if 'email' not in json_data or 'password' not in json_data:
      return JsonResponse({
        'message': 'Email or password not provided'
      }, status = 400)

    # Check if the user exists
    user, error = database.check_user(json_data['email'], json_data['password'])
    if error:
      return JsonResponse({
        'message': error
      }, status = 400)

    # Create JWT and attach it to an Auth header
    jwt_token, jwt_error = auth.encode_jwt(user.id, user.email)
    if jwt_error:
      return JsonResponse({
        'message': jwt_error
      }, status = 400)

    response = JsonResponse({
      'message': 'User logged in'
    }, status=200)
    # Add JWT token to HTTP header
    response['Authorization'] = jwt_token
    return response
    
  return JsonResponse({
      'message': 'HTTP method not allowed'
  }, status = 405)

@csrf_exempt
def post_content(request):
  # User must be logged in
  access_token = request.META['HTTP_AUTHORIZATION']
  jwt_data, jwt_error = auth.decode_jwt(access_token)
  if jwt_error:
    return JsonResponse({
      'message': jwt_error
    }, status = 400)

  if request.method == 'POST':
    # Check the request, request must not be empty
    if not request.body:
      return JsonResponse({
        'message': 'Please provide needed data'
      }, status = 400)
      
    # Convert string to dict
    json_data = json.loads(request.body)
    if 'subject' not in json_data or 'content' not in json_data:
      return JsonResponse({
        'message': 'Subject or content not provided'
      }, status = 400)

    subject = json_data['subject']
    content = json_data['content']
    user_id = jwt_data['user_id']
    # Create post for logged in user
    post, post_error = database.create_post(subject, content, user_id)
    if post_error:
      return JsonResponse({
        'message': post_error
      }, status = 400)

    return JsonResponse({
    'post_subject': post.subject,
    'post_content': post.content
    }, status = 201)

  elif request.method == 'GET':
    post_id = request.GET['post_id']

    post, post_error = database.get_post(post_id)
    if post_error:
      return JsonResponse({
        'message': post_error
      }, status = 400)

    # Get post, accept query param
    return JsonResponse(post, status = 200)

  return JsonResponse({
    'message': 'HTTP method not allowed'
  }, status = 405)

@csrf_exempt
def like_post(request):
  # User must be logged in
  access_token = request.META['HTTP_AUTHORIZATION']
  jwt_data, jwt_error = auth.decode_jwt(access_token)
  if jwt_error:
    return JsonResponse({
      'message': jwt_error
    }, status = 400)

  if request.method == 'POST':
    # Convert string to dict
    json_data = json.loads(request.body)
    if 'post_id' not in json_data:
      return JsonResponse({
        'message': 'Subject or content not provided'
      }, status = 400)
    
    liked_post, liked_post_error = database.like_post(json_data['post_id'], jwt_data['user_id'])
    if liked_post_error:
      return JsonResponse({
        'message': liked_post_error
      }, status = 400)
    
    return JsonResponse({
      'post_id': liked_post.post_id,
      'user_id': liked_post.user_id,
      'like': liked_post.liked
    }, status = 200)

  return JsonResponse({
    'message': 'HTTP method not allowed'
  }, status = 405)
  
