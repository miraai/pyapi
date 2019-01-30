from api.models import User, Posts, PostsLike
from django.db import IntegrityError, OperationalError, DatabaseError

import bcrypt

def register_user(email, password):
  try:
    # hash the password
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # We need to decode hashed password so we can save it as a pure string
    user = User(email = email, password = hash_pwd.decode('utf-8'))
    user.save()
  except (IntegrityError, OperationalError, DatabaseError) as error:
    return None, error.message

  return user, None

def check_user(email, password):
  try:
    # Find user by email
    user = User.objects.get(email__exact = email)
    if not user:
      return None, 'User doesn\'t exist'
  
    # Before comparing passwords we must encode them with utf-8
    input_pwd = password.encode('utf-8')
    hashed_pwd = user.password.encode('utf-8')
    print(type(input_pwd))
    print(input_pwd)
    print('------------')
    print(type(hashed_pwd))
    print(hashed_pwd)
    # Check encoded passwords
    valid_pwd = bcrypt.checkpw(input_pwd, hashed_pwd)
    if not valid_pwd:
      return None, 'Password incorrect'

  except (IntegrityError, OperationalError, DatabaseError) as error:
    return None, error.message

  return user, None
  
def create_post(subject, content, user_id):
  try:
    post = Posts(subject = subject, content = content)
    post.user_id = user_id
    post.save()
  except (IntegrityError, OperationalError, DatabaseError) as error:
    return None, error
  
  return post, None

def get_post(post_id):
  try:
    post = Posts.objects.get(id__exact = post_id)
    if not post:
      return None, 'Post not found'

    post = {
      'id': post.id,
      'subject': post.subject,
      'content': post.content,
      'num_like': 0
    }

    post_like = PostsLike.objects.filter(post_id__exact = post_id, liked = True).count()
    if post_like:
      post['num_like'] = post_like

  except (IntegrityError, OperationalError, DatabaseError) as error:
    return None, error.message

  return post, None

def like_post(post_id, user_id):
  try:
    # Find the post
    post = Posts.objects.filter(pk = post_id).first()
    if not post:
      return None, 'Post not found'

    if post:
      # Check if that user already liked that post
      liked_post = PostsLike.objects.filter(post_id = post_id, user_id = user_id).first()
      # Like didn't exist, create it
      if not liked_post:
        liked_post = PostsLike(liked = True)
        liked_post.post_id = post_id
        liked_post.user_id = user_id
        liked_post.save()
      else:
        # If the post is liked, unlike it
        if liked_post.liked:
          liked_post.liked = False
          liked_post.save()
        # If the post is unliked, like it
        else:
          liked_post.liked = True
          liked_post.save()
    
  except (IntegrityError, OperationalError, DatabaseError) as error:
    return None, error.message  
    
  return liked_post, None
  
def unlike_post():
  pass

