from models import User, Posts, PostsLike
from django.db import IntegrityError, OperationalError, DatabaseError

import bcrypt

def register_user(email, password):
  try:
    # hash the password
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(email = email, password = hash_pwd)
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
  
    # Check password
    valid_pwd = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
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
    post = Post.objects.get(id__exact = post_id)
    if not post:
      return None, 'Post not found'

  except (IntegrityError, OperationalError, DatabaseError) as error:
    return None, error.message

  return post

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
        like = PostsLike(liked = True)
        like.post_id = post_id
        like.user_id = user_id
        like.save()
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

